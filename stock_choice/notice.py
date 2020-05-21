
from stock_choice.channels.wx_company_notice import WXCompanyNotice
from stock_choice import settings

global wx_company
wx_company = WXCompanyNotice()
# 可以实现自己的推送逻辑（例如发送到手机上）
def strategy(msg=None):
    if msg is None or not msg:
        msg = "今日没有符合条件的股票"
    if settings.NOTIFY:
        # print(msg)
        wx_company.send_notice(settings.WX_COMPANY_CORP_ID,settings.WX_COMPANY_AGENT_ID,settings.WX_COMPANY_AGENT_SECRET_ID,settings.WX_COMPANY_SEND_USERS,msg)


def statistics(msg=None):
    if settings.NOTIFY:
        # print(msg)
        wx_company.send_notice(settings.WX_COMPANY_CORP_ID, settings.WX_COMPANY_AGENT_ID,
                               settings.WX_COMPANY_AGENT_SECRET_ID,settings.WX_COMPANY_SEND_USERS,msg)