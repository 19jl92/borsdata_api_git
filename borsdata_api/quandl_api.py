import quandl
import pandas as pd


def quandl_api():
    try:
        x = quandl.get("LBMA/GOLD")
        x.rename(columns={'USD (AM)': 'gold'}, inplace=True)
        x.index = x.index.strftime('%Y-%m-%d')
        x = x['gold']
        s = quandl.get("LBMA/SILVER")
        s.rename(columns={'USD': 'silver'}, inplace=True)
        s = s['silver']
        s.index = s.index.strftime('%Y-%m-%d')
    except quandl.errors.quandl_error.LimitExceededError as e:
        print('error: {}'.format(str(e)))
        return pd.DataFrame(), pd.DataFrame()

    return x, s
