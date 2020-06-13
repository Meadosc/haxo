"""functional tests for pkg_info."""

from haxo import pkg_info


def test_rpm_pkgs():
    """test rpm lister."""
    pkgs, _ = pkg_info.rpm_pkgs("fedora:31")
    assert pkgs.split("\n") == ["Package,Version,License", ""]
