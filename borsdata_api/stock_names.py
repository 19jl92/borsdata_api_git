import pandas as pd
import requests

def stock_names():
    key = 'c0a2f9c9d5e04dd3aabe6395d3c03a1d'
    url = 'https://apiservice.borsdata.se/v1/instruments'

    # "https://apiservice.borsdata.se/v1/instruments/97/stockprices?
    # authKey=c0a2f9c9d5e04dd3aabe6395d3c03a1d&from=2018-01-01&to=2019-01-01"

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['instruments']
    df = pd.DataFrame(data2)
    df = df[['insId', 'urlName', 'ticker']]
    df.rename(columns={'insId': 'i'}, inplace=True)
    df.set_index('i', inplace=True)

    return df