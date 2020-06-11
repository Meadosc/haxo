import os
import re
import subprocess as sps
import shlex as sx
from concurrent.futures import ProcessPoolExecutor as ps_exec

from container import Container
from constants import LOGGER
from constants import SPDX
from utils import image_sha_name
from utils import csv2markdown


def pip_pkgs(img_name):
    """get python packages installed in an image."""
    with Container(img_name) as sha_id:
        Container.run_docker_cmd(sha_id, "pip install pip-licenses")
        pkgs = Container.run_docker_cmd(sha_id, "pip-licenses -f=csv --from=mixed")
    return pkgs, sha_id


def rpm_pkgs(img_name):
    """get rpm packages installed in an image."""
    with Container(img_name) as sha_id:
        pkgs = "Package,Version,License\n"
        pkgs += Container.run_docker_cmd(
            sha_id, "rpm -qa --qf '%{NAME},%{VERSION},%{LICENSE}\n'"
        )
    return pkgs, sha_id


def apt_pkgs(img_name):
    """get apt packages installed in an image."""
    with Container(img_name) as sha_id:
        cmd = "dpkg-query -Wf '${Package},${Version},${Source}\n'"
        pkgs = "Package,Version,Source\n"
        pkgs += Container.run_docker_cmd(sha_id, cmd)
    return pkgs, sha_id


def _search_spdx(string):
    lcs = []
    tricky = ["GPL", "LGPL", "BSD"]
    for lc in SPDX:
        if lc in string:
            lcs.append(lc)
    for t in tricky:
        for l in lcs:
            if l.startswith(t) and t in lcs and l != t:
                lcs.remove(t)
    return ";".join(lcs)


def apt_licenses(img_name):
    """get licenses of apt pkgs from an image."""
    pkg_lcs = {}
    with Container(img_name) as sha_id:
        cmd = "bash -c \"for pkg in `dpkg-query -Wf '${Package}\n'`; do lc=`cat /usr/share/doc/$pkg/copyright 2>/dev/null`; echo PKG_START $pkg PKG_END,LFILE_START $lc LFILE_END; done\""
        pkgs = Container.run_docker_cmd(sha_id, cmd)
    pkg = re.findall("PKG_START(.*?)PKG_END", pkgs)
    license = re.findall("LFILE_START(.*?)LFILE_END", pkgs)
    pkg_lcs = {p.strip(): _search_spdx(v.strip()) for p, v in zip(pkg, license)}
    pkgs = "Package,License\n"
    for pkg, lc in pkg_lcs.items():
        pkgs += "{0},{1}\n".format(pkg, lc)
    return pkgs, sha_id


def npm_pkgs(image_name):
    """get node packages installed in an image."""
    # TODO(unrahul): npm list -g --json=true and parse
    pass


def runner(image, pkg_manager, format="csv", license="spdx", show=False):
    """universal runnner to extract metadata based on the pkg_manager.

    Creates a csv(default format) file and saves it to the data directory

    params
    ------
    image: str - docker image name with tag
    pkg_manager: str - which pkg manager to use - apt, pip, rpm, npm
    format: str - save file as csv
    license: str - license format
    show: bool - show output to screen
    """
    run_method = {
        "apt-lic": apt_licenses,
        "rpm": rpm_pkgs,
        "pip": pip_pkgs,
        "apt": apt_pkgs,
        "npm": npm_pkgs,
    }
    try:
        sha_id, _ = image_sha_name(image)
    except TypeError as exc:
        LOGGER.error("%r generated an exception: %s" % (image, exc))
        sha_id, _ = image_sha_name(image)
    fname = "data/{}-pkgs-{}-{}.{}".format(
        pkg_manager, image.split(":")[0].split("/")[-1], sha_id[:5], format
    )
    LOGGER.debug("to be saved as %s " % (fname))
    if not os.path.isfile(fname):
        LOGGER.info("metadata not cached, extracting..")
        with ps_exec(max_workers=10) as executor:
            try:
                future = executor.submit(run_method[pkg_manager], image)
                pkgs, _ = future.result()
                LOGGER.info("done!")
            except Exception as exc:
                LOGGER.error("%r generated an exception: %s" % (image, exc))
                exit(1)
            else:
                try:
                    print(pkgs, file=open(fname, "w"))
                except FileNotFoundError as exc:
                    LOGGER.error("generated an exception: %s" % (exc))
    if show:
        try:
            print(csv2markdown(fname))
        except FileNotFoundError as exc:
            LOGGER.error("generated an exception: %s" % (exc))


if __name__ == "__main__":
    print(pip_pkgs("hylang"), file=open("data/pip-pkg-lc.csv", "w"))
    print(rpm_pkgs("fedora"), file=open("data/fedora-pkg-lc.csv", "w"))
    print(apt_pkgs("ubuntu"), file=open("data/ubuntu-apt-version.csv", "w"))
    print(apt_licenses("ubuntu"), file=open("data/ubuntu-pkg-lc.csv", "w"))
