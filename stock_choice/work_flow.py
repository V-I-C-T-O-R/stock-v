
import datetime
import logging
import time

import pandas as pd
import tushare as ts

from stock_choice import data_fetcher, notice
from stock_choice import db
from stock_choice import settings
from stock_choice import utils
from stock_choice.strategy import backtrace_ma250
from stock_choice.strategy import breakthrough_platform
from stock_choice.strategy import enter as enter
from stock_choice.strategy import keep_increasing
from stock_choice.strategy import parking_apron
from stock_choice.strategy import turtle_trade
from tools.sqlite_handle import SqliteDB


def process():
    logging.info("************************ process start ***************************************")
    try:
        all_data = ts.get_today_all()
        if all_data is None or all_data.empty:
            return
        #code:股票代码,name:企业名,nmc:流通市值
        subset = all_data[['code', 'name', 'nmc']]
        logging.info('清理stock_info表股票数据...')
        db = SqliteDB(settings.SQLITE_DB_NAME)
        db.execute_handle('delete from stock_info')
        stocks = [tuple(x) for x in subset.values]
        logging.info('stock_info表插入最新股票数据')
        db.batch_insert('stock_info',['code','name','nmc'],stocks)

        statistics(all_data, stocks)
    except Exception as e:
        logging.warning('获取股票数据失败,从旧数据从获取...',e)
        db = SqliteDB(settings.SQLITE_DB_NAME)
        data = db.query_data('select * from stock_info')
        subset = pd.DataFrame(data, columns=['code', 'name', 'nmc'])
        stocks = [tuple(x) for x in subset.values]

    if utils.need_update_data():
        data_fetcher.run(stocks)
        check_exit()

    strategies = {
        '海龟交易法则': turtle_trade.check_enter,
        '放量上涨': enter.check_volume,         #放量上涨是指成交量大幅增加的同时，个股的股价也同步上涨的一种量价配合现象
        '突破平台': breakthrough_platform.check,#平台突破是描述股票、期货、外汇的K线图价格走势突破前期整理的平台
        '均线多头': keep_increasing.check,      #多头排列由三根移动平均线组成，其排列顺序是:短期、中期、长期均线呈自上而下顺序排列。它出现在涨势中，是一种做多的信号，表明后市继续看涨
        '停机坪': parking_apron.check,          #股价一波下跌后大阳线拉起就横盘，很形象的称为停机坪
        '回踩年线': backtrace_ma250.check,      #什么是回踩年线？回踩年线什么意思？攻击线是均线系统中周期最短的一根线，在上升趋势中位于所有均线之上。
                                                #回踩年线当股价出现洗盘或者调整时一定是第一时间向下触碰攻击线，回踩年线此时回调的幅度最浅，回调的时间最短，
                                                #对上升趋势的保护性最强，回踩年线属于最强势的一种上升趋势，一且回踩止跌后就会带给投资者非常好的交易机会。
    }

    if datetime.datetime.now().weekday() == 0:
        strategies['均线多头'] = keep_increasing.check

    for strategy, strategy_func in strategies.items():
        check(stocks, strategy, strategy_func)
        time.sleep(2)

    logging.info("************************ process   end ***************************************")


def check(stocks, strategy, strategy_func):
    end = None
    m_filter = check_enter(end_date=end, strategy_fun=strategy_func)
    results = list(filter(m_filter, stocks))

    format_put = '********"{0}"********\n{1}\n********"{0}"********\n'.format(strategy, utils.format_print_result(results))
    print(format_put)
    logging.info(format_put)
    if not results:
        return
    notice.strategy(format_put)


def check_enter(end_date=None, strategy_fun=enter.check_volume):
    def end_date_filter(code_name):
        data = utils.read_data(code_name)
        if data is None or data.empty:
            return False
        else:
            return strategy_fun(code_name, data, end_date=end_date)
        # if result:
        #     message = turtle_trade.calculate(code_name, data)
        #     logging.info("{0} {1}".format(code_name, message))
        #     notice.push("{0} {1}".format(code_name, message))

    return end_date_filter


# 统计数据
def statistics(all_data, stocks):
    limitup = len(all_data.loc[(all_data['changepercent'] >= 9.5)])
    limitdown = len(all_data.loc[(all_data['changepercent'] <= -9.5)])

    up5 = len(all_data.loc[(all_data['changepercent'] >= 5)])
    down5 = len(all_data.loc[(all_data['changepercent'] <= -5)])

    def ma250(stock):
        stock_data = utils.read_data(stock)
        return enter.check_ma(stock, stock_data)

    ma250_count = len(list(filter(ma250, stocks)))

    msg = "涨停数：{}   跌停数：{}\n涨幅大于5%数：{}  跌幅大于5%数：{}\n年线以上个股数量：    {}"\
        .format(limitup, limitdown, up5, down5, ma250_count)
    logging.info(msg)
    notice.statistics(msg)

def check_exit():
    t_shelve = db.ShelvePersistence()
    file = t_shelve.open()
    for key in file:
        code_name = file[key]['code_name']
        data = utils.read_data(code_name)
        if turtle_trade.check_exit(code_name, data):
            notice.strategy("{0} 达到退出条件".format(code_name))
            logging.info("{0} 达到退出条件".format(code_name))
            del file[key]
        elif turtle_trade.check_stop(code_name, data, file[key]):
            notice.strategy("{0} 达到止损条件".format(code_name))
            logging.info("{0} 达到止损条件".format(code_name))
            del file[key]

    file.close()