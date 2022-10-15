from cgitb import handler
import http
import requests
import json
import os
import logging
import random
import time
import sys
import codecs
import logging.handlers

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter(
    '[%(asctime)s] - [%(levelname)s]- %(message)s', '%Y-%m-%d %H:%M:%S')  # 添加cmd handler
# cmd_handler = logging.StreamHandler(sys.stdout)
# cmd_handler.setLevel(logging.DEBUG)
# cmd_handler.setFormatter(fmt)
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
# logger.addHandler(cmd_handler)
logger.addHandler(file_handler)


def read_push_config():
    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    stk = config['stk']
    sender = config['sender']
    receiver = config['receiver']
    way = config['way']
    isSendToGroup = config['isSendToGroup']
    # pusher_api=config['pusher_api']
    return stk, sender, receiver, way, isSendToGroup


stk, sender, receiver, way, isSendToGroup = read_push_config()


def send_msg(msg, way=way):
    if way == 'qq':
        logger.info('向QQ推送'+msg)
        send_qq_msg(msg)
    elif way == 'wx':
        logger.info('向微信推送'+msg)
        send_wx_msg(msg)
    elif way == 'dd':
        logger.info('向钉钉推送'+msg)
        send_dd_msg(msg)
    elif way == 'qywx':
        logger.info('向企业微信推送'+msg)
        send_qywx_msg(msg)
    else:
        pass

# # 透过系统时间获取今天的日期
# localDate = time.strftime('%Y-%m-%d', time.localtime())


def send_qq_msg(msg):
    global stk, sender, receiver, isSendToGroup
    # msg=msg+'\n'
    if isSendToGroup == 'True':

        s_ep = 'group_id='
    else:
        s_ep = 'user_id='
    requests.packages.urllib3.disable_warnings()
    pusher_api = "https://api.5i03.cn/api/push/qq/"+sender+'/'+stk+'/'+'send_msg'
    q = requests.post(pusher_api+'?' + s_ep + receiver +
                      '&message='+msg, verify=False)
    logger.info('推送服务回应:'+msg+q.text)


def send_wx_msg(msg):
    global stk, sender, receiver
    print('developing...')


def send_dd_msg(msg):
    global stk, sender, receiver
    print('developing...')


def send_qywx_msg(msg):
    global stk, sender, receiver
    print('developing...')


if __name__ == '__main__':
    logger.error('推送模块不可被直接执行')
