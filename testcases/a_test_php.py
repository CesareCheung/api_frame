# -*- coding: UTF-8 -*-
import re
import requests

'''
需要带请求头的接口，需要带Cookie的接口
cookie关联。基本上所有的web项目的接口都需要做cookie关联。
一般情况下我们会使用session对象关联。
因为session就表示同一个回话，同一个回话里面的cookie会自动关联。
'''

class Testrequests:

    csrf_token=""
    # phpwind_cookis=""
    # session = requests.session()    # 获得session会话对象

    # 访问phpwind论坛网页
    def test_phpwind_start(self,get_session):
        url = "http://47.107.116.139/phpwind"
        # res = requests.get(url)
        # res = Testrequests.session.request("get",url)
        res = get_session.request("get",url)
        return_data = res.text
        # 通过正则表达式取值
        obj = re.search('name="csrf_token" value="(.*?)"',return_data)
        Testrequests.csrf_token = obj.group(1)
        Testrequests.phpwind_cookis = res.cookies

    # 登录php首页
    def test_login(self,get_session):
        url = "http://47.107.116.139/phpwind/index.php?m=u&c=login&a=dorun"
        data = {
            "username":"wxw",
            "password":"123456",
            "csrf_token":Testrequests.csrf_token,
            "backurl":"http://47.107.116.139/phpwind/",
            "invite":""
        }
        headers={
            "Accept":"application/json, text/javascript, /; q=0.01",
            "X-Requested-With":"XMLHttpRequest"
        }
        # res = requests.post(url=url,data=data,headers=headers,cookies=Testrequests.phpwind_cookis)
        # res = Testrequests.session.request("post",url=url,data=data,headers=headers)
        res = get_session.request("post",url=url,data=data,headers=headers)
        print(res.request.headers)
        print(res.json())













