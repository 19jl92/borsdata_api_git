import pandas as pd
from ebitda_kpi_history import ebita_kpi_history
from profit_growth_kpi_history import profit_growth_kpi_history
from roic_kpi_history import roic_kpi_history
from outstanding_shares_history import outstanding_shares_history
from merge_history_kpis import merge_history_kpis
from all_stocks_api import all_stocks_api


api_key = input('api_key:')
all_stocks_api = all_stocks_api(api_key)
ebita_kpi_history = ebita_kpi_history(api_key, all_stocks_api)
profit_growth_kpi_history = profit_growth_kpi_history(api_key, all_stocks_api)
roic_kpi_history = roic_kpi_history(api_key, all_stocks_api)
outstanding_shares_history = outstanding_shares_history(api_key, all_stocks_api)
list_of_dataframes = [ebita_kpi_history, profit_growth_kpi_history, roic_kpi_history, outstanding_shares_history]
merge_history_kpis = merge_history_kpis(list_of_dataframes)
print(merge_history_kpis.sort_values(['y'], ascending=False))
merge_history_kpis.to_csv('test.csv', sep=',', index=False)
