"""utils to helpout."""
import os
import subprocess as sps
import shlex as sx

import pandas
from tabulate import tabulate

from constants import LOGGER


def csv2markdown(name):
    """convert csv files to markdown."""
    csv_df = pandas.read_csv(name, header=0)
    return tabulate(csv_df, headers="keys", tablefmt="rst")


def image_sha_name(name: str) -> bool:
    """check if dockerfile exists.

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
        cmd = "docker pull {}".format(name)
        cmd = sx.split(cmd)
        if sps.run(cmd, stdout=sps.PIPE, shell=False).stdout:
            image_sha_name(name)
        else:
            LOGGER.error("Image not found locally and unable to pull %s" % (name))
            exit(1)
    return out.split(",")


if __name__ == "__main__":
    # print(csv2markdown("./data/ubuntu-pkg-lc.csv"))
    # print(csv2markdown("./data/fedora-pkg-lc.csv"))
    # print(csv2markdown("./data/pip-pkg-lc.csv"))
    # print(csv2markdown("./data/ubuntu-apt-version.csv"))
    # print(image_sha_name("hylang"))
    pass
