
import tushare as ts
import pandas as pd
import datetime
import logging
from stock_choice import settings
import talib as tl

from stock_choice import utils

import concurrent.futures

from pandas.tseries.offsets import *


# def update_data(code_name):
#     stock = code_name[0]
#     old_data = utils.read_data(code_name)
#     if not old_data.empty:
#         start_time = utils.next_weekday(old_data.iloc[-1].date_day)
#         current_time = datetime.datetime.now()
#         if start_time > current_time:
#             return
#
#         df = ts.get_k_data(stock, autype='qfq')
#         mask = (df['date_day'] >= start_time.strftime('%Y-%m-%d'))
#         appender = df.loc[mask]
#         if appender.empty:
#             return
#         else:
#             return appender
from tools.sqlite_handle import SqliteDB


def init_data(code_name):
    stock = code_name[0]
    data = ts.get_k_data(stock, autype='qfq')

    if data is None or data.empty:
        logging.debug("股票："+stock+" 没有数据，略过...")
        return

    data['p_change'] = tl.ROC(data['close'], 1)
    return data


def run(stocks):
    update_fun = init_data

    db = SqliteDB(settings.SQLITE_DB_NAME)
    db.execute_handle('DELETE FROM stock_work_day_data')
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_stock = {executor.submit(update_fun, stock): stock for stock in stocks}
        for future in concurrent.futures.as_completed(future_to_stock):
            stock = future_to_stock[future]
            try:
                data = future.result()
                data['code'] = data['code'].apply(lambda x: str(x))
                if data is not None or not data.empty:
                    stocks = [tuple(x) for x in data.values]
                    db.batch_insert('stock_work_day_data', ['date_day', 'open', 'close','high','low','volume','code','p_change'], stocks)
            except Exception as exc:
                print('%s(%r) generated an exception: %s' % (stock[1], stock[0], exc))
