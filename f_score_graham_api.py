import pandas as pd
import requests

def f_score_graham_api(api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments/kpis/171/last/sum'

    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})

    if str(content) == '<Response [401]>':
        print('Erroneous api key, please enter valid key')
        quit()

    data2 = content.json()['values']

    df = pd.DataFrame(data2)
    df.rename(columns={'n': 'f_score_graham'}, inplace=True)
    df.drop(['s'], axis=1, inplace=True)
    df.set_index('i', inplace=True)

    return df