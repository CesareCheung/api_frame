# -*- coding: UTF-8 -*-
import random
from common.yaml_util import read_file


class DebugTalk:

    # 获取随机数
    def get_random_number(self,mix,max):
        return random.randint(int(mix),int(max))

    # 获取基础路径
    def get_base_url(self,one_node):
        return read_file('/config/config.yml','base',one_node)



