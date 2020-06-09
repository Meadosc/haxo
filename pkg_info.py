import logging
import os
import subprocess as sps
import shlex as sx

log_format = "%(filename)s: %(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_image(name="hylang"):
    """get docker image."""
    cmd = f"docker pull {name}"
    cmd = sx.split(cmd)
    out = sps.run(cmd, stdout=sps.PIPE, shell=False).stdout.decode("utf-8")
    logger.debug(out)
    return out.split()[-1].split("/")[-1]


def deamonize_image(name):
    cmd = f"docker run -dt {name}"
    cmd = sx.split(cmd)
    out = sps.run(cmd, stdout=sps.PIPE, shell=False).stdout.decode("utf-8")
    logger.debug(out)
    return out


def run_docker_cmd(sha_id, cmd):
    """run a command with a image."""
    cmd = f"docker exec -ti {sha_id} {cmd}"
    cmd = sx.split(cmd)
    logger.debug("running command: %s", cmd)
    out = sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")
    logger.debug(out)
    return out


def _stop_container(sha_id):
    """stop a docker container."""
    cmd = f"docker stop {sha_id}"
    cmd = sx.split(cmd)
    logger.debug("running command: %s", cmd)
    sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")


def _remove_container(sha_id):
    """stop a docker container."""
    cmd = f"docker rm {sha_id}"
    cmd = sx.split(cmd)
    logger.debug("running command: %s", cmd)
    sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")


def stop_rm_container(sha_id):
    _stop_container(sha_id)
    _remove_container(sha_id)


def pip_pkgs(img_name):
    """get python packages installed in an image."""
    img = get_image(img_name)
    sha_id = deamonize_image(img)
    run_docker_cmd(sha_id, "pip install pip-licenses")
    pkgs = run_docker_cmd(sha_id, "pip-licenses -f=csv --from=mixed")
    stop_rm_container(sha_id)
    return pkgs


def rpm_pkgs(img_name):
    """get rpm packages installed in an image."""
    img = get_image(img_name)
    sha_id = deamonize_image(img)
    pkgs = "Package,Version,License\n"
    pkgs += run_docker_cmd(sha_id, "rpm -qa --qf '%{NAME},%{VERSION},%{LICENSE}\n'")
    stop_rm_container(sha_id)
    return pkgs


def apt_pkgs(img_name):
    """get apt packages installed in an image."""
    img = get_image(img_name)
    sha_id = deamonize_image(img)
    cmd = "dpkg-query -Wf '${Package},${Version},${Source}\n'"
    pkgs = "Package,Version,Source\n"
    pkgs += run_docker_cmd(sha_id, cmd)
    stop_rm_container(sha_id)
    return pkgs


def apt_licenses(img_name):
    """get licenses of apt pkgs from an image."""
    img = get_image(img_name)
    sha_id = deamonize_image(img)
    cmd = 'bash -c "for pkg in `dpkg-query -Wf \'${Package}\n\'`; do lc=`cat /usr/share/doc/$pkg/copyright 2>/dev/null`; echo $pkg,LFILE: $lc; done"'
    pkgs = "Package,License\n"
    pkgs += run_docker_cmd(sha_id, cmd)
    stop_rm_container(sha_id)
    return pkgs

def npm_pkgs(image_name):
    """get node packages installed in an image."""
    #TODO(unrahul): npm list -g --json=true and parse
    pass

if __name__ == "__main__":
    print(pip_pkgs("hylang"), file=open("hylang-pip.csv", "w"))
    print(rpm_pkgs("fedora"), file=open("fedora-rpm.csv", "w"))
    print(apt_pkgs("ubuntu"), file=open("ubuntu-apt.csv", "w"))
    print(apt_licenses("ubuntu") , file=open("ubuntu-apt-lc.csv", "w"))
