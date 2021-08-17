#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2021年6月2日
@author: yuejing
'''
import os
import time
import requests
import json

class WeChat:
    def __init__(self):
        #企业ID，在管理后台获取
        self.CORPID = 'XXX'  
        #自建应用的Secret，每个自建应用里都有单独的secret
        self.CORPSECRET = 'XXX'
        #应用ID，在后台应用中获取
        self.AGENTID = 'XXX'  
        #接收者用户名,多个用户用|分割
        self.TOUSER = "@all"  
        #接收部门ID，多个部门用|分割
        self.TOPARTY='2'

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

if __name__ == '__main__':
    wx = WeChat()
    wx.send_message("【标题测试】\n通知正文测试")
