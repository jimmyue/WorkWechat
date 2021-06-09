#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2021年6月2日
@author: yuejing
'''
# https://www.cnblogs.com/rancher-maomao/p/10860069.html

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
        self.TOPARTY="2"

    def send_message(self, Content):
    	#获取access_token
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        access_token=data["access_token"]
        #发送企业微信消息
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        send_values = {
            "touser": self.TOUSER,
            "toparty":self.TOPARTY,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {"content": Content},
            "safe": "0" }
        send_msges=(bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json() 
        print(respone["errmsg"])
        return respone["errmsg"]

if __name__ == '__main__':
    wx = WeChat()
    wx.send_message("【标题】\n通知正文")
