"""functional tests for pkg_info."""

from haxo import pkg_info


def fake_subprocess_run():
    class Return:
        def __init__(*args, **kwargs):
            pass

        stdout = b"[samplepkg]"

    return Return


def test_rpm_pkgs(monkeypatch):
    """test rpm lister."""

    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    pkgs, _ = pkg_info.rpm_pkgs("fedora:31")
    assert pkgs.split("\n")[0] == "Package,Version,License"


def test_apt_pkgs(monkeypatch):
    """test apt lister."""

    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    pkgs, _ = pkg_info.apt_pkgs("debian")
    assert pkgs.split("\n")[0] == "Package,Version,Source"


def test_apt_license_pkgs(monkeypatch):
    """test apt license lister."""

    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    pkgs, _ = pkg_info.apt_licenses("debian")
    assert pkgs.split("\n")[0] == "Package,License"


def test_pip_pkgs(monkeypatch):
    """test apt lister."""

    monkeypatch.setattr("subprocess.run", fake_subprocess_run())
    pkgs, _ = pkg_info.pip_pkgs("hylang")
    assert pkgs.split("\n")[0] == "[samplepkg]"
