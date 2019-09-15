# Python packages
import time
import numpy as np
import datetime
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import mysql_code as mc

# python functions
import data_analysis as gbm
from f_score_graham_api import f_score_graham_api
from roic_api import roic_api
from ebit_growth_api import ebit_growth_api
from magic_rank_api import magic_rank_api
from trend_api import trend_api
from rsi_api import rsi_api
from profit_stability_api import profit_stability_api
from ev_ebit_api import ev_ebit_api
from join_dataframes import join_dataframes
from stock_screener import stock_screener
from stock_names import stock_names
from stock_prices_api import stock_prices_api
from quandl_api import quandl_api
from value_at_risk import value_at_risk
from ebitda_per_share_api import ebitda_per_share
from outstanding_shares import outstanding_shares
import getpass

api_key = getpass.getpass("Input your borsdata api key: ")

# check if user input the key or not
if not api_key:
    print("Missing key, please try again")
    api_key = getpass.getpass("Input your borsdata api key: ")

# capital to invest
Capital = float(input("Capital to invest: "))

# api requests
f_score_graham_dataframe = f_score_graham_api(api_key)
time.sleep(1)
roic_api_dataframe = roic_api(api_key)
time.sleep(1)
ebit_growth_dataframe = ebit_growth_api(api_key)
time.sleep(1)
ev_ebit_dataframe = ev_ebit_api(api_key)
time.sleep(1)
magic_rank_dataframe = magic_rank_api(api_key)
time.sleep(1)
trend_dataframe1, trend_dataframe2 = trend_api(api_key)
time.sleep(1)
rsi_dataframe = rsi_api(api_key)
time.sleep(1)
profit_stability_dataframe = profit_stability_api(api_key)
time.sleep(1)
stock_names_dataframe = stock_names(api_key)
time.sleep(1)
gold_dataframe, silver_dataframe = quandl_api()
time.sleep(1)
ebitda_per_share_dataframe = ebitda_per_share(api_key)
time.sleep(1)
outstanding_shares_dataframe = outstanding_shares(api_key)

frames = [stock_names_dataframe,
          f_score_graham_dataframe,
          roic_api_dataframe,
          ebit_growth_dataframe,
          ev_ebit_dataframe,
          magic_rank_dataframe,
          trend_dataframe1,
          trend_dataframe2,
          rsi_dataframe,
          profit_stability_dataframe,
          ebitda_per_share_dataframe,
          outstanding_shares_dataframe,
          ]

dataframe = join_dataframes(frames)


df = stock_screener(dataframe)

if df.empty:
    print('No stocks mached your criteria')
    exit()
else:
    x = stock_prices_api(df, gold_dataframe, api_key)



stocks = list(x.columns.values)

nr_of_data_series = len(stocks)

x.dropna(inplace=True)

'''-------------------------------------------------------------
  MATPLOTLIB CAN ONLY HANDLE DATETIME FORMATS - CONVERSION CODE
----------------------------------------------------------------'''
x_dates = x.index.values[1:]
x_list = []
for t in range(0, len(x_dates)):
    x_list.append(datetime.datetime.strptime(x_dates[t], '%Y-%m-%d'))
'''-------------------------------------------------------------
                CALCUATING THE RETURNS OF SELECTED STOCKS
----------------------------------------------------------------'''
std = []
mean = []
for index in x.columns:
    x[index] = np.log(x[index] / x[index].shift(1))
    std.append(np.std(x[index])*np.sqrt(252))
    mean.append(np.mean(x[index])*252)

# stock returns dataframe
x = x[1:]
# VaR_array = value_at_risk(x)
# print(VaR_array)

'''-------------------------------------------------------------
                CALCUATING REUSLTS DATAFRAME
----------------------------------------------------------------'''

x = np.array(x)
x_t = np.array(x.T)  # transposed x array.
cov = np.cov(x_t)
corr = np.corrcoef(x_t)

num_of_portfolios = 50000
results = np.zeros((num_of_portfolios, 3))
vikt = np.zeros((num_of_portfolios, nr_of_data_series))

for z in range(num_of_portfolios):
    w = np.random.random(nr_of_data_series)
    w /= np.sum(w)
    k = []
    for r in w:
        k.append(r)

    weights = np.matrix(k)
    portfolio_risk = weights * cov * weights.T
    portfolio_return = float(mean*weights.T)
    portfolio_risk = float(np.sqrt(portfolio_risk) * np.sqrt(252))
    sharp_ratio = float(portfolio_return/portfolio_risk)
    # VaR = VaR_array.T * weights.T

    results[z, 0] = portfolio_return
    results[z, 1] = portfolio_risk
    results[z, 2] = sharp_ratio
    # results[z, 3] = VaR

    vikt[z] = w

