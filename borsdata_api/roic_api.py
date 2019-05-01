import pandas as pd
import requests

def roic_api():
    key = 'c0a2f9c9d5e04dd3aabe6395d3c03a1d'
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/37/last/latest'

    # "https://apiservice.borsdata.se/v1/instruments/97/stockprices?
    # authKey=c0a2f9c9d5e04dd3aabe6395d3c03a1d&from=2018-01-01&to=2019-01-01"

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['values']

    df = pd.DataFrame(data2)
    df.rename(columns={'n': 'roic'}, inplace=True)
    df.drop(['s'], axis=1, inplace=True)
    df.set_index('i', inplace=True)

    return df
