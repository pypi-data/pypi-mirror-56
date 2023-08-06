import abc
import collections
from dataclasses import dataclass, field
import decimal
import functools
import itertools
import math
import sys
import typing

import pkg_resources

import _thread

from . import code, events, python, utils


class ExternalName(python.Name):
    ...


def _recursive_rotten(func):
    # skip circling dependencies
    rotten_running = set()

    @functools.wraps(func)
    def wrapper(self):
        key = id(self), _thread.get_ident()
        if key in rotten_running:
            # XXX TODO should this be zero, since we have a circle in dependencies
            return 1
        rotten_running.add(key)
        try:
            result = func(self)
        finally:
            rotten_running.discard(key)
        return result

    return wrapper


@dataclass
class Stats:
    modules: typing.Dict[python.Name, "Stats"]
    dependencies: typing.Set[python.Name] = field(default_factory=set)
    dependents: typing.Set[python.Name] = field(default_factory=set)
    tags: utils.adict = field(default_factory=utils.adict)

    @property
    def inbound(self):
        return len(self.dependents)

    @property
    def outbound(self):
        return len(self.dependencies)

    @property
    def internal_dependencies(self):
        return {dep for dep in self.dependencies if not isinstance(dep, ExternalName)}

    @property
    def internal_outbound(self):
        return len(self.internal_dependencies)

    @property
    def stability(self):
        try:
            return self.inbound / (self.inbound + self.internal_outbound)
        except ZeroDivisionError:
            return 1

    @property
    def is_independent(self):
        return not self.dependents

    @utils.reify
    @_recursive_rotten
    def rotten(self):
        # return 1
        if not self.internal_outbound:
            return 1

        index = decimal.Decimal("1")
        c = decimal.Decimal("0")
        for out in self.internal_dependencies:
            m = self.modules[out]
            if m.stability == 1:
                continue
            c += 1
            index *= m.rotten
        if c:
            try:
                return decimal.Decimal("1") / (decimal.Decimal(c) / index)
            except decimal.DivisionByZero:
                return decimal.Decimal("0")
        return 1


rotten_gradient = list(
    itertools.chain(
        # (
        #     utils.color_to_hex(color)
        #     for color in utils.linear_gradient(
        #         (255, 255, 255, 0), (255, 255, 255, 128), 2
        #     )
        # ),
        # (
        #     utils.color_to_hex(color)
        #     for color in utils.linear_gradient(
        #         (255, 255, 255, 0), (255, 255, 0, 128), 3
        #     )
        # ),
        utils.linear_gradient((255, 255, 0, 0), (255, 0, 0, 128), 50),
        utils.linear_gradient((255, 0, 0, 128), (0, 0, 0, 255), 200),
        utils.linear_gradient((255, 0, 0, 255), (0, 0, 0, 128), 200),
        utils.linear_gradient((255, 0, 0, 128), (0, 0, 0, 255), 20000),
    )
)


class AnalysisBase(abc.ABC):
    def __init__(self, selection: code.Selection):
        self.selection = selection

        scanner = code.Scanner()
        for module in selection.modules():
            for event in scanner.scan(module):
                self.account(event)

    @abc.abstractmethod
    def account(self, event):
        ...

    @abc.abstractmethod
    def report(self):
        ...


class PackageCollector(AnalysisBase):
    def __init__(self, selection: code.Selection):
        self.env = pkg_resources.Environment()
        self.env.scan()
        self.used_packages = set()

        super().__init__(selection)

    @utils.methdispatch
    def account(self, event):
        ...

    @account.register
    def account_dependency(self, event: events.Dependency):
        self.used_packages.add(str(event.on.root))

    def report(self):
        print("The follwoing packages and their distributions seem lost... \n")
        __import__("pdb").set_trace()  # XXX BREAKPOINT
        unused = set(self.env) - self.used_packages
        for package, dists in sorted(
            (
                package,
                ", ".join(
                    f"{dist.project_name} {dist.version}" for dist in self.env[package]
                ),
            )
            for package in unused
        ):
            print(package, "->", dists)


