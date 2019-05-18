import quandl
import pandas as pd

def quandl_api():
    x = quandl.get("LBMA/GOLD")
    x.rename(columns={'USD (AM)': 'gold'}, inplace=True)
    x.index = x.index.strftime('%Y-%m-%d')
    x = x['gold']
    #print('gold:', x)

    s = quandl.get("LBMA/SILVER")
    s.rename(columns={'USD': 'silver'}, inplace=True)
    s = s['silver']
    s.index = s.index.strftime('%Y-%m-%d')
   

    return x, s
