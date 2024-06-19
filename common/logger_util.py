import logging
import time
from common.get_path import *
from common.yaml_util import read_file


class LoggerUitl:
    def create_log(self,logger_name='log'):
        # 创建一个日志对象
        self.logger = logging.getLogger(logger_name)
        # 设置全局的日志级别(DEBUG<INFO<WARNING<ERROR<CRITICAL)
        self.logger.setLevel(logging.DEBUG)
        # 防止日志重复
        if not self.logger.handlers:
            #------------文件日志--------------
            # 获取日志文件的名称
            self.file_log_path = LOGS_DIR+'/'+ read_file('/config/config.yml','log','log_name') + str(int(time.time()))+".log"
            # 创建文件日志的控制器
            self.file_handler = logging.FileHandler(self.file_log_path,encoding='utf-8')
            # 设置文件日志的级别
            file_log_level= str(read_file('/config/config.yml','log','log_level')).lower()
            if file_log_level == 'debug':
                self.file_handler.setLevel(logging.DEBUG)
            elif file_log_level == 'info':
                self.file_handler.setLevel(logging.INFO)
            elif file_log_level == 'waring':
                self.file_handler.setLevel(logging.WARNING)
            elif file_log_level == 'error':
                self.file_handler.setLevel(logging.ERROR)
            elif file_log_level == 'critical':
                self.file_handler.setLevel(logging.CRITICAL)
            # 设置文件日志的格式
            self.file_handler.setFormatter(logging.Formatter(read_file('/config/config.yml','log','log_format')))
            # 将控制器加入到日志对象
            self.logger.addHandler(self.file_handler)

            #------------控制台日志--------------
            # 创建控制台日志的控制器
            self.console_handler = logging.StreamHandler()
            # 设置控制台日志的级别
            console_log_level= read_file('/config/config.yml','log','log_level').lower()
            if console_log_level == 'debug':
                self.console_handler.setLevel(logging.DEBUG)
            elif console_log_level == 'info':
                self.console_handler.setLevel(logging.INFO)
            elif console_log_level == 'waring':
                self.console_handler.setLevel(logging.WARNING)
            elif console_log_level == 'error':
                self.console_handler.setLevel(logging.ERROR)
            elif console_log_level == 'critical':
                self.console_handler.setLevel(logging.CRITICAL)
            # 设置控制台日志的格式
            self.console_handler.setFormatter(logging.Formatter(read_file('/config/config.yml','log','log_format')))
            # 将控制器加入到日志对象
            self.logger.addHandler(self.console_handler)

        return self.logger

# 函数:输出正常日志
def my_log(log_massage):
    LoggerUitl().create_log().info(log_massage)

# 函数:输出错误日志
def error_log(log_massage):
    LoggerUitl().create_log().error(log_massage)
    raise Exception(log_massage)


if __name__ == '__main__':
    my_log('zhangweixu')








