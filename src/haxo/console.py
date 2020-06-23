"""command line interface to access haxo, version 0.1.0."""
import click

from haxo.pkg_info import runner
from haxo.diff import difference

from . import __version__


@click.group()
@click.version_option(version=__version__)
def cli() -> None:
    """Haxo - look inside a docker image.

    This tool can be used to get information on system packages
    installed in a container image using package managers such
    as apt, dnf, rpm, pip and npm.
    """


@cli.command("apt-licenses")
@click.argument("image", type=str)
@click.option("--format", default="csv", type=str)
@click.option("--license", default="spdx", type=str)
@click.option("--show/--no-show", default=False)
def apt_lic(
    image: str, format: str = "csv", license: str = "spdx", show: bool = False
) -> None:
    """apt packages and licenses info.

    Creates a csv file and saves it to the data directory
    by default with name, license info of dpkg(ubuntu, debian)
    packages in the given image, not all package have licenses
    in the image.

   
    Attributes:
        image: docker image name with tag
        format: save file as csv
        license: license format
        show: show output to screen
    """
    runner(image, pkg_manager="apt-lic", format=format, license=license, show=show)


@cli.command("apt")
@click.argument("image", type=str)
@click.option("--format", default="csv", type=str)
@click.option("--license", default="spdx", type=str)
@click.option("--show/--no-show", default=False)
def apt(image, format="csv", license="spdx", show=False):
    """apt package info.

    Creates a csv file and saves it to the data directory
    by default with name, verson info
    of dpkg(ubuntu, debian) packages in the given image.

    Attributes:
        image: docker image name with tag
        format: save file as csv
        license: license format
        show: show output to screen
    """
    runner(image, pkg_manager="apt", format=format, license=license, show=show)


@cli.command("rpm")
@click.argument("image", type=str)
@click.option("--format", default="csv", type=str)
@click.option("--license", default="spdx", type=str)
@click.option("--show/--no-show", default=False)
def rpm(image, format="csv", license="spdx", show=False):
    """rpm package info.

    Creates a csv file and saves it to the data directory
    by default with name, verson and license info
    of rpm(centos, fedora, redhat) packages in the given image.

    Attributes:
        image: docker image name with tag
        format: save file as csv
        license: license format
        show: show output to screen
    """
    runner(image, pkg_manager="rpm", format=format, license=license, show=show)


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

    Attributes:
        image: docker image name with tag
        format: save file as csv
        license: license format
        show: show output to screen
    """
    runner(image, pkg_manager="pip", format=format, license=license, show=show)


@cli.command("diff")
@click.argument("old", type=str)
@click.argument("new", type=str)
def diff(old, new):
    """find difference between packages in two csv files.

    Designed for output from haxo

    Creates two csv files and saves them to data/diff directory
    by default with csv files concated and appended with 'added'
    and 'removed'.

    Arguments:
        old: str of path to old image csv file
        new: str of path to new image csv file
    """
    difference(old, new)
