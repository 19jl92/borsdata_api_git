import pandas as pd
import requests
from ebitda_kpi_history import ebita_kpi_history
from profit_growth_kpi_history import profit_growth_kpi_history
def roic_kpi_history(api_key, all_stocks_api):
    instruments = all_stocks_api
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/Instruments/'
    #instruments = [str(803)]
    df_new = pd.DataFrame(columns=['y', 'i', 'roic', 'roic_growth'])
    for k in instruments:
        content = requests.get(url + str(k) + '/kpis/37/year/mean/history?authKey=' + key + '&maxcount=20',
                           headers={'content-type': 'application/json'})

        data2 = content.json()['values']
        df = pd.DataFrame(data2)
        if df.empty:
            print('skipping: ' + str(k))
            continue
        df['roic_growth'] = (df['v'] / df['v'].shift(-1)) - 1
        df['i'] = str(k)
        df.dropna(inplace=True)
        df.rename(columns={'v': 'roic'}, inplace=True)
        df = df[['y', 'i', 'roic', 'roic_growth']]
        new = [df_new, df]
        df_new = pd.concat(new, sort=False)
    return df_new


