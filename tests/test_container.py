"""functional tests for container.py"""

from haxo.container import Container


def fake_subprocess_run():
    class Return:
        def __init__(*args, **kwargs):
            pass

        stdout = b"42"

    return Return


class Img:
    sha = "42"
    name = "fedora:31"
    full_name = "docker.io/library/fedora:31"
    output = "42"
    cmd = "cmd"


def test_get_image(monkeypatch):
    """test get image."""
    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    img_sha = Container.get_image(Img.name)
    assert img_sha == Img.sha


def test_deamonize_image(monkeypatch):
    """test deamonize image."""
    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    out = Container.deamonize_image(Img.name)
    assert out == Img.sha


def test_stop_rm_container(monkeypatch):
    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    assert Container.stop_rm_container(Img.sha) is None


def test_run_docker_cmd(monkeypatch):
    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    out = Container.run_docker_cmd(Img.sha, Img.cmd)
    assert out == Img.output
