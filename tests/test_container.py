"""functional tests for container.py"""

from haxo.container import Container


class Img:
    sha = None
    name = "fedora:31"
    full_name = "docker.io/library/fedora:31"


def test_get_image():
    """test get image."""
    img_name = Container.get_image(Img.name)
    assert img_name == Img.full_name


def test_deamonize_image():
    """test deamonize image."""
    out = Container.deamonize_image("fedora:31")
    Img.sha = out
    assert out != ""


def test_stop_rm_container():
    assert Container.stop_rm_container(Img.sha) == ""
