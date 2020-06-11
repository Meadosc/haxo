"""entry point script."""
import os

import concurrent.futures
import click
import pandas as pd

from constants import LOGGER
from pkg_info import apt_pkgs
from pkg_info import apt_licenses
from pkg_info import npm_pkgs
from pkg_info import pip_pkgs
from pkg_info import rpm_pkgs
from utils import image_sha_name
from utils import csv2markdown


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
    sha_id, _ = image_sha_name(image)
    fname = "data/apt-lc-pkgs-{}-{}.{}".format(image.split(":")[0], sha_id[:5], format)
    if not os.path.isfile(fname):
        LOGGER.info("metadata not cached, extracting..")
        try:
            pkgs, _ = apt_licenses(image)
        except Exception as exc:
            LOGGER.error("%r generated an exception: %s" % (image, exc))
            exit(1)
        else:
            print(pkgs, file=open(fname, "w"))
    if show:
        print(csv2markdown(fname))


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
    sha_id, _ = image_sha_name(image)
    fname = "data/apt-pkgs-{}-{}.{}".format(image.split(":")[0], sha_id[:5], format)
    if not os.path.isfile(fname):
        LOGGER.info("metadata not cached, extracting..")
        try:
            pkgs, _ = apt_pkgs(image)
        except Exception as exc:
            LOGGER.error("%r generated an exception: %s" % (image, exc))
            exit(1)
        else:
            print(pkgs, file=open(fname, "w"))
    if show:
        print(csv2markdown(fname))


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
    sha_id, _ = image_sha_name(image)
    fname = "data/rpm-pkgs-{}-{}.{}".format(image.split(":")[0], sha_id[:5], format)
    if not os.path.isfile(fname):
        LOGGER.info("metadata not cached, extracting..")
        try:
            pkgs, _ = rpm_pkgs(image)
        except Exception as exc:
            LOGGER.error("%r generated an exception: %s" % (image, exc))
            exit(1)
        else:
            print(pkgs, file=open(fname, "w"))
    if show:
        print(csv2markdown(fname))


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
    sha_id, _ = image_sha_name(image)
    fname = "data/pip-pkgs-{}-{}.{}".format(image.split(":")[0], sha_id[:5], format)
    if not os.path.isfile(fname):
        LOGGER.info("metadata not cached, extracting..")
        try:
            pkgs, _ = pip_pkgs(image)
        except Exception as exc:
            LOGGER.error("%r generated an exception: %s" % (image, exc))
            exit(1)
        else:
            print(pkgs, file=open(fname, "w"))
    if show:
        print(csv2markdown(fname))


if __name__ == "__main__":
    cli()
