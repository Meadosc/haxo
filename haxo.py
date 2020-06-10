"""entry point script."""
import click
import tabulate

import pkg_info


@cli.group()
def cli():
    """Haxo - look inside a docker image.

    This tool can be used to get information on system packages
    installed in a container image using package managers such
    as apt, dnf, rpm, pip and npm.
    """
