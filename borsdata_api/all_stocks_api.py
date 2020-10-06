import pandas as pd
import requests

def all_stocks_api(api_key):
    key = api_key
    list_of_stocks= []
    url = 'https://apiservice.borsdata.se/v1/instruments'
    content = requests.get(url + '?authKey=' + key,
                           headers={'content-type': 'application/json'})
    data2 = content.json()['instruments']
    df = pd.DataFrame(data2)
    df.drop_duplicates(keep='first', inplace=True)
    df = df[['insId', 'urlName']]
    list_of_stocks = df['insId'].tolist()
    return list_of_stocks
