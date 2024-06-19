import allure
import pytest
from common.requests_util import Requestutil
from common.parameters_until import read_file

@allure.epic('微信公众号平台')
@allure.feature('标签模块')
class Testrequests:

    # 获取access_token(get请求)
    @allure.story('获取接口统一鉴权码token接口')
    @pytest.mark.parametrize("caseinfo",read_file('/testcases/weixin/get_token.yml'))
    def test_get_token(self,caseinfo):
        # url = "/cgi-bin/token"
        # params = {
        #     "grant_type":"client_credential",
        #     "appid":"wx9b755d429f6fb216",
        #     "secret":"b963db0b97c8487b0cb920a240bd78e3"
        # }
        # res = Requestutil('base','base_weixin_url').send_request("get",url,params=params)

        # return_data = res.json()
        # # 把中间变量写入extract.yml文件
        # extract_data = {"access_token":return_data['access_token']}
        # write_file('/extract.yml',extract_data)

        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)

    # 获取标签列表(get请求)
    @allure.story('查询标签接口')
    @pytest.mark.parametrize('caseinfo',read_file('/testcases/weixin/select_flag.yml'))
    def test_select_flag(self,caseinfo):
        # url = "/cgi-bin/tags/get"
        # params = {
        #     "access_token":"{{access_token}}",
        # }
        # Requestutil('base','base_weixin_url').send_request("get",url=url,params=params)

        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)

    # 编辑标签(post-json传参raw-json)
    @allure.story('编辑标签接口')
    @pytest.mark.parametrize('caseinfo', read_file('/testcases/weixin/edit_flag.yml'))
    def test_edit_flag(self,caseinfo):
        # url = "/cgi-bin/tags/update?access_token={{access_token}}"
        # data = {
        #     "tag": {"id": 100, "name": "码尚" + str(random.randint(100000,999999))}
        # }
        # Requestutil('base','base_weixin_url').send_request("post",url, json=data)
        # # res = requests.post(url=url, data=json.dumps(data))   #dumps序列化:把字典转换成字符串;loads反序列化:把字符串转换成字典

        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)

    # 文件上传
    @allure.story('文件上传接口')
    @pytest.mark.parametrize('caseinfo', read_file('/testcases/weixin/file_upload.yml'))
    def test_file_upload(self,caseinfo):
        # url = "/cgi-bin/media/uploadimg?access_token={{access_token}}"
        # data = {
        #     "media":open(r"E:/资料/图片/Tanzl.jpg",'rb')
        # }
        # Requestutil('base','base_weixin_url').send_request("post",url, files=data)

        allure.dynamic.title(caseinfo['name'])
        allure.dynamic.description(caseinfo['name'])
        Requestutil().analysis_yaml(caseinfo)



