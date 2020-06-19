"""utils to helpout."""
import os
import pathlib
import shlex as sx
import subprocess as sps

import pandas
from tabulate import tabulate  # noqa:I201
from typing import List, Optional, Any, Union

from haxo.constants import LOGGER  # noqa: I100


def mkdirp(path) -> None:
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def csv2markdown(name: str):
    """convert csv files to markdown."""
    csv_df = pandas.read_csv(name, header=0)
    return tabulate(csv_df, headers="keys", tablefmt="rst")


def image_sha_name(name: str) -> List[str]:
    """check if docker image exists.

    args
    ----
    name: str - name of the image with tag
    """
    cmd: Any = "docker image list --format '{{.ID}},{{.Repository}}:{{.Tag}}'"
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

    return out.split(",")


def csv_to_df(path):
    """wrapper for pandas read_csv"""
    return pandas.read_csv(path)

 
def compare_dataframes(old_df, new_df):
    """ get difference between two dataframes.
    Return the added and removed elements. """
    diff_df = old_df.merge(new_df,how='right',indicator=True)
    df_added = diff_df[diff_df['_merge']=='right_only'].drop(columns='_merge')
    df_removed = diff_df[diff_df['_merge']=='left_only'].drop(columns='_merge')
    return df_added, df_removed


def strip_path(file_path: str):
    """
    strip the path and extension out of a file path

    returns filename (string)
    """
    return os.path.splitext(os.path.basename(file_path))[0]

    
def save_diff(diff_df, old_name, new_name, added=True):
    """
    save the csv that is the difference between two csvs.
    Name the csv with a combination of the old names and
    a label stating whether it represents added packages
    or removed packages.
    """
    name = f"{strip_path(old_name)}_{strip_path(new_name)}"
    if added:
        name = f"{name}_added.csv"
    else:
        name = f"{name}_removed.csv" 
    diff_df.to_csv(f"data/diff/{name}", index=False)


if __name__ == "__main__":
    # print(csv2markdown("./data/ubuntu-pkg-lc.csv"))
    # print(csv2markdown("./data/fedora-pkg-lc.csv"))
    # print(csv2markdown("./data/pip-pkg-lc.csv"))
    # print(csv2markdown("./data/ubuntu-apt-version.csv"))
    # print(image_sha_name("hylang"))
    pass
