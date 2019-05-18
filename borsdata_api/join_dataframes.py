import pandas as pd

def join_dataframes(frames):
    try:
        x = pd.concat(frames, axis=1, sort=True).dropna()
    except ValueError:
        print('No Index Matched the Trend Criteria')
        quit()

    return x

