# -*- coding: UTF-8 -*-
import os
import yaml
from common.get_path import *


# 读取yml文件
def read_file(yml_file,one_node=None,two_node=None):
    path = BASE_DIR+yml_file
    with open(path,encoding='utf-8') as f:
        value = yaml.load(f,Loader=yaml.FullLoader)
        if one_node and two_node:
            return value[one_node][two_node]
        elif one_node:
            return value[one_node]
        else:
            return value

# 写入yml文件
def write_file(yml_file,data):
    path = BASE_DIR+yml_file
    with open(path,encoding='utf-8',mode='a') as f:
        yaml.dump(data, stream=f,allow_unicode=True)

# 清空yml文件
def clean_file(yml_file):
    path = BASE_DIR+yml_file
    with open(path,encoding='utf-8',mode='w') as f:
        f.truncate()

if __name__ == '__main__':
    # print(read_file('/config.yml',"base",'base_info_url'))
    print(read_file('/config/config.yml','log','log_name'))


