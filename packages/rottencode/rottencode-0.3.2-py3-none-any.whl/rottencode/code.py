import ast
import collections
from dataclasses import dataclass, field
import functools
import inspect
import itertools
import pathlib
import re
import sys
import typing

import structlog

from . import python, utils

sl = structlog.get_logger()
re_identifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)


def make_paths(paths) -> typing.Tuple[pathlib.Path, ...]:
    return tuple(pathlib.Path(path).resolve() for path in paths)


@dataclass
class Selection(utils.ConvertingDataclass):
    excludes: typing.Tuple[typing.Pattern] = field(default_factory=tuple)
    paths: typing.Tuple[pathlib.Path, ...] = field(
        default_factory=tuple, metadata={"converter": make_paths}
    )
    cwd: pathlib.Path = pathlib.Path(".").resolve()
    sys_paths: typing.List[pathlib.Path] = field(
        default_factory=lambda: list(
            reversed(sorted(pathlib.Path(path) for path in sys.path))
        )
    )

    def resolve_module_name(self, path):
        for sys_path in itertools.chain(self.paths, self.sys_paths):
            try:
                relative_path = path.relative_to(sys_path)
            except ValueError:
                pass
            else:
                return python.Name.from_relative_path(relative_path)
        raise ValueError("Path is not resolvable", path)

    @property
    def local_sys_paths(self):
        def gen():
            for path in self.sys_paths:
                try:
                    path.relative_to(self.cwd)
                except ValueError:
                    pass
                else:
                    yield path

        return list(gen())

    @property
    def search_paths(self):
        return self.paths or self.local_sys_paths

    def modules(self):
        for path in itertools.chain(
            *(path.glob("**/*.py") for path in self.search_paths)
        ):
            module_name = self.resolve_module_name(path)

            # we skip excludes
            if any(exclude.match(str(module_name)) for exclude in self.excludes):
                continue

            # we skip bad identifiers
            valid_identifiers = all(re_identifier.match(part) for part in module_name)
            if not valid_identifiers:
                continue

            sl.info("Found python file", path=path, module=module_name)
            yield python.Module(module_name, path)

    def module(self, name: python.Name):
        if isinstance(name, python.Module):
            return name

        def module_path(path_stem):
            possible_names = itertools.chain(
                (
                    (module_name, module_name.is_file())
                    for module_name in map(
                        path_stem.with_suffix, (".py", ".pyc", ".pyo", ".pyx")
                    )
                ),
                (
                    (
                        (path_stem / "__init__.py"),
                        (path_stem / "__init__.py").is_file(),
                    ),
                    (path_stem, path_stem.is_dir()),
                ),
            )
            for path, exists in possible_names:
                if exists:
                    return path

        parts = list(name)
        path = None
        module = None
        while parts:
            part = parts.pop(0)
            # find root and descent to module
            if path is None:
                try:
                    path = next(
                        filter(module_path, (path / part for path in self.search_paths))
                    )
                except StopIteration:
                    return None
                module = python.Module(part, path)

            else:
                path = module_path(path / part)
                if path:
                    module = python.Module(module / part, path)
                    # trim path if package
                    if module.is_package:
                        path = module.package_dir
                else:
                    break
        return module


class ScannerRegistry:
    handlers: typing.Dict[
        typing.Any, typing.Dict[typing.Any, typing.Set]
    ] = collections.defaultdict(lambda: collections.defaultdict(set))

    def __get__(self, inst, cls):
        if inst:
            return functools.partial(self.register_instance, inst)
        return functools.partial(self.register_class, cls)

    def register_class(self, cls, node_cls):
        def decorator(func):
            # put whole mro into registry
            for mro_cls in inspect.getmro(node_cls):
                self.handlers[mro_cls][cls].add(func)
            return func

        return decorator

    def register_instance(self, inst, node_cls):
        def decorator(func):
            # put whole mro into registry
            for mro_cls in inspect.getmro(node_cls):
                self.handlers[mro_cls][inst].add(func)
            return func

        return decorator

    @classmethod
    def find(cls, inst, node_cls):
        node_scanners = cls.handlers[node_cls]
        scanner_mro = inspect.getmro(inst.__class__)
        for scanner, handlers in node_scanners.items():
            if scanner is inst or scanner in scanner_mro:
                yield from handlers


class ScannerState(utils.adict):
    ...


class Scanner:
    register = ScannerRegistry()

    def scan(self, module: python.Module, state=None):
        if state is None:
            state = ScannerState()

        root_node = ast.parse(module.path.read_text(), module.path)
        for node in ast.walk(root_node):
            sl.debug("Handle node", node=node)
            yield from self.handle_node(module, node, state)

    def handle_node(self, module, node, state):
        node_cls = type(node)
        yield from itertools.chain(
            *(
                handler(node, module, state)
                for handler in ScannerRegistry.find(self, node_cls)
            )
        )
