import pandas as pd
import requests

def stock_names(api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments'

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['instruments']
    df = pd.DataFrame(data2)
    df = df[['insId', 'urlName', 'ticker']]
    df.rename(columns={'insId': 'i'}, inplace=True)
    df.set_index('i', inplace=True)

    return df