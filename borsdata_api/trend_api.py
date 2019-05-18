import pandas as pd
import requests
import time

def trend_api(api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/318/100day/diff'
    url2 = 'https://apiservice.borsdata.se/v1/instruments/kpis/318/20day/diff'


    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    time.sleep(1)
    content2 = requests.get(url2 + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['values']
    data4 = content2.json()['values']

    df = pd.DataFrame(data2)
    df2 = pd.DataFrame(data4)
    df.rename(columns={'n': 'trend1'}, inplace=True)
    df2.rename(columns={'n': 'trend2'}, inplace=True)
    df.drop(['s'], axis=1, inplace=True)
    df2.drop(['s'], axis=1, inplace=True)
    df.set_index('i', inplace=True)
    df2.set_index('i', inplace=True)

    return df, df2
