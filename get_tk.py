# 获取操作时用的令牌并写入config.json
from asyncio.log import logger
import hashlib
import jsonpath
import requests
import json
import time
# import op_config
# import demjson

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='report.log')
logger = logging.getLogger(__name__)


def read_config():
    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    # rosterId = config['rosterId']
    # access_token = config['access_token']
    # studentName = config['studentName']
    send_hosts = config['send_hosts']
    return send_hosts


send_hosts = read_config()


def get_token():
    global send_hosts
    userCode = str(input("请输账号:"))
    userPwd = str(input("请输密码:"))
    logger.info("账号："+userCode+"\n密码："+userPwd)
    logger.info("正在使用加密算法加密密码")
    userPwd = hashlib.md5(userPwd.encode(encoding='UTF-8')).hexdigest()
    logger.info("加密完成,加密后用于传输的密码是："+userPwd)
    logger.info("加密完成,正在发起请求")
    endpoit_url = "/api/mStuApi/token.do"
    BaseURL = "https://" + send_hosts
    get_token_send_data = {
        "userCode": userCode,
        "userPwd": userPwd
    }
    r = requests.post(url=BaseURL+endpoit_url, data=get_token_send_data)
# print(r.text)
    logger.info("请求完成,正在处理返回数据")
    # if r.status_code == 200:
    json_data = json.loads(r.text)
    if json_data['isSuccess'] == True:
        logger.info("获取令牌成功")
        access_token = jsonpath.jsonpath(json_data, '$.data.accessToken')
        rosterId = jsonpath.jsonpath(json_data, '$.data.studentId')
        studentName = jsonpath.jsonpath(json_data, '$.data.studentName')
        # logger.info("你好"+str(studentName) +'\n你的rosterId是'+str(rosterId)+"\n你的令牌是"+str(access_token))
        logger.info("正在写配置config.json")
        with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                config['rosterId'] = rosterId[0]
                config['access_token'] = access_token[0]
                config['studentName'] = studentName[0]
        with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)
        logger.info("配置文件写入完成")
        return True
    else:
        logger.error("发送请求成功，获取令牌失败")
        logger.error("错误信息："+json_data['message'])
        return False
    # else:
        # logger.error("发送请求失败，网络配置请检查")
        # logger.error("错误信息是："+r.text)
        # return False


if __name__ == '__main__':
    logger.error("请直接调用而不是执行")
    exit()
