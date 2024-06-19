import re
import pytest
from common.requests_util import Requestutil
from common.yaml_util import *


class Testrequests:

    # 访问phpwind论坛网页
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/phpwind_start.yml'))
    def test_phpwind_start(self,caseinfo):
        # url = "/phpwind"
        # res = Requestutil('base','base_php_url').send_request("get",url)
        # return_data = res.text
        # # 通过正则表达式取值
        # obj = re.search('name="csrf_token" value="(.*?)"',return_data)
        # extract_data = {"csrf_token":obj.group(1)}
        # write_file("/extract.yml",extract_data)

        Requestutil().analysis_yaml(caseinfo)

    # 登录php首页
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/phpwind_login.yml'))
    def test_php_login(self,caseinfo):
        # url = "/phpwind/index.php?m=u&c=01_login&a=dorun"
        # data = {
        #     "username":"wxw",
        #     "password":"123456",
        #     "csrf_token": "{{csrf_token}}",
        #     "backurl":"http://47.107.116.139/phpwind/",
        #     "invite":""
        # }
        # headers={
        #     "Accept":"application/json, text/javascript, /; q=0.01",
        #     "X-Requested-With":"XMLHttpRequest"
        # }
        # Requestutil('base','base_php_url').send_request("post",url,data=data,headers=headers)

        Requestutil().analysis_yaml(caseinfo)

