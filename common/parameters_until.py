import csv
import json
import traceback
import yaml
from common.get_path import *
from common.logger_util import error_log


# 读取csv文件
def read_csv_file(csv_file):
    '''c参数说明'''
    csv_list = []
    path = BASE_DIR+"/"+csv_file
    with open(path,encoding='utf-8') as f:
        csv_data = csv.reader(f)
        for row in csv_data:
            csv_list.append(row)
    return csv_list

# 读取yaml文件
def read_file(yml_file):
    try:
        path = BASE_DIR+yml_file
        with open(path,encoding='utf-8') as f:
            caseinfo = yaml.load(f,Loader=yaml.FullLoader)
            if len(caseinfo)>=2:
                return caseinfo
            else:
                caseinfo_keys = dict(*caseinfo).keys()
                if 'parameters' in caseinfo_keys:
                    new_caseinfo = analysis_parameters(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo
    except Exception as f:
        error_log("读取用例文件报错：异常信息：%s"%str(traceback.format_exc()))


# 分析参数化
def analysis_parameters(caseinfo):
    try:
        caseinfo_keys = dict(caseinfo).keys()
        if 'parameters' in caseinfo_keys:
            for key, value in dict(caseinfo['parameters']).items():
                caseinfo_str = json.dumps(caseinfo)
                key_list = str(key).split('-')
                # 规范csv数据的写法
                length_flag = True
                csv_list = read_csv_file(value)
                one_row_data = csv_list[0]
                for csv_data in csv_list:
                    if len(csv_data) != len(one_row_data):
                        length_flag = False
                        break
                # 解析
                new_caseinfo = []
                if length_flag:
                    for x in range(1, len(csv_list)):  # x代表行
                        temp_caseinfo = caseinfo_str
                        for y in range(0, len(csv_list[x])):  # y代表列
                            if csv_list[0][y] in key_list:
                                temp_caseinfo = temp_caseinfo.replace("$csv{" + csv_list[0][y] + "}", csv_list[x][y])
                        new_caseinfo.append(json.loads(temp_caseinfo))
                return new_caseinfo
        else:
            return caseinfo
    except Exception as f:
        error_log("分析parameters参数异常：异常信息：%s"%str(traceback.format_exc()))


if __name__ == '__main__':
    print(read_file('/testcases/weixin/get_token.yml'))

















