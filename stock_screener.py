

def stock_screener(dataframe):

    # f_score_graham > 10
    dataframe = dataframe[dataframe['f_score_graham'] >= int(10)]

    # profit stability over the last 10 year = 10
    dataframe = dataframe[dataframe['profit_stability'] >= int(10)]

    # roic equal or above 10 percent
    dataframe = dataframe[dataframe['roic'] >= int(10)]

    # positive ebit growth
    dataframe = dataframe[dataframe['ebit_growth'] >= int(0)]

    # sanity check on 0 < EV/EBIT < 50
    dataframe = dataframe[(dataframe['ev_ebit'] < int(50)) & (dataframe['ev_ebit'] > int(5))]

    # stock in a positive trend? pric/ma100
    dataframe = dataframe[(dataframe['trend1'] >= int(0)) & (dataframe['trend1'] <= int(10))]

    # stock in a positive trend? pric/ma20
    dataframe = dataframe[(dataframe['trend2'] >= int(0)) & (dataframe['trend2'] <= int(10))]

    # profit stability over the last 10 year = 10
    dataframe = dataframe[(dataframe['rsi'] >= int(10)) & (dataframe['rsi'] <= int(60))]

    # ebitda per share data frame > 0 equal to YoY growth
    dataframe = dataframe[(dataframe['ebitda_per_share'] >= int(0))]

    dataframe.sort_values('magic_rank', ascending=True, inplace=True)
    dataframe.reset_index(inplace=True)


    return dataframe
