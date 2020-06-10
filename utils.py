"""utils to helpout."""

import pandas
from tabulate import tabulate

def csv2markdown(name):
    """convert csv files to markdown."""
    csv_df = pandas.read_csv(name)
    print(tabulate(csv_df))


if __name__ == "__main__":
    print(csv2markdown("./data/ubuntu-pkg-lc.csv"))
    print(csv2markdown("./data/fedora-pkg-lc.csv"))
    print(csv2markdown("./data/pip-pkg-lc.csv"))
    print(csv2markdown("./data/ubuntu-apt-version.csv"))
