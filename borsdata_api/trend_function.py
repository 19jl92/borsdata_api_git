''' TREND FUNCTION '''

import pandas as pd

def trend_function(lista):
    lista_trend = []
    for i in range(len(lista)):
        temp_lista = []
        temp_lista.append(lista[i])
        #lista[i].columns.values[0]
        rolling_200 = lista[i].rolling(200).mean().dropna()
        rolling_200 = rolling_200.rename(columns={rolling_200.columns.values[0]: '200'})
        temp_lista.append(rolling_200)
        rolling_50 = lista[i].rolling(50).mean().dropna()
        rolling_50 = rolling_50.rename(columns={rolling_50.columns.values[0]: '50'})
        temp_lista.append(rolling_50)
        temp = pd.concat(temp_lista, axis=1, sort=True).dropna()
        if float(temp[lista[i].columns.values[0]][-1:]) > float(temp['200'][-1:]):
            #if float(temp['50'][-1:]) > float(temp['200'][-1:]):
            lista_trend.append(lista[i])

    return lista_trend