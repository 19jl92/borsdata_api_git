import pandas as pd
import quandl
import numpy as np
#x = {'col1': [1, 2], 'col2': [3, 4]}
#df = pd.DataFrame(x)
#print(df.shift(1))
#print(list(df.columns.values))

#b = quandl.get("LBMA/SILVER")

#print(b)
#weights = np.exp(np.linspace(-1,0,14))
#print(weights, sum(weights))
#weights /= weights.sum()
#x = sum(weights)
#print(weights, x)


import pandas as pd
import requests


key = 'c0a2f9c9d5e04dd3aabe6395d3c03a1d2'
url = 'https://apiservice.borsdata.se//v1/Instruments/77/kpis/17/r12/mean/history'

# "https://apiservice.borsdata.se/v1/instruments/97/stockprices?

content = requests.get(url + '?authKey=' + key,
                       headers={'content-type': 'application/json'})

if str(content) == '<Response [401]>':
    print('Erroneous api key, please enter valid key')
    quit()

#data2 = content.json()['values']
#for x in data2:
#    print(x['v'])




