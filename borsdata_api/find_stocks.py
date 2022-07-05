import pandas as pd
import requests

def find_stocks(stock_isins, api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments'
    content = requests.get(url + '?authKey=' + key,
                               headers={'content-type': 'application/json'})
    if content.status_code == 401:
        print(content.status_code,"Wrong API key")
        exit()
    data2 = content.json()['instruments']
    df = pd.DataFrame(data2)
    df = df[df['isin'].isin(stock_isins)]
    df = df[df['countryId'] == 1]
    df = df[['insId', 'isin', 'name', 'urlName']]
    return df

