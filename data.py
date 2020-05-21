
import numpy as np

from tools.csv_handle import *
from tools.generate_data import generate_stock_basic, query_industry_data


def get_data(token):
    result = generate_stock_basic(token)

    # list扁平化 [['a'],['b'],['c']] ==> ['a','b','c']
    flatten_list = np.array(result).flatten().tolist()

    stock_list = request_to_list(flatten_list, 50)

    price_list = top_ten_by_price(stock_list)
    range_list = top_ten_by_range(stock_list)
    range_r_list = top_ten_by_range_r(stock_list)
    volume_list = top_ten_by_volume(stock_list)
    turn_volume_list = top_ten_turn_volume(stock_list)

    context = dict()
    context["price_list"] = price_list
    context["range_list"] = range_list
    context["range_r_list"] = range_r_list
    context["volume_list"] = volume_list
    context["turn_volume_list"] = turn_volume_list
    context["stock_list"] = stock_list

    return context

def get_industry_data(token):
    result , industry_list = query_industry_data(token)

    # list扁平化 [['a'],['b'],['c']] ==> ['a','b','c']
    flatten_list = np.array(result).flatten().tolist()

    stock_list = request_to_list(flatten_list, 50)
    industry_stock_list = {}
    for stock_info in stock_list:
        for key,value in industry_list.items():
            if stock_info[6] not in value:
                continue
            if industry_stock_list.get(key):
                industry_stock_list[key].append(stock_info)
            else:
                industry_stock_list[key] = [stock_info]

    context = dict()
    for k,v in industry_stock_list.items():
        context[k] = top_ten_by_range(v)

    return context