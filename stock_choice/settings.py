import os

import logging

from stock_choice import utils

current_dir = os.path.dirname(os.path.abspath(__file__))
from tools.sqlite_handle import SqliteDB

def init():
    global DB_DIR, NOTIFY,SHELVE_DB_NAME,SQLITE_DB_NAME,TUSHARE_TOKEN,WX_COMPANY_AGENT_ID,WX_COMPANY_AGENT_SECRET_ID,WX_COMPANY_CORP_ID,WX_COMPANY_SEND_USERS
    DB_DIR = current_dir + '/storage'
    LOG_DIR = current_dir + '/logs'
    NOTIFY = True
    SHELVE_DB_NAME = DB_DIR + '/stock_position'
    SQLITE_DB_NAME = DB_DIR + '/stock'
    PRE_SQL = current_dir + '/preSql.sql'
    WX_COMPANY_AGENT_ID = '1000001'
    WX_COMPANY_AGENT_SECRET_ID = 'ghgfgfhrr-wbEs8hnejju6pZuu68GUxtAtMT1_SvlxiU'
    WX_COMPANY_CORP_ID = '3454gfgshssdesdsd'
    WX_COMPANY_SEND_USERS = 'victor'
    # 如果有token则调用新api,没有则使用原始api
    TUSHARE_TOKEN = '1ba4asdasd2dd76b10dfsdfsdf3d61320054c870i0jojob641ad1987b46064'

    dirs = [DB_DIR,LOG_DIR]
    utils.prepare(dirs)
    db = SqliteDB(SQLITE_DB_NAME)
    db.execute_handle_file(PRE_SQL)

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%b-%d-%H:%M:%S', filename=LOG_DIR + '/info.log')
    logging.getLogger().setLevel(logging.INFO)