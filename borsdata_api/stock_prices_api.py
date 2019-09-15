import pandas as pd
import requests
import time
from join_dataframes import join_dataframes
from trend_function import trend_function
from adx import adx_function

def stock_prices_api(dataframe, gold, api_key):
    key = api_key
    url = 'https://apiservice.borsdata.se/v1/instruments/'

    stock_list = []
    df = pd.DataFrame()
    for x in dataframe.values:
        content = requests.get(url + str(x[0]) + '/stockprices' + '?authKey=' + key,
                           headers={'content-type': 'application/json'}).json()['stockPricesList']
        time.sleep(1)
        prices = pd.DataFrame(content)
        #prices = adx_function(prices)
        #prices = prices[['d', 'c','PDIs', 'NDIs', 'ADX']]
        prices = prices[['d', 'c']]
        prices.rename(columns={'d': 'date', 'c': x[1]}, inplace=True)
        prices.set_index('date', inplace=True)
        #print(prices)
        prices = prices[~prices.index.duplicated(keep='first')]
        stock_list.append(prices)

    if gold.empty:
        pass
    else:
        stock_list.append(gold)

    stock_dataframe = pd.concat(stock_list, axis=1, sort=True)


    return stock_dataframe