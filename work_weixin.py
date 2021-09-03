#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2021年9月3日
@author: yuejing
'''
import os
import requests
import json
import pymysql
import datetime

class WeChat:
    def __init__(self):
    	#企业ID，在管理后台获取
        self.CORPID = 'XXXX'  
        #自建应用的Secret，每个自建应用里都有单独的secret
        self.CORPSECRET = 'XXXX'
        #应用ID，在后台应用中获取
        self.AGENTID = 'XXXX'  
        #接收者用户名,多个用户用|分割
        self.TOUSER = "@all"  
        #接收部门ID，多个部门用|分割
        self.TOPARTY='1'

    #企业微信接口 https://work.weixin.qq.com/api/doc/90000/90135/91039
    def get_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET }
        req = requests.post(url, params=values)
        data = req.json() 
        access_token=data["access_token"]
        #写入access_token
        fo = open('access_token.txt', "w")
        fo.write(access_token)
        fo.close()

    #企业微信接口 https://work.weixin.qq.com/api/doc/90000/90135/90236
    def send_msg(self,access_token,Content):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        send_values = {
            "touser": self.TOUSER,
            "toparty": self.TOPARTY,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": Content},
            "safe": "0" }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json() 
        print(respone["errmsg"])
        return respone["errmsg"]

    #企业微信规定gettoken接口不能频繁请求
    def send_message(self, Content):
        try:
            #不存在access_token.txt则获取access_token生成
            if not os.path.exists('access_token.txt'):
                self.get_token()
            #循环获取有效access_token，直到发送消息
            result='do'
            while result != 'ok':
                #读取access_token
                fo = open('access_token.txt', "r+")
                access_token = fo.read()
                fo.close()
                #发送消息
                result=self.send_msg(access_token,Content)
                if result == 'ok':
                    break
                #获取新的access_token
                self.get_token()
        except Exception as e:
            print(str(e)) 

def run_compare():
	conn=pymysql.connect(host='XXXX',port=3306,user='root',passwd='123456',db='jimmy',use_unicode=True, charset="utf8")
	cur = conn.cursor()
	#查询数据库
	cur.execute("select DATE_FORMAT(CDATE,'%Y-%m-%d')+INTERVAL 27 DAY real_time from weixin where type='MC' and CDATE=(SELECT max(CDATE) from weixin)")
	result = cur.fetchone()[0]
	print(result,"提醒！")
	#插入数据库
	today = datetime.date.today()
	if result==str(today):
		#微信提醒
		wx = WeChat()
		wx.send_message("【姨妈提醒】\n宝宝，明天要大姨妈了，注意防护呀，爱你~")
		#插入时间
		cur.execute("insert into weixin select null,'MC',SYSDATE()+INTERVAL 1 DAY")
		conn.commit()
	#关闭
	cur.close()
	conn.close()

if __name__ == '__main__':
	run_compare()
