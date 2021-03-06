import pandas as pd
import requests

def profit_growth_kpi_history(api_key, all_stocks_api):
    instruments = all_stocks_api
    key = api_key
    column_name = 'profit'
    url = 'https://apiservice.borsdata.se/v1/Instruments/'
    df_new = pd.DataFrame(columns=['y', 'i', column_name])
    for k in instruments:
        content = requests.get(url + str(k) + '/kpis/56/year/mean/history?authKey=' + key + '&maxcount=20',
                           headers={'content-type': 'application/json'})

        data2 = content.json()['values']
        df = pd.DataFrame(data2)
        if df.empty:
            print('skipping: ' + str(k))
            continue
        df[column_name+"_growth"] = (df['v'] / df['v'].shift(-1)) - 1
        df['i'] = str(k)
        df.rename(columns={'v': column_name}, inplace=True)
        df.dropna(inplace=True)
        df = df[['y', 'i', column_name, column_name+"_growth"]]
        new = [df_new, df]
        df_new = pd.concat(new, sort=False)
    return df_new



