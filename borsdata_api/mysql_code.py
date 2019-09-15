from sqlalchemy import create_engine
import pymysql
from config import borsdata_db_pw
import datetime as dt


def mysql_code(dataframe, df):
    dataframe['date'] = dt.date.today().strftime("%Y-%m-%d")
    df['date'] = dt.date.today().strftime("%Y-%m-%d")

    engine = create_engine("mysql+pymysql://root:"+borsdata_db_pw+"@127.0.0.1:3306/borsdata")
    engine.connect()

    dataframe.to_sql(name='borsdata_stocks',
                     con=engine,
                     index=True,
                     if_exists='append')

    df.to_sql(name='borsdata_screened_stocks_kpi',
              con=engine,
              index=True,
              if_exists='append')
    return
