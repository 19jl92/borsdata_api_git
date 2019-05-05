import pandas as pd
import requests
import time

def trend_api():
    key = 'c0a2f9c9d5e04dd3aabe6395d3c03a1d'
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/318/100day/diff'
    url2 = 'https://apiservice.borsdata.se/v1/instruments/kpis/318/20day/diff'


    # "https://apiservice.borsdata.se/v1/instruments/97/stockprices?
    # authKey=c0a2f9c9d5e04dd3aabe6395d3c03a1d&from=2018-01-01&to=2019-01-01"

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
