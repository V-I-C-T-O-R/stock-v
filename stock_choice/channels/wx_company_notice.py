import json

import logging
import requests

'''
通知企业微信用户
'''
class WXCompanyNotice:
    def __init__(self):
        self.__failed = '发送失败'
        self.__successed = '发送成功'

    def send_notice(self, corp_id,agent_id,agent_secret,wechat_users,content):
        token = self.__get_token(corp_id,agent_secret)
        data = self.__createpostdata(wechat_users,agent_id,content)
        send_url = self.__get_send_url(token)
        _,msg = self.__send_to_wx(send_url,data)
        logging.info(msg)

    def __send_to_wx(self,url,data):
        try:
            resp = requests.post(url,data,headers={'Content-Type':'application/json'})
            if not resp or resp.status_code != 200 :
                return False,self.__failed
            return True,self.__successed
        except Exception as e:
            logging.error('访问企业微信错误',e)
            return False,self.__failed

    def __get_token_url(self, corp_id, corp_secret):
        return "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=" + corp_id + "&corpsecret=" + corp_secret;

    def __get_token(self, corpid,corp_secret):
        tokenUrl = self.__get_token_url(corpid, corp_secret);
        resp = requests.get(tokenUrl)
        jsonO = json.loads(resp.text)
        return jsonO.get("access_token");

    def __createpostdata(self, to_user, agent_id, content_value):
        data = {}
        data['touser'] = to_user
        data['msgtype'] = "text"
        data['agentid'] = agent_id

        content = {}
        content['content'] = content_value
        data["text"] = content
        return json.dumps(data)

    def __get_send_url(self,token):
        return "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+token;