class ModuleAnalysis(AnalysisBase):
    def __init__(
        self,
        selection: code.Selection,
        *,
        with_externals=False,
        cluster=False,
        **kwargs,
    ):
        self.with_externals = with_externals
        self.cluster = cluster
        self.modules: typing.Dict[python.Name, Stats] = collections.defaultdict(
            lambda: Stats(self.modules)
        )

        super().__init__(selection)
        scanner = code.Scanner()
        for module in selection.modules():
            for event in scanner.scan(module):
                self.account(event)

    @utils.methdispatch
    def account(self, event):
        ...

    @account.register
    def account_dependency(self, event: events.Dependency):
        # trim dependency to module level or to external root module
        dependency_module = self.selection.module(event.on) or ExternalName(
            event.on.root
        )
        self.modules[event.module].dependencies.add(dependency_module)
        self.modules[dependency_module].dependents.add(event.module)

    def report(self):
        print(self.to_dot())

    def filtered_modules(self):
        for module, stats in sorted(self.modules.items()):
            if self.with_externals or not isinstance(module, ExternalName):
                yield module, stats

    def nodes(self):
        scale_rotten = decimal.Decimal("3")
        gradient_len = len(rotten_gradient)
        for module, stats in self.filtered_modules():
            try:
                log_color_index = -math.log(stats.rotten ** scale_rotten)
            except ValueError:
                # rotten can be very small
                log_color_index = gradient_len - 1

            rotten_color = rotten_gradient[min(int(log_color_index), gradient_len - 1)]
            fg_color = "#ffffff" if sum(rotten_color[:3]) <= 224 else "#000000"

            yield from (
                f'"{module}"',
                "[",
                "color=blue, penwidth=3, "
                if "plugin" in stats.tags
                else "color=red, penwidth=3, "
                if stats.is_independent
                else "",
                f'label="{module}\\ns={stats.stability:.4g}\\nr={stats.rotten:.4g}", ',
                f"margin={1 - stats.stability}, ",
                f'style=filled, fontcolor="{fg_color}", fillcolor="#{utils.color_to_hex(rotten_color)}", ',
                f"fontsize={10 + ((1 - stats.stability) * 5) ** 2}, ",
                "];",
            )

    def edges(self):
        for module, stats in self.filtered_modules():
            for dependency in sorted(stats.dependencies):
                dep_stats = self.modules.get(dependency)
                weight = (
                    1 + (1 - stats.stability * dep_stats.stability) * 10
                    if dep_stats
                    else 1
                )
                if self.with_externals or not isinstance(dependency, ExternalName):
                    yield f'"{module}" -> "{dependency}"[weight={weight}];'

    def clusters(self):
        clusters = collections.defaultdict(set)

        for module, stats in self.filtered_modules():
            if not module.is_package:
                package = module.parent
                clusters[package].add(module)
            else:
                clusters[module].add(module)

        for package, children in clusters.items():
            yield from (
                f'subgraph "cluster_{package}" {{',
                'style=filled; fillcolor="#efefef";',
                "margin=50;",
                "color=blue;",
                *(f'"{child}";' for child in children),
                "}",
            )

    def header(self):
        yield from (
            "node [shape=Mrecord, nodesep=20.0];",
            'graph [overlap="false"];',
            'splines="true";',
            "layout=fdp;",
            "rankdir=BT;",
            'sep="+25,25";',
            "maxiter=500;",
        )

    def to_dot(self,):
        return "\n".join(
            (
                "digraph RottenCode {",
                "\n".join(self.header()),
                "\n".join(self.clusters()) if self.cluster else "",
                "\n".join(self.nodes()),
                "\n".join(self.edges()),
                "}",
            )
        )
