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
    #企业微信接口 https://developer.work.weixin.qq.com/document/path/90253
    def upload_media(self,filepath,filetype='image'):
        try:
            #不存在access_token.txt则获取access_token生成
            if not os.path.exists('access_token.txt'):
                self.get_token()
            result=1
            while result != 0: #循环获取有效access_token，直到发送请求
                #读取access_token
                fo = open('access_token.txt', "r+")
                access_token = fo.read()
                fo.close()
                #发送请求
                upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}".format(access_token,filetype)
                files = {filetype: open(filepath, 'rb')}
                respone = requests.post(upload_url, files=files).json()
                result=respone["errcode"]
                if result == 0:
                    print('上传临时素材成功！ media_id:',respone['media_id'])
                    break
                #获取新的access_token
                self.get_token()
        except Exception as e:
            print(str(e)) 
        return respone['media_id']
    #企业微信接口 https://work.weixin.qq.com/api/doc/90000/90135/90236
    #发送文本消息
    def send_text(self,Content):
        try:
            #不存在access_token.txt则获取access_token生成
            if not os.path.exists('access_token.txt'):
                self.get_token()
            result=1
            while result != 0: #循环获取有效access_token，直到发送请求
                #读取access_token
                fo = open('access_token.txt', "r+")
                access_token = fo.read()
                fo.close()
                #发送请求
                send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
                send_values = {
                    "touser": self.TOUSER,
                    "toparty": self.TOPARTY,
                    "msgtype": "text",
                    "agentid": self.AGENTID,
                    "text": {"content": Content},
                    "safe": "0" }
                send_msges=(bytes(json.dumps(send_values), 'utf-8'))
                respone = requests.post(send_url,send_msges).json() 
                result=respone["errcode"]
                if result == 0:
                    print('文本消息发送成功！')
                    break
                #获取新的access_token
                self.get_token()
        except Exception as e:
            print(str(e)) 
    #发送图片消息
    def send_image(self,mediaid):
        try:
            #不存在access_token.txt则获取access_token生成
            if not os.path.exists('access_token.txt'):
                self.get_token()
            result=1
            while result != 0: #循环获取有效access_token，直到发送请求
                #读取access_token
                fo = open('access_token.txt', "r+")
                access_token = fo.read()
                fo.close()
                #发送请求
                send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
                send_values = {
                    "touser": self.TOUSER,
                    "toparty": self.TOPARTY,
                    "msgtype": "image",
                    "agentid": self.AGENTID,
                    "image" : {"media_id" : mediaid},
                    "safe": "0" }
                send_msges=(bytes(json.dumps(send_values), 'utf-8'))
                respone = requests.post(send_url,send_msges).json() 
                result=respone["errcode"]
                if result == 0:
                    print('图片消息发送成功！')
                    break
                #获取新的access_token
                self.get_token()
        except Exception as e:
            print(str(e)) 
    #发送图文消息
    def send_mpnews(self,mediaid,title,content):
        try:
            #不存在access_token.txt则获取access_token生成
            if not os.path.exists('access_token.txt'):
                self.get_token()
            result=1
            while result != 0: #循环获取有效access_token，直到发送请求
                #读取access_token
                fo = open('access_token.txt', "r+")
                access_token = fo.read()
                fo.close()
                #发送请求
                send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
                send_values = {
                    "touser": self.TOUSER,
                    "toparty": self.TOPARTY,
                    "msgtype": "mpnews",
                    "agentid": self.AGENTID,
                    "mpnews" : {
                        "articles":[
                            {
                               "title": title, 
                               "thumb_media_id": mediaid,
                               "author": "jimmy",
                               "content": content,
                               "digest":  content
                            }
                        ]
                    },
                    "safe": "0" }
                send_msges=(bytes(json.dumps(send_values), 'utf-8'))
                respone = requests.post(send_url,send_msges).json() 
                result=respone["errcode"]
                if result == 0:
                    print('图文消息发送成功！')
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
		wx.send_text("【姨妈提醒】\n宝宝，明天要大姨妈了，注意防护呀，爱你~")
		#插入时间
		cur.execute("insert into weixin select null,'MC',SYSDATE()+INTERVAL 1 DAY")
		conn.commit()
	#关闭
	cur.close()
	conn.close()

if __name__ == '__main__':
	run_compare()
