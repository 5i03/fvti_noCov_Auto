
import codecs
import json
import logging
import os
import requests
import argparse
import random
import sys
import msgSender
import logging.handlers
from urllib.parse import urlencode
###############################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(
    '[%(asctime)s] - [%(levelname)s]- %(message)s', '%Y-%m-%d %H:%M:%S')  # 添加cmd handler
cmd_handler = logging.StreamHandler(sys.stdout)
cmd_handler.setLevel(logging.DEBUG)
cmd_handler.setFormatter(fmt)
# logpath = os.path.join(os.getcwd(), 'run.log')
# file_handler = logging.FileHandler(logpath)
file_handler = logging.FileHandler(os.path.join(os.getcwd(), 'run.log'))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(fmt)
http_handler = logging.handlers.HTTPHandler(
    r"api.5i03.cn", "/api/logs/push", "GET", secure=False)
http_handler.setLevel(logging.DEBUG)
http_handler.setFormatter(fmt)
logger.addHandler(http_handler)
logger.addHandler(cmd_handler)
logger.addHandler(file_handler)

msg=''
# 获取令牌接口学生和教师通用
def get_tk(Username, Password, role):
    # 获取令牌接口 api.5i03.cn
    global s_header, msg
    try:
        to_req = urlencode({'userCode': Username, 'userPwd': Password, 'role': role})
        logger.info('自动令牌更新开始执行')
        req_tk = requests.packages.urllib3.disable_warnings()
        req_tk = requests.get('https://api.5i03.cn/api/fvti/get_tk?' +
                              to_req, verify=False)
        json_data = json.loads(req_tk.text)
        accessToken = json_data['data']['accessToken']
        # print(accessToken)
        if json_data['isSuccess'] == True:
            logger.info("获取令牌成功")
            if role == 'Teacher':
                Id = json_data['data']['teacherId']
                Name = json_data['data']['teacherName']
                logger.info("教师鉴权成功 "+str(Name)+' ID: ' +
                            str(Id)+' 令牌 '+str(accessToken))
            elif role == 'Student':
                Id = json_data['data']['studentId']
                Name = json_data['data']['studentName']
                logger.info("学生鉴权成功 "+str(Name)+' ID: ' +
                            str(Id)+' 令牌: '+str(accessToken))
            logger.info("正在写入配置文件")

            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
                config['Id'] = Id
                config['accessToken'] = accessToken
                config['Name'] = Name
            with open('config.json', 'w+', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False)
            logger.info("配置文件写入完成")
            msg=msg+str('教师'if role == 'Teacher' else '学生')+"鉴权并保存成功 \n Name: "+str(Name)+' ID: '+str(Id) +' Token: '+str(accessToken)
            # msgSender.sendMsg(msg)
            logger.info(msg)
        else:
            err_msg = json_data['message']
            logger.info("令牌获取失败 错误信息: "+err_msg)
        return True
    except Exception as e:
        logger.error(e)
        return False


def read_config():
    with open(os.path.normpath(sys.path[0]+'/config.json'), 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    accessToken = config['accessToken']
    Name = config['Name']
    Username = config['Username']
    Password = config['Password']
    role = config['role']

    return accessToken, Name, Username, Password, role


accessToken, Name, Username, Password, role = read_config()

if __name__ == '__main__':
    if get_tk(Username, Password, role) == True:
        logger.info("自动获取令牌完成")
    else:
        logger.info("自动获取令牌失败")
