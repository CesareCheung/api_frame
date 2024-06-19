import allure
import pytest
from common.requests_util import Requestutil
from common.yaml_util import read_file


@allure.epic('财债通')
@allure.feature('财报审核分析')
class Testrequests:

    # 财债通-财报审核分析
    @allure.story('下载原文件')
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/CZT/financial_report/financial_report.yml'))
    def test_post_info(self,caseinfo):
        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)


