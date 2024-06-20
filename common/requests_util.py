# -*- coding: UTF-8 -*-
import json
import re
import traceback
import jsonpath
import requests
# from common.parameters_until import read_file
from common.logger_util import my_log, error_log
from common.yaml_util import *
from debugtalk import DebugTalk


class Requestutil:

    session = requests.session()

    def __init__(self):
        self.base_url =""
        self.last_headers={}

    # 规范功能测试YAML测试用例文件的写法
    def analysis_yaml(self,caseinfo):
        try:
            # 1.必须有的四个一级关键字：name，base_url，requests，validate
            caseinfo_keys = dict(caseinfo).keys()
            if 'name' in caseinfo_keys and 'base_url' in caseinfo and 'request' in caseinfo and 'validate' in caseinfo:
                # 2.request关键字必须包含两个二级关键字：method，url
                request_keys = dict(caseinfo['request']).keys()
                if 'method' in request_keys and 'url' in request_keys:
                    # 参数(params,data,json),请求头,文件上传这些都不能约束.
                    name = caseinfo['name']
                    self.base_url = caseinfo['base_url']
                    method = caseinfo['request']['method']
                    del caseinfo['request']['method']
                    url = caseinfo['request']['url']
                    del caseinfo['request']['url']
                    headers = None
                    if jsonpath.jsonpath(caseinfo,'$..headers'):
                        headers = caseinfo['request']['headers']
                        del caseinfo['request']['headers']
                    files = None
                    if jsonpath.jsonpath(caseinfo, '$..files'):
                        files = caseinfo['request']['files']
                        for key,value in dict(files).items():
                            files[key] = open(value,'rb')
                        del caseinfo['request']['files']
                    # 把method,url,headers,files这四个数据从caseinfo['request']去掉之后再把剩下的传给kwargs
                    res = self.send_request(name=name,method=method,url=url,headers=headers,files=files,**caseinfo['request'])
                    return_text = res.text
                    status_code = res.status_code
                    my_log("响应文本信息：%s"%return_text)
                    my_log("响应json信息：%s"%res.json())
                    # 提取接口关联的变量,既要支持正则表达式,又要支持json提取
                    if 'extract' in caseinfo_keys:
                        for key,value in dict(caseinfo['extract']).items():
                            # 正则表达式提取
                            if '(.*?)' in value or '(.+?)' in value:
                                ze_value = re.search(value,return_text)
                                if ze_value:
                                    extract_data = {key:ze_value.group(1)}
                                    write_file('/config/extract.yml',extract_data)
                                    print(extract_data)
                            else:   # json提取
                                return_json = res.json()  # 前提是要返回json格式
                                extract_data = {key:return_json[value]}
                                write_file('/config/extract.yml', extract_data)
                                print(extract_data)
                    # 断言的封装
                    yq_result = caseinfo['validate']
                    sj_result = res.json()
                    self.validate_result(yq_result, sj_result, status_code)
                else:
                    error_log('request关键字必须包含两个二级关键字：method，url')
            else:
                error_log('必须有的四个一级关键字：name，base_url，request，validate')
        except Exception as f:
            error_log("分析YAML文件异常：异常信息：%s" % str(traceback.format_exc()))

    #  统一替换方法,data可以是url(string),也可以是参数(字典,字典中包含有列表),也可以是请求头(字典).
    def replace_value(self,data):
        # 字典类型转换成字符串
        if data and isinstance(data,dict):  # 如果data不为空并且数据类型为字典
            str_data = json.dumps(data)
        else:
            str_data = data
        # 替换值
        for i in range(1, str_data.count('{{') + 1):
            if "{{" in str_data and "}}" in str_data:
                start_index = str_data.index("{{")
                end_index = str_data.index("}}",start_index)
                old_value = str_data[start_index:end_index + 2]
                new_value = read_file("/config/extract.yml", old_value[2:-2])
                str_data = str_data.replace(old_value, new_value)
        # 还原数据类型
        if data and isinstance(data,dict):  # 如果data不为空并且数据类型为字典
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #  统一替换方法,data可以是url(string),也可以是参数(字典,字典中包含有列表),也可以是请求头(字典).
    def replace_load(self, data):
        # 字典类型转换成字符串
        if data and isinstance(data, dict): # 如果data不为空并且数据类型为字典
            str_data = json.dumps(data)
        else:
            str_data = data
        # 替换值
        for i in range(1, str_data.count('${') + 1):
            if "${" in str_data and "}" in str_data:
                start_index = str_data.index("${")
                end_index = str_data.index("}", start_index)
                old_value = str_data[start_index:end_index + 1]
                function_name = old_value[2:old_value.index('(')]
                args_value = old_value[old_value.index('(')+1:old_value.index(')')]
                # 反射(通过一个函数的字符串直接去调用这个方法)
                new_value = getattr(DebugTalk(),function_name)(*args_value.split(','))
                str_data = str_data.replace(old_value, str(new_value))
        # 还原数据类型
        if data and isinstance(data, dict):   # 如果data不为空并且数据类型为字典
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    # 统一发送请求
    def send_request(self,name,method,url,headers=None,files=None,**kwargs):
        try:
            # 处理method
            self.last_method = str(method).lower()
            # 处理基础路径
            self.url=self.replace_load(self.base_url) + self.replace_value(url)
            # 处理请求头
            if headers and isinstance(headers,dict):
                self.last_headers=self.replace_value(headers)
            # 最核心的地方:请求数据如何去替换:可能是params,data,json
            for key,value in kwargs.items():
                if key in ['params','data','json']:
                    # 替换{{}}格式
                    value = self.replace_value(value)
                    # 替换${}格式
                    value = self.replace_load(value)
                    kwargs[key] = value
            # 收集日志
            my_log('-----------------接口请求开始-----------------')
            my_log("接口名称：%s"%name)
            my_log("请求方式：%s"%self.last_method)
            my_log("请求路径：%s"%self.url)
            my_log("请求头：%s"%self.last_headers)
            if 'params' in kwargs.keys():
                my_log("请求参数：%s"%kwargs['params'])
            elif 'data' in kwargs.keys():
                my_log("请求参数：%s"%kwargs['data'])
            elif 'json' in kwargs.keys():
                my_log("请求参数：%s"%kwargs['json'])
            my_log("文件上传：%s"%files)
            # 发送请求
            res = Requestutil.session.request(method=self.last_method,url=self.url,headers=self.last_headers,**kwargs)
            # print(res.request.headers)
            # print(res.text)
            # print(res.json())
            return res
        except Exception as f:
            error_log("发送请求异常：异常信息：%s"%str(traceback.format_exc()))

    # 断言封装
    def validate_result(self,yq_result,sj_result,status_code):
        try:
            '''
            :param yq_result:预期结果
            :param sj_result:实际结果
            :param status_code:实际状态码
            :return:
            '''
            # 收集日志
            my_log("预期结果：%s"%yq_result)
            my_log("实际结果：%s"%sj_result)
            #判断是否断言成功,0成功,1失败
            flag = 0
            # 解析ƒ
            if yq_result and isinstance(yq_result,list):
                for yq in yq_result:
                    for key,value in dict(yq).items():
                        # 判断断言方式
                        if key=='equals':
                            for assert_key,assert_value in dict(value).items():
                                if assert_key=='status_code':
                                    if status_code!=assert_value:
                                        flag=flag+1
                                        error_log("断言失败:"+assert_key+"不等于"+str(assert_value)+"")
                                else:
                                    key_list = jsonpath.jsonpath(sj_result,'$..%s'%assert_key)
                                    if key_list:
                                        if assert_value not in key_list:
                                            flag = flag + 1
                                            error_log("断言失败:"+assert_key+"不等于"+str(assert_value)+"")
                                    else:
                                        flag = flag + 1
                                        error_log("断言失败:返回结果中不存在"+assert_key+"")
                        elif key=='contains':
                            if value not in json.dumps(sj_result):
                                flag = flag + 1
                                error_log("断言失败:返回结果中不包含字符串"+value+"")
                        else:
                            error_log('框架不支持此断言方式')
            assert flag==0
            my_log('接口请求成功')
            my_log('-----------------接口请求结束-----------------\n')
        except Exception as f:
            my_log('接口请求失败')
            my_log('-----------------接口请求结束-----------------\n')
            error_log("断言异常：异常信息：%s" % str(traceback.format_exc()))


if __name__ == '__main__':
    # url = "/cgi-bin/tags/update?access_token={{access_token}}&a=c{{csrf_token}}"
    # for i in range(1,url.count("{{")+1):
    #     if "{{" in url and "}}" in url:
    #         start_index = url.index("{{")
    #         end_index = url.index("}}")
    #         old_value = url[start_index:end_index+2]
    #         new_value = read_file('/config/extract.yml',old_value[2:-2])
    #         url = url.replace(old_value,new_value)
    #
    #         print(old_value,new_value)
    #         print(url)


    # dict_data = {'name': '获取access_token统一鉴权码', 'base_url': 'https://api.weixin.qq.com', 'request': {'method': 'GET', 'url': '/cgi-bin/token', 'params': {'grant_type': 'client_credential', 'appid': 'wx9b755d429f6fb216', 'secret': 'b963db0b97c8487b0cb920a240bd78e3'}}, 'validate': [{'eq': ['status_code', 200]}]}
    # # print(dict_data.pop('name'))
    # del dict_data['name']
    # print(dict_data)

    json_data = {"tag": {"id": 100, "name": "张维序${get_random_number(100000,999999)}" }}
    result = Requestutil('base', 'base_weixin_url').replace_load(json_data)
    print(result)


