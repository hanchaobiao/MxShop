#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : yunzhixu.py
# @Author: 韩朝彪
# @Date  : 2018/8/5
# @Desc  : 云之讯短信接口
import requests
import json


class YunZhiXun(object):

    def __init__(self):
        """
        封装各类REST操作接口
        :param baseUrl: 基准URL
        :param version: 版本号
        :param accountSid: 主帐号ID
        :param token: 账户授权令牌
        :param appId: 应用ID
        """
        self.accountSid = ""
        self.token = ""
        self.appId = ""
        self.baseUrl = "https://open.ucpaas.com/ol/sms/sendsms"

    def send_sms(self, mobile, code):
        """
        发送验证码
        :param mobile: 
        :param code: 
        :return: 
        """
        url = self.baseUrl
        header = {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=utf-8",
        }
        body = {
            "sid": self.accountSid,
            "token": self.token,
            "appid": self.appId,
            "templateid": "359306",
            "param": "{},{}".format(code, 5),
            "mobile": mobile,
            "uid": "2d92c6132139467b989d087c84a365d8"
        }
        response = requests.post(url=url, headers=header, json=body)
        print(json.loads(response.text))
        return json.loads(response.text)

if __name__ == '__main__':

    yzx = YunZhiXun()
    yzx.send_sms("", "1234")
