import pandas as pd
import requests
import numpy as np

def adx_function(prices):

    def TrueRange(prices):
        # TruRange is the greates of below
        x = prices['h']-prices['l'] # panda series
        y = abs(prices['h']-prices['c'].shift(1))
        z = abs(prices['l']-prices['c'].shift(1))

        TR = [] # first comparison hits else
        for i in range(len(prices)):
            if y.iloc[i] <= x.iloc[i] >= z.iloc[i]:
                TR.append(x.iloc[i])
            elif x.iloc[i] <= y.iloc[i] >= z.iloc[i]:
                TR.append(y.iloc[i])
            elif x.iloc[i] <= z.iloc[i] >= z.iloc[i]:
                TR.append(z.iloc[i])
            else: TR.append(float(0))

        prices['TR'] = pd.Series(TR)
        
        return prices 

    def DM(prices):
        moveUp = prices['h']-prices['h'].shift(1)
        moveDown = prices['l'].shift(1)-prices['l']
        PDM = [0]
        NDM = [0]
        for i in range(len(prices)):
            if 0 < moveUp.iloc[i] > moveDown.iloc[i]:
                PDM.append(moveUp.iloc[i])
            else: 
                PDM.append(float(0))
            if 0 < moveDown.iloc[i] >moveUp.iloc[i]:
                NDM.append(moveDown.iloc[i])
            else:
                NDM.append(float(0))

        prices['PDM'] = pd.Series(PDM)
        prices['NDM'] = pd.Series(NDM)
        
        return prices

    def EWMA(prices):
        window = 14
        weights = np.exp(np.linspace(-1.0,0,window))
        weights /= weights.sum()
        PDM_convolve = np.convolve(prices['PDM'], weights)[:len(prices['PDM'])]
        prices['PDM_convolve'] = pd.Series(PDM_convolve)
        NDM_convolve = np.convolve(prices['NDM'], weights)[:len(prices['NDM'])]
        prices['NDM_convolve'] = pd.Series(NDM_convolve)
        TR_convolve = np.convolve(prices['TR'], weights)[:len(prices['TR'])]
        prices['TR_convolve'] = pd.Series(TR_convolve)

        return prices

    def PDIs_NDIs(prices):
        PDIs = []
        NDIs = []
        for i in range(len(prices)):
            if prices['TR_convolve'].iloc[i] == 0:
                PDIs.append(0)
                NDIs.append(0)
            else: 
                p = 100*(prices['PDM_convolve'].iloc[i]/prices['TR_convolve'].iloc[i])
                PDIs.append(p)
                n = 100*(prices['NDM_convolve'].iloc[i]/prices['TR_convolve'].iloc[i])
                NDIs.append(n)
        prices['PDIs'] = pd.Series(PDIs)
        prices['NDIs'] = pd.Series(NDIs)
        return prices

    def ADX(prices):
        ADX = []
        for i in range(len(prices)):
            a = 100 * ((abs(prices['PDIs'].iloc[i]-prices['NDIs'].iloc[i])/(prices['PDIs'].iloc[i]+prices['NDIs'].iloc[i])))
            ADX.append(a)
        window = 14
        weights = np.exp(np.linspace(-1.0,0,window))
        weights /= weights.sum()
        prices['ADX_convolve'] = pd.Series(ADX)
        ADX_convolve = np.convolve(prices['ADX_convolve'], weights)[:len(prices['ADX_convolve'])] 
        prices['ADX'] = pd.Series(ADX_convolve)
        return prices


    prices = TrueRange(prices)
    prices = DM(prices)
    prices = EWMA(prices)
    prices = PDIs_NDIs(prices)
    prices = ADX(prices)
    prices.drop(['PDM', 'NDM', 'PDM_convolve', 'NDM_convolve','TR_convolve', 'ADX_convolve'], axis=1)
    
    return prices
