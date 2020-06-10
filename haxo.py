"""entry point script."""
import click
import pandas as pd
import tabulate

from pkg_info import apt_pkgs
from pkg_info import apt_licenses
from pkg_info import npm_pkgs
from pkg_info import pip_pkgs
from pkg_info import rpm_pkgs


@click.group()
def cli():
    """Haxo - look inside a docker image.

    This tool can be used to get information on system packages
    installed in a container image using package managers such
    as apt, dnf, rpm, pip and npm.
    """


@cli.command("pip")
@click.argument("image", type=str)
@click.option("--format", default="csv", type=str)
@click.option("--license", default="spdx", type=str)
@click.option("--show/--no-show", default=False)
def pip(image, format="csv", license="spdx", show=False):
    """pip package info.
    
    Creates a csv file and saves it to the data directory
    by default with name, verson and license info 
    of python packages in the given image.
    """
    fname = "data/pip-pkgs-{}.{}".format(image, format)
    # concurrent futures
    # cache file based on image sha in the pkg_utils script
    # pkgs = pip_pkgs(image)
    # print(pkgs, file=open(fname, "w"))
    headers = ["Package", "Version", "License"]
    if show:
        print(tabulate.tabulate(pd.read_csv(fname), headers=headers))


if __name__ == "__main__":
    cli()
