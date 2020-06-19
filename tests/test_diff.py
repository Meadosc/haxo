"""unit tests for src/haxo/diff.py."""

import pandas as pd

from haxo import diff


def test_diff():
    d_old = {'Name': ['test1', 'test2'], 'Version': ['1.2', '3.4'], 'License': ['BSD', 'GCL']}
    d_new = {'Name': ['test1', 'test3'], 'Version': ['1.2', '2.1'], 'License': ['BSD', 'BSD']}
    diff_added, diff_removed = diff('./test1.csv','./test2.csv')
    d_added = {'Name': ['test3'], 'Version': ['2.1'], 'License': ['BSD']}
    d_remov = {'Name': ['test2'], 'Version': ['3.4'], 'License': ['GCL']}
    assert d_added == diff_added
    assert d_remov == diff_removed


if __name__ == '__main__':
    test_diff()

