import numpy as np
from scipy import stats as scs
import statsmodels.api as sm
import matplotlib.pyplot as plt


def print_statistics(data):
    print("RETURN SAMPLE STATISTICS")
    print("-------------------------------------------------------------")
    print("Mean of Daily Log Retunrs   %9.6f", np.mean(data.returns))
    print("Std  of Daily Log Returns   %9.6f", np.std(data.returns))
    print("Mean of Annua. Log Returns  %9.6f", np.mean(data.returns) * 252)
    print("Std  of Annua. Log Returns  %9.6f", np.std(data.returns) * np.sqrt(252))
    print("-------------------------------------------------------------")
    print("Skew of sample Log Returns  %9.6f", scs.skew(data.returns))
    print("Skew Normal Test p-value    %9.6f", scs.skewtest(data.returns)[1])
    print("-------------------------------------------------------------")
    print("Kurt of Sample Log Returns  %9.6f", scs.kurtosis(data.returns))
    print("Kurt Normal Test p-value    %9.6f", scs.kurtosistest(data.returns)[1])
    print("-------------------------------------------------------------")
    print("Normal Test p-value         %9.6f", scs.normaltest(data.returns)[1])
    print("-------------------------------------------------------------")
    print("Realized Volatility         %9.6f", data.rea_vol.iloc[-1]) # -1 everything but the last number in series.
    print("Realized Variance           %9.6f", data.rea_var.iloc[-1]) # -1 everything but the last number in series.


##Graphical Output#

# daily quotes and log returns
def quotes_returns(data):
    ''' Plots quotes and returns. '''
    plt.figure(figsize=(9, 6))
    plt.subplot(211)
    data['index'].plot()
    plt.ylabel('daily quotes')
    plt.grid(True)
    plt.axis('tight')

    plt.subplot(212)
    data.returns.plot()
    #print(data.returns)
    plt.ylabel('daily log returns')
    plt.grid(True)
    plt.axis('tight')
    plt.show()

# Q-Q plot of annulized daily log returns
def return_qqplot(data):
    ''' Generates a Q-Q plot of returns. '''
    #plt.figure(figsize=(9, 5))
    sm.qqplot(data.returns, line='s')
    plt.grid(True)
    plt.xlabel('Theoretical quantiles')
    plt.ylabel('sample quantiles')
    plt.title('Max Sharp quantiles')
    plt.show()

# mean_return, vol, and correlation (252 days moving = 1 year)
def rolling_statistics(data):
    ''' Calculates and plots rolling statistics (mean, std, correlation) '''
    plt.figure(figsize=(11, 8))

    plt.subplot(211)
    mr = data.returns.rolling(252).mean()
    mr.plot()
    plt.grid(True)
    plt.ylabel('returns (252d)')
    plt.axhline(mr.mean(), color='r', ls='dashed', lw=1.5)
    plt.title('rolling statistics returns')

    plt.subplot(212)
    vo = data.returns.rolling(252).std()
    vo.plot()
    plt.grid(True)
    plt.ylabel('volatility (252d)')
    plt.axhline(vo.mean(), color='r', ls='dashed', lw=1.5)
    plt.title('rolling statistics vol')

    plt.show()

def count_jumpes(data, value):
    ''' Countes the number of return jumps as defined in size by value. '''
    jumps = np.sum(np.abs(data.returns) > value)
    line = "-------------------------------------------------------------"
    return print(line), print('# of jumps: ', jumps)
