Stock-V
----------
> 炒股有风险,投资需谨慎

糅合[Sequoia](https://github.com/sngyai/Sequoia)与[py_stock](https://github.com/geeeeeeeek/py_stock)项目功能，统一展现

##### 所做工作
* py_stock项目web接口化,定时生成最新看板
* py_stock项目去除中转csv文件，直接查询新浪
* Sequoia去掉中转本地文件，改用sqlite存储查询(建表记得建索引(⊙o⊙)哦)
* 优化Sequoia逻辑
* Sequoia企业微信通知(短信懒得弄了-_-)

> 环境统一为python3.5,推荐新建env运行项目

#### 步骤
1. 请设置tushare pro的token凭证码，如果没有请访问https://tushare.pro注册申请
#### tushare用法
| 名称          | 类型        | 必选 | 描述 |
| ------------ | ---------- | :-------: | :-------: |
| ts_code      | str        |     Y     |     证券代码     |
| pro_api      | str        |     N     |     pro版api对象     |
| start_date   | str        |     N     |     开始日期 (格式：YYYYMMDD)     |
| end_date     | str        |     N     |     结束日期 (格式：YYYYMMDD)     |
| asset        | str        |     Y     |     资产类别：E股票 I沪深指数 C数字货币 F期货 O期权，默认E     |
| adj          | str        |     N     |     复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None     |
| freq         | str        |     Y     |     数据频度 ：1MIN表示1分钟（1/5/15/30/60分钟） D日线 ，默认D     |
| ma           | list       |     N     |     均线，支持任意合理int数值     |
2. 注册企业微信新建通知应用,并绑定个人微信通知

3. pip install -r requirements.txt

4. 启动py_stock服务,直接python run.py. web访问http://localhost:8080访问
效果如图:
![2.png](images/2.png?raw=true "行情看板")

5. 启动Sequoia,直接python stock_choice/god_choice.py. 通过企业微信小助手通知便可得到结果
效果如图:
![1.jpg](pic/1.jpg?raw=true "信息通知")

#### 问题
- 当调用ts.get_today_all()方法时，会出现ValueError: No ':' found when decoding object value异常。不要慌，直接更改环境库源码中site-packages/tushare/stock/trading.py文件的_parsing_dayprice_json函数内容即可：
```
def _parsing_dayprice_json(types=None, page=1):
    """
           处理当日行情分页数据，格式为json
     Parameters
     ------
        pageNum:页码
     return
     -------
        DataFrame 当日所有股票交易数据(DataFrame)
    """
    ct._write_console()
    request = Request(ct.SINA_DAY_PRICE_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'],
                                 ct.PAGES['jv'], types, page))
    text = urlopen(request, timeout=10).read()
    if text == 'null':
        return None
    js = text.decode('utf8')       # 此处关键的地方
    df = pd.DataFrame(pd.read_json(js, dtype={'code':object}),
                  columns=ct.DAY_TRADING_COLUMNS)
    df = df.drop('symbol', axis=1)
    return df

```
- 安装ta-lib
下载 [ta-lib-0.4.0-src.tar.gz](http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz) :
```
$ tar -zxvf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib
$ sudo ./configure --prefix=/usr
$ sudo make && sudo make install
$ sudo find / -name libta_lib.so.0
$ vim /etc/profile
##添加
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib
$ sudo source /etc/profile
```