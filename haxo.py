"""entry point script."""
import click

from pkg_info import runner


@click.group()
def cli():
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
def apt_lic(image, format="csv", license="spdx", show=False):
    """apt packages and licenses info.
    
    Creates a csv file and saves it to the data directory
    by default with name, license info of dpkg(ubuntu, debian) 
    packages in the given image, not all package have licenses
    in the image.

    params
    ------
    image: str - docker image name with tag
    format: str - save file as csv
    license: str - license format
    show: bool - show output to screen
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

    params
    ------
    image: str - docker image name with tag
    format: str - save file as csv
    license: str - license format
    show: bool - show output to screen
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

    params
    ------
    image: str - docker image name with tag
    format: str - save file as csv
    license: str - license format
    show: bool - show output to screen
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

    params
    ------
    image: str - docker image name with tag
    format: str - save file as csv
    license: str - license format
    show: bool - show output to screen
    """
    runner(image, pkg_manager="pip", format=format, license=license, show=show)


if __name__ == "__main__":
    cli()
