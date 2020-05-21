import tushare as ts

def replace_code(x):
    if x.endswith('.SZ'):
        return 's_sz' + x[:-3]
    else:
        return 's_sh' + x[:-3]

def replace_short_code(x):
    if x.endswith('.SZ'):
        return 'sz' + x[:-3]
    else:
        return 'sh' + x[:-3]

def generate_stock_basic(token):
    pro = ts.pro_api(token)
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code')
    result = data['ts_code'].apply(replace_code)
    return result

def query_industry_data(token=None):
    pro = ts.pro_api(token)
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,industry')
    result = data['ts_code'].apply(replace_code)

    industry_map = {}
    for i in data.to_dict('records'):
        ts_code = replace_short_code(i['ts_code'])
        industry = i['industry']

        if industry_map.get(industry):
            industry_map[industry].append(ts_code)
        else:
            industry_map[industry] = [ts_code]

    return result,industry_map


def query_today_data(token):
    # ts.set_token(token)
    all_data = ts.get_stock_basics()

    print(all_data)
