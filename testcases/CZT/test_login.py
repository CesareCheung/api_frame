import allure
import pytest
from common.requests_util import Requestutil
from common.yaml_util import read_file

@pytest.mark.run(order=1)
@allure.epic('财债通')
@allure.feature('登录模块')
class Testrequests:

    # 财债通-登录
    @allure.story('获取登录token')
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/CZT/login.yml'))
    def test_post_info(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)


