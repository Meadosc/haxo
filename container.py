import os
import re
import subprocess as sps
import shlex as sx
from concurrent.futures import ProcessPoolExecutor as ps_exec
from contextlib import ContextDecorator

from constants import LOGGER
from constants import SPDX
from utils import image_sha_name
from utils import csv2markdown


class Container(ContextDecorator):
    """Container commands and context manager."""

    @staticmethod
    def get_image(name="hylang"):
        """get docker image."""
        cmd = f"docker pull {name}"
        cmd = sx.split(cmd)
        out = sps.run(cmd, stdout=sps.PIPE, shell=False).stdout.decode("utf-8")
        LOGGER.info(out)
        return out.split()[-1]

    @staticmethod
    def deamonize_image(name):
        cmd = f"docker run -dt {name}"
        cmd = sx.split(cmd)
        out = sps.run(cmd, stdout=sps.PIPE, shell=False).stdout.decode("utf-8")
        LOGGER.debug(out)
        return out

    @staticmethod
    def run_docker_cmd(sha_id, cmd):
        """run a command with a image."""
        cmd = f"docker exec -ti {sha_id} {cmd}"
        cmd = sx.split(cmd)
        LOGGER.debug("running command: %s", cmd)
        out = sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")
        LOGGER.debug(out)
        return out

    @staticmethod
    def _stop_container(sha_id):
        """stop a docker container."""
        cmd = f"docker stop {sha_id}"
        cmd = sx.split(cmd)
        LOGGER.debug("running command: %s", cmd)
        sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")

    @staticmethod
    def _remove_container(sha_id):
        """stop a docker container."""
        cmd = f"docker rm {sha_id}"
        cmd = sx.split(cmd)
        LOGGER.debug("running command: %s", cmd)
        sps.run(cmd, shell=False, stdout=sps.PIPE).stdout.decode("utf-8")

    @staticmethod
    def stop_rm_container(sha_id):
        Container._stop_container(sha_id)
        Container._remove_container(sha_id)

    def __init__(self, img_name):
        self.img_name = img_name

    def __enter__(self):
        img = Container.get_image(self.img_name)
        self.sha_id = Container.deamonize_image(img)
        return self.sha_id

    def __exit__(self, *args):
        Container.stop_rm_container(self.sha_id)
