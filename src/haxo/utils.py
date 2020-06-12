"""utils to helpout."""
import os
import subprocess as sps
import shlex as sx
import pathlib

import pandas
from tabulate import tabulate

from haxo.constants import LOGGER


def mkdirp(path: str) -> bool:
    return pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def csv2markdown(name):
    """convert csv files to markdown."""
    csv_df = pandas.read_csv(name, header=0)
    return tabulate(csv_df, headers="keys", tablefmt="rst")


def image_sha_name(name: str) -> bool:
    """check if docker image exists.

    args
    ----
    name: str - name of the image with tag
    """
    cmd = "docker image list --format '{{.ID}},{{.Repository}}:{{.Tag}}'"
    cmd = sx.split(cmd)
    out = sps.run(cmd, stdout=sps.PIPE, shell=False).stdout.decode("utf-8")
    LOGGER.debug(out)
    out = out[out.find(name) - 12 : out.find(name) + len(name)]
    if not out:
        LOGGER.info("pulling the image %s" % (name))
        cmd = sx.split("docker pull {}".format(name))
        try:
            if sps.run(cmd, stdout=sps.PIPE).stdout:
                image_sha_name(name)
        except Exception as e:
            LOGGER.error(
                "%s not found locally and unable to pull, exiting:  %s" % (name, e)
            )
            exit(1)
    else:
        return out.split(",")


if __name__ == "__main__":
    # print(csv2markdown("./data/ubuntu-pkg-lc.csv"))
    # print(csv2markdown("./data/fedora-pkg-lc.csv"))
    # print(csv2markdown("./data/pip-pkg-lc.csv"))
    # print(csv2markdown("./data/ubuntu-apt-version.csv"))
    # print(image_sha_name("hylang"))
    pass
