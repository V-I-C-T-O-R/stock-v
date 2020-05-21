
import datetime
from pandas.tseries.offsets import *
import pandas as pd
import os
from stock_choice import settings
from tools.sqlite_handle import SqliteDB

ONE_HOUR_SECONDS = 60 * 60

# 读取本地数据文件
def read_data(code_name):
    stock = code_name[0]
    db = SqliteDB(settings.SQLITE_DB_NAME)
    data = db.query_data('select * from stock_work_day_data where code = "%s" order by date_day asc' % stock)
    subset = pd.DataFrame(data, columns=['date_day', 'open', 'close','high','low','volume','code','p_change'])
    return subset

# 是否需要更新数据
def need_update_data():
    try:
        code_name = ('000001', '平安银行')
        data = read_data(code_name)
        if data is None or data.empty:
            return True
        else:
            start_time = next_weekday(data.iloc[-1].date_day)
            current_time = datetime.datetime.now()
            if start_time > current_time:
                return False
            return True
    except IOError:
        return True


# 是否是工作日
def is_weekday():
    return datetime.datetime.today().weekday() < 5


def next_weekday(date):
    return pd.to_datetime(date) + BDay()


def prepare():
    dirs = [settings.DB_DIR]
    for dir in dirs:
        if os.path.exists(dir):
            return
        else:
            os.makedirs(dir)

def format_print_result(results):
    contents = ''
    if not results:
        return contents
    flag = False
    for res in results:
        if flag:
            contents += '\n'
        else:
            flag = True
        code_name = '代码:' + str(res[0]) + '-' + res[1]
        volumns = ',市值:' + str(res[2]) + '万'
        contents += code_name + volumns
    return contents