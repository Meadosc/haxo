""" Diff tool to find different packages in csv file output by haxo"""

from haxo.utils import csv_to_df, compare_dataframes, save_diff


def difference(old, new, test=False):
    if test:
        return compare_dataframes(old, new)
    else:    
        old_df = csv_to_df(old)
        new_df = csv_to_df(new)
        diff_added, diff_removed = compare_dataframes(old_df, new_df)
        save_diff(diff_added, old_name=old, new_name=new, added=True)
        save_diff(diff_removed, old_name=old, new_name=new, added=False)
