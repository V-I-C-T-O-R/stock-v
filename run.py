from bottle import route, run, template, HTTPResponse, static_file
from data import get_data, get_industry_data
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
from stock_choice import settings
settings.init()

@route('/stock')
def get_stock():
    data = get_data(settings.TUSHARE_TOKEN)
    html_template = current_dir + '/static/template.html'
    if data:
        return template(html_template, items=data)
    else:
        return HTTPResponse(status=204)

@route('/stock/industry')
def get_industry():
    data = get_industry_data(settings.TUSHARE_TOKEN)
    print(data)
    html_template = current_dir + '/static/industry_template.html'
    if data:
        return template(html_template, industry=data)
    else:
        return HTTPResponse(status=204)

@route('/static/:filename#.*#', name='css')
def send_static(filename):
    return static_file(filename, root=os.path.join(current_dir, 'static'))

run(host='localhost', port=8080, debug=True)