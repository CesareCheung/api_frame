import os
import time
import pytest

if __name__ == '__main__':
    pytest.main()

    time.sleep(1)
    # os.system("allure generate ./reports/temp -o ./reports/allure --clean")
    # copy environment.properties  .\\reports\\temp 设置allure报告环境变量
    os.system("copy environment.properties  .\\reports\\temp")
    os.system("allure generate ./reports/temp -o ./reports/allure --clean")


import json


# 修改allure报告的报告标题
def set_report_title(json_file_path, key, new_value):
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 修改特定内容
    data['reportName'] = new_value

    # 将修改后的内容写回到文件
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 调用set_report_title方法，设置测试报告报告title
json_file_path = r'C:\Users\1\Desktop\api_frame\reports\allure\widgets\summary.json'
set_report_title(json_file_path, 'reportName', '分米互联接口自动化测试报告')