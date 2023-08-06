import re

import click
import structlog

from . import code, events, logging, stats, utils

sl = structlog.get_logger()


class Regex(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        try:
            regex = re.compile(value)
            return regex
        except re.error:
            self.fail(f"`{value}` is not a valid regular expression value", param, ctx)

    def __repr__(self):
        return "REGEX"


@click.group()
@click.option("paths", "-p", "--path", default=None, multiple=True)
@click.option("excludes", "-x", "--exclude", multiple=True, type=Regex())
@click.option("log_level", "--log-level", default="warning")
@click.pass_obj
def cli(obj, log_level, **flags):
    logging.setup_logging(level=log_level)
    obj.selection = code.Selection(**flags)


@cli.command("graph")
@click.option("with_externals", "-e", "--ext/--no-ext", is_flag=True, default=False)
@click.option(
    "without_independent",
    "-i",
    "--no-independent/--independent",
    is_flag=True,
    default=False,
)
@click.option("cluster", "-c", "--cluster/--no-cluster", is_flag=True, default=False)
@click.pass_obj
def cli_graph(obj, with_externals, without_independent, cluster, **flags):
    """Generate a dot dependecy graph to show rotten packages."""
    analysis = stats.ModuleAnalysis(
        obj.selection,
        with_externals=with_externals,
        without_independent=without_independent,
        cluster=cluster,
    )
    analysis.report()


@cli.command("lost")
@click.pass_obj
def cli_lost(obj):
    """Compare imported packages against installed distributions to find unused ones."""
    analysis = stats.PackageCollector(obj.selection)
    analysis.report()


def main():
    cli(obj=utils.adict())
