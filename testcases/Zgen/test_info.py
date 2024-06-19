import allure
import pytest
from common.requests_util import Requestutil
from common.yaml_util import read_file


@allure.epic('Z世代项目')
@allure.feature('资讯模块')
class Testrequests:

    # Z世代-公司简介(post-键值对传参x-www-form-urlencoded)
    @allure.story('查询浦发银行公司简介接口')
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/Zgen/Zgen_info.yml'))
    def test_post_info(self,caseinfo):
        # url = "/info/pub/profile"
        # data = {
        #     "stockCode":600000
        # }
        # Requestutil('base','base_info_url').send_request("post",url, data=data)

        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)


