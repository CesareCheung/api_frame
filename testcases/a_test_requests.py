import json
import random
import requests

class Testrequests:

    access_token=""

    # 获取access_token(get请求)
    def test_get1(self):
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            "grant_type":"client_credential",
            "appid":"wx9b755d429f6fb216",
            "secret":"b963db0b97c8487b0cb920a240bd78e3"
        }
        res = requests.get(url=url, params=params)
        # print(res.text)
        # print(res.content)
        # print(res.json())
        # print(res.status_code)
        # print(res.reason)
        # print(res.cookies)
        # print(res.headers)
        # print(res.request.headers)
        return_data = res.json()
        Testrequests.access_token = return_data['access_token']
        print(return_data)

    # 获取标签列表(get请求)
    def test_get2(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/get"
        params = {
            "access_token":Testrequests.access_token,
        }
        res = requests.get(url=url, params=params)
        return_data = res.json()
        print(return_data)

    # Z世代-公司简介(post-键值对传参x-www-form-urlencoded)
    def test_post1(self):
        url = "https://info-node1.superzgen.com/info/pub/profile"
        data = {
            "stockCode":600000,
        }
        res = requests.post(url=url, data=data)
        print(res.request.headers)
        print(res.json())

    # Z世代-公司简介(post-json传参raw-json)
    def test_post2(self):
        url = "https://api.weixin.qq.com/cgi-bin/tags/update?access_token="+Testrequests.access_token+""
        data = {
            "tag": {"id": 100, "name": "码尚" + str(random.randint(100000,999999))}
        }
        res = requests.post(url=url, json=data)
        # res = requests.post(url=url, data=json.dumps(data))   #dumps序列化:把字典转换成字符串;loads反序列化:把字符串转换成字典
        print(res.request.headers)
        print(res.json())

    # 文件上传
    def test_file_upload(self):
        url = "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token="+Testrequests.access_token+""
        data = {
            "media":open(r"E:/资料/图片/Tanzl.jpg",'rb')
        }
        res = requests.post(url=url, files=data)
        print(res.request.headers)
        print(res.json())

if __name__ == '__main__':
    Testrequests().test_get1()
    Testrequests().test_file_upload()

