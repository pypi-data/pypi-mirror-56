"""Events for analyzing rotten code structures."""
import ast
from dataclasses import dataclass

from . import code, python


@dataclass
class Event:
    module: python.Module


@dataclass
class Dependency(Event):
    on: python.Name


@code.Scanner.register(ast.Import)
def handle_import(node: ast.Import, module, state):
    for alias in node.names:
        yield Dependency(module=module, on=python.Name(alias.name))


@code.Scanner.register(ast.ImportFrom)
def handle_from_import(node: ast.ImportFrom, module, state):
    # resolve module
    if not node.level:
        base_name = python.Name(node.module)
    else:
        base_name = module
        for _ in range(node.level - 1 if (module.is_package) else node.level):
            base_name = base_name.parent

        if node.module:
            base_name = base_name / node.module

    for alias in node.names:
        name = base_name / alias.name
        yield Dependency(module=module, on=python.Name(name))
