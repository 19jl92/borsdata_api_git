import pandas as pd
import requests

def roic_api(api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/37/last/latest'

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['values']

    df = pd.DataFrame(data2)
    df.rename(columns={'n': 'roic'}, inplace=True)
    df.drop(['s'], axis=1, inplace=True)
    df.set_index('i', inplace=True)

    return df
