import pandas as pd

def merge_history_kpis(list_of_dataframes):
    merged_df = list_of_dataframes[0]
    x = 0
    for i in list_of_dataframes:
        if x == 0:
            pass
        else:
            merged_df = merged_df.merge(i, left_on=['y', 'i'], right_on=['y', 'i'])
        x += 1

    return merged_df
