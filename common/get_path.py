# -*- coding: UTF-8 -*-
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件目录
CONFIG_DIR = os.path.join(BASE_DIR,'config')

# 测试用例文件目录
TESTCASES_DIR = os.path.join(BASE_DIR,'testcases')

#data文件目录
DATA_DIR = os.path.join(BASE_DIR,'data')

#日志文件目录
LOGS_DIR=os.path.join(BASE_DIR,'logs')


if __name__ == '__main__':
    print(LOGS_DIR)