'''-------------------------------------------------------------
                        BUILDING RESULT FRAME
----------------------------------------------------------------'''
results_frame = pd.DataFrame(results, columns=['ret', 'stdev', 'sharp'])
max_sharp = results_frame['sharp'].idxmax()
min_std = results_frame['stdev'].idxmin()
results_frame_vikt = pd.DataFrame(vikt, columns=stocks)

'''-------------------------------------------------------------
                        PRINTING RESULT FRAME
----------------------------------------------------------------'''

print("----- MAX SHARP -----  ")
max_sharp_capital = pd.DataFrame()
max_sharp_capital['Weights'] = results_frame_vikt.iloc[max_sharp]
max_sharp_capital['Capital'] = Capital*results_frame_vikt.iloc[max_sharp]
print(max_sharp_capital)

print("----- MAX SHARP RESULTS -----  ")
print(results_frame.iloc[max_sharp])

print("----- MIN VOL -----  ")
min_vol_capital = pd.DataFrame()
min_vol_capital['Weights'] = results_frame_vikt.iloc[min_std]
min_vol_capital['Capital'] = Capital*results_frame_vikt.iloc[min_std]
print(min_vol_capital)

print("----- MIN VOL RESULTS -----  ")
print(results_frame.iloc[min_std])
print('')

#mc.mysql_code(dataframe, df)


'''-------------------------------------------------------------
                        BUILDING TIME SERIES
----------------------------------------------------------------'''
time_series = x * np.matrix(results_frame_vikt.iloc[max_sharp].values).T
time_series_cum = 100 * np.cumprod(np.array(time_series) + 1)

time_series_df = pd.DataFrame(time_series, columns=['returns'])
VaR_max_sharp = value_at_risk(time_series_df)
time_series_df['rea_var'] = 252 * np.cumsum(time_series_df.returns ** 2) / np.arange(len(time_series_df.returns))
time_series_df['rea_vol'] = np.sqrt(time_series_df.rea_var)

time_series_min_vol = x * np.matrix(results_frame_vikt.iloc[min_std].values).T
time_series_cum_min_vol = 100 * np.cumprod(np.array(time_series_min_vol) + 1)
time_series_min_vol_df = pd.DataFrame(time_series_min_vol, columns=['returns'])
VaR_min_vol = value_at_risk(time_series_min_vol_df)

print("----- MAX SHARP VaR -----  ")
print(pd.DataFrame(VaR_max_sharp))
print("----- MIN VOL VaR -----  ")
print(pd.DataFrame(VaR_min_vol))
print('')



'''-------------------------------------------------------------
                        BUILDING NORMAL CURVE
----------------------------------------------------------------'''
y = [pd.Series(np.random.normal(np.mean(time_series), np.std(time_series), len(time_series))), time_series]
sns.distplot(y[0]*100, label='Normal Curve', hist=True, kde=True, bins=100,
             hist_kws={'edgecolor': 'red', 'color': 'red'},
             kde_kws={'shade': True, 'color': 'red', 'linewidth': 0.5})
sns.distplot(y[1]*100, label='MAX Curve', hist=True, kde=True, bins=100,
             hist_kws={'edgecolor': 'blue', 'color': 'blue'},
             kde_kws={'shade': True, 'color': 'blue', 'linewidth': 0.5})
plt.legend()

'''-------------------------------------------------------------
                    PLOT HISTORICAL PERFORMANCE
----------------------------------------------------------------'''
plt.figure(figsize=(9, 5))
plt.title('MAX SHARP')
plt.plot(x_list, time_series_cum, label='MaxSharp', color='r', lw=0.8)
plt.plot(x_list, time_series_cum_min_vol, label='MIN VOL', color='b', lw=0.8)
plt.axhline(time_series_cum[-1], ls='--', color='r', lw=0.5)
plt.axhline(time_series_cum_min_vol[-1], color='b', ls='--', lw=0.5)
plt.xlabel('Dates')
plt.ylabel('')
plt.gcf().autofmt_xdate()
plt.grid(color='w', lw=0.4)
plt.legend(loc=0)

'''-------------------------------------------------------------
                        PLOT SCATTER PLOT
----------------------------------------------------------------'''
plt.figure(figsize=(9, 5))
plt.scatter(results_frame.stdev, results_frame.ret, c=results_frame.sharp, cmap='hsv')
plt.grid(color='w', lw=0.4)
plt.colorbar()
plt.show()

'''-------------------------------------------------------------
                        PLOT SCATTER PLOT
----------------------------------------------------------------'''
#gbm.print_statistics(time_series_df)
gbm.return_qqplot(time_series_df)
gbm.rolling_statistics(time_series_df)
gbm.count_jumpes(time_series_df, 0.02)

'''-------------------------------------------------------------
                            THE END
----------------------------------------------------------------'''
