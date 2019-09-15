import pandas as pd
import requests

def ebitda_per_share(api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/54/last/quarter'

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    data2 = content.json()['values']

    df = pd.DataFrame(data2)
    df.rename(columns={'n': 'ebitda_per_share'}, inplace=True)
    df.drop(['s'], axis=1, inplace=True)
    df.set_index('i', inplace=True)

    return df
