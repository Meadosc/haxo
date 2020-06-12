"""unit tests for src/haxo/utils.py."""

from haxo import utils


def test_image_sha_name():
    output = ["dfbfa4a115a", "fedora:31"]
    out = utils.image_sha_name("fedora:31")
    out = utils.image_sha_name("fedora:31")
    assert output == out
