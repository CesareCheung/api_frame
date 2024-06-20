# **Python+Pytest+Allure+Yaml框架结构**

common:公共方法包
	
	--get_path.py:获取文件路径方法
	
	--logger_util.py:输出日志方法
	
	--parameters_until.py：传参方式方法封装
	
	--requests_util.py：请求方式方法封装
	
	--yaml_util.py：yaml文件读取写入方法
	

config: 配置包

	--config.yml：配置文件，主要为域名ip地址配置及日志输出级别
	
	--extract.yml：接口上下游串联时，用例文件做参数化截取返回值后自动输出保存到该文件


data: 用于存放csv传参文件包（可用可不用，具体根据实际情况）

	--get_token.csv：存放csv文件参数

logs: 日志输出文件，会自动生成

reports: 测试报告文件

testcase: 测试用例文件集
	
	--fenmi：项目测试用例
	
		--login.yml：接口参数传参  
        # 如：
        -   name: 1、获取UUID
            #    base_url: https://baidu.com
            base_url: ${get_base_url(base_fenmi_url)}
            request:
                method: get
                url: /fenmi/code
                headers:
                    Authorization: '{{access_token}}'
                params:
                    Accept: application/json, text/plain, */*
                    Accept-Encoding: gzip, deflate, br, zstd
                    Accept-Language: zh-CN,zh;q=0.9
                    Connection: keep-alive
            extract:
                uuid: '"uuid":"(.*?)"'
            validate:
                -   equals: {code: 200}
                -   equals: {msg: "操作成功"}
                
        # 解释：
            name：为接口名称
            
            base_url：读取config.yml文件的域名IP
            
            request:请求参数
            
            method：请求方式
            
            url:接口地址
            
            headers：请求头，比如token,'{{access_token}}'为取上游接口返回值做变量进行参数化，做参数化为固定写法'{{变量名}}'
            
            params: 请求参数，具体需要看接口请求传参方式
            
            extract：用于存在上下游接口关联时对返回值进行取值，固定写法，'"uuid":"(.*?)"'为正则表达式取值，也可用json提取，固定写法'"变量名"：正则表达式'
            
            validate：断言           
		
		--test_fenmi.py: 单用例执行器，执行式传入对应yaml文件地址即可
        
            import allure
            import pytest
            from common.requests_util import Requestutil
            from common.parameters_until import read_file

            @allure.epic('XX互联')
            @allure.feature('登录并查询服务收入细项列表数据')
            class Testrequests:

                # 获取access_token(get请求)
                @allure.story('获取uuid并登录获取token')
                @allure.severity("normal")
                @pytest.mark.parametrize("caseinfo",read_file('/testcases/fenmi/login.yml'))
                def test_get_token(self,caseinfo):
                    allure.dynamic.title(caseinfo['name'])
                    allure.dynamic.description(caseinfo['name'])
                    Requestutil().analysis_yaml(caseinfo)

	

all.py:  主运行程序

conftest.py: 测试配置工具，clean_extract方法为重跑时清除原文件数据

debugtalk.py:自定义函数，用于存放公共函数和变量的文件

environment.properties:用于生成allure测试报告时，配置展示环境数据


pytest.ini: pytest测试运行配置文件，用于配置pytest运行时指定一些参数

    [pytest]
    addopts = -vs --alluredir=reports/temp --clean-alluredir            运行时清除原先的测试报告及临时文件
    ; testpaths = testcases/fenmi                                       执行单个项目测试文件时可选一个testcase目录
    testpaths = testcases/fenmi testcases/weixin testcases/Zgen         执行多个项目测试文件时可选多个testcase目录   
    python_files = test_*.py                                            执行的文件，及测试用例
    python_classes = Test*                                              执行对应测试用例目录所有Test开头的类
    python_functions = test_*                                           执行对应类下所有的test开头的方法











# **接口自动化测试框架规则**

1.必须有的四个一级关键字：name，base_url，requests，validate

2.request关键字必须包含两个二级关键字：method，url

3.传参方式：在request一级关键字下，通过二级关键字参数传参。

    如果是get请求，通过params传参。如：
        params:
            grant_type: client_credential
            appid: wx9b755d429f6fb216
            secret: b963db0b97c8487b0cb920a240bd78e3
    如果是post请求：
        传json格式，通过json关键字传参。如：
            json: {"tag": {"id": 100, "name": "王兴文aaa" }}
        传表单格式，通过data关键字传参。如：
            data:{
                "tag": {"id": 100, "name": "王兴文aaa" }
            }
        传文件格式，通过files关键字传参。如：
            files:
                media: "E:/资料/图片/Tanzl.jpg"
4.如果需要做接口关联，那么必须使用一级关键字：extract

    提取：
        如：json提取方式
        extract:
            access_token: access_token
        如：正则表达式提取方式
        extract:
            access_token: '"access_token":"(.*?)"'
    取值：
        如：
        access_token={{access_token}}

5.热加载，当yaml文件需要使用动态参数时，那么可以在debugtalk.py中写方法调用。

    注意：传参时，需要什么类型的数据，需要做强转。int(mix),int(max)，如：
    # 获取随机数
    def get_random_number(self,mix,max):
        return random.randint(int(mix),int(max))
    热加载取值：
    ${get_random_number(100000,999999)}
6.此框架支持两种断言方式：分别是equals和contains断言：

    如：
    validate:
    -   equals: {status_code: 200}
    -   equals: {expires_in: 7200}
    -   contains: access_token
7.数据驱动使用csv和一级关键字parameters实现：如：
    
    yaml写法：
        parameters:
            name-appid-secret-grant_type-assert_str: data/get_token.csv
    csv写法：

    name,appid,secret,grant_type,assert_str
    获取access_token统一鉴权码,wx9b755d429f6fb216,b963db0b97c8487b0cb920a240bd78e3,client_credential,access_token
    appid必填项检查,"",b963db0b97c8487b0cb920a240bd78e3,client_credential,errcode
    secret必填项检查,wx9b755d429f6fb216,"",client_credential,errcode
8.日志监控，异常处理，以及基础路径的设置。




