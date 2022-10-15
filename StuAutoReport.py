# coding:utf-8
import codecs
# from configs import *
import json
import logging
# import urllib.request
import os
import random
import sys
import time
# import jsonpath
import requests
import argparse
import random
import logging.handlers
import sys
import msgSender
# from tencentcloud.common import credential
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.ocr.v20181119 import ocr_client, models
# import op_config
# from configs import *
# import demjson
# 预防中文导致报错，规范输出为utf8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# 日志服务初始化


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

# 透过系统时间获取今天的日期
localDate = time.strftime('%Y-%m-%d', time.localtime())
# def is_config_json_exist():
# is_config_json_exist
# 本函数用于检查config.json文件是否存在
# global config_file
# if os.path.isfile(config_file):
#     logger.info("配置文件已经存在")
#     return True
# else:
#     logger.info("配置文件并不存在")
#     # download file from 5i03.cn and wirted to config.json in current dir
#     logger.info("正在开始下载配置文件")
#     download_config_json()
#     logger.info("配置下载完成已经执行")
#     return False


def read_config():
    # 读取配置文件config.json 读取学生名字，健康日报名册ID，和访问令牌,和填报用的数据
    with open(os.path.normpath(sys.path[0]+'/config.json'), 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    rosterId = config['Id']
    accessToken = config['accessToken']
    studentName = config['Name']
    sendHost = config['sendHost']
    isGfxReturn = config['isGfxReturn']
    isJwReturn = config['isJwReturn']
    isContactPatient = config['isContactPatient']
    isContactRiskArea = config['isContactRiskArea']
    isHealthCodeOk = config['isHealthCodeOk']
    isSick = config['isSick']
    details = config['details']
    liveState = config['liveState']
    nowAddress = config['nowAddress']
    nowAddressDetail = config['nowAddressDetail']
    nowTiwenState = config['nowTiwenState']
    nowHealthState = config['nowHealthState']
    temperature = config['temperature']
    sender = config['sender']
    stk = config['stk']
    receiver = config['receiver']
    Name = config['Name']
    # assert isinstance(send_hosts, object)
    return rosterId, accessToken, studentName, sendHost, \
        isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, \
        isHealthCodeOk, isSick, details, liveState, nowAddress, \
        nowAddressDetail, nowTiwenState, nowHealthState, temperature, \
        sender, stk, receiver, Name


rosterId, accessToken, studentName, sendHost, isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, isHealthCodeOk, isSick, details, liveState, nowAddress, nowAddressDetail, nowTiwenState, nowHealthState, temperature, sender, stk, receiver, Name = read_config()
baseURL = "https://" + sendHost
userAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac"
s_Header = {
    "Host": sendHost,
    "Content-Type": "application/json",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": userAgent,
    "accessToken": accessToken,
    "Referer": "https://servicewechat.com/wx56b1d7357f3df890/25/page-frame.html",
    # "Content-Length":"19"
    # "Content-Length": "null"
}
# which path i am in
# task_save_2 = os.path.normpath(sys.path[0] + '/task/')
dataDate = "dataDate=" + localDate
msg = ''


# task_file_to_operate=str(rosterId + "_" + localDate + '_task_list.json', encoding='utf8')
taskSaveTo = os.path.normpath(
    sys.path[0] + '/task/' + rosterId + '_' + localDate + '_task_list.json')


def getTodayTaskList():
    global rosterId, taskSaveTo
    try:
        if os.path.isfile(taskSaveTo):
            logger.info("今日任务文件已存在,跳过下载")
            return True
        else:
            logger.info("今日任务文件不存在,开始下载")
            downloadTaskList()
            logger.info("今日任务已下载完成，开始处理")
            return True
    except Exception as e:
        logger.error(e)
        return False


def downloadTaskList():
    # downloadTaskList
    # 本函数用于下载当天任务的原始文件
    # send_data_for_task_list = {
    #     "page": "1",
    #     "rows": "9"
    # }
    global baseURL, rosterId, healthId, localDate, file_rs, taskSaveTo
    try:
        task_list_epurl = baseURL + "/api/mStuApi/queryByStuEpidemicHealthReport.do"
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url=task_list_epurl, headers=s_Header,
                         data={
                             "page": "1",
                             "rows": "9"
                         }, timeout=30)
        with open(taskSaveTo, 'w+', encoding='utf-8') as f:
            f.write(r.text)
            f.close()
        return True
    except Exception as e:
        logger.error(e)
        return False


def preReadTaskJson(dataType):
    global baseURL, s_Header, dataDate, rosterId, isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, isHealthCodeOk, isSick, details, liveState, nowAddress, nowAddressDetail, nowTiwenState, nowHealthState, temperature, Name
    try:
        logger.info('开始读取并处理本地缓存的任务数据')
        with open(taskSaveTo, encoding='utf8') as json_file:
            jsonData = json.load(json_file)
        if dataType == 1:
            logtype = "早报"
        elif dataType == 2:
            logtype = "午报"
        elif dataType == 3:
            logtype = "晚报"
        else:
            logtype = "未知"
            logger.error('无法识别的任务类型%d请提交issue' % dataType)
            exit()
        logger.info('开始处理'+logtype+'任务')
        for i in range(0, 3):
            if jsonData['rows'][i]['dataType'] == str(dataType):
                healthId = jsonData['rows'][i]['healthId']
                endTime = jsonData['rows'][i]['endTime']
                logger.info('发现:开始于'+endTime+'的'+logtype + '(' + healthId+') ')
                if jsonData['rows'][i]['dataStatus'] == '1':
                    logger.info("该任务未被提交，开始健康上报日报")
                    postDataToServer(healthId, dataType, endTime, logtype)
                    return True
                else:
                    logger.error("该任务已被提交，请确认日报情况")
                    pass
                    return False
            else:

                logger.error("未找到"+logtype+"任务，请确认日报情况")
                pass
    except Exception as e:
        logger.error(e)
        return False


def postDataToServer(healthId, dataType, endTime, logtype):
    try:
        sendDatas = {'healthId': healthId,
                     'rosterId': rosterId,
                     'isGfxReturn': isGfxReturn,  # 是否高风险返回 2为否
                     'isJwReturn': isJwReturn,  # 是否境外返回 2为否
                     'isContactPatient': isContactPatient,  # 是否接触确诊，疑似，无症状感染者 2为否
                     'isContactRiskArea': isContactPatient,  # 是否时空伴随 2为否
                     'isHealthCodeOk': isHealthCodeOk,  # 健康码是不是绿色的 为
                     'isSick': isSick,  # 是否有发热症状
                     'details': dataDate,
                     'dataType': dataType,
                     'dataStatus': '2',
                     'endTime': endTime,
                     'liveState': liveState,
                     'nowAddress': nowAddress,
                     'nowAddressDetail': nowAddressDetail,
                     'nowTiwenState': nowTiwenState,
                     'nowHealthState': nowHealthState,
                     'counsellorApprovalStatus': '未审核',
                     'temperature': temperature
                     }
        requests.packages.urllib3.disable_warnings()
        report_epurl = baseURL + \
            '/api/mStuApi/updateHealthReportEpidemicHealthReport.do'
        r = requests.post(url=report_epurl,
                          headers=s_Header, params=sendDatas, verify=False)
        if r.status_code == 200:

            json_data = json.loads(r.text)
            if json_data['isSuccess'] == True:
                logger.info(str(logtype) + "任务提交成功")
                msgSender.send_msg(Name+"的健康励园" + str(logtype) + "上报成功")
            else:
                logger.error(str(logtype) + "上报失败")
                msgSender.send_msg(Name+"的健康励园" + str(logtype) +
                                   '因'+json_data['message'] + "上报失败")
                logger.error("错误信息:" + json_data['message'])
    except Exception as e:
        logger.error(e)
        msgSender.send_msg(Name+"的健康励园" + str(logtype) + "上报失败")
        pass

def main():
    read_config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=int, default=0,
                        help='上报类型,1为早报,2为午报,3为晚报,默认为0为全部上报')
    args = parser.parse_args()

    if getTodayTaskList() == True:
        logger.info("任务列表获取成功")
        # if time.strftime('%H:%M', time.localtime()) >= '00:15' and time.strftime('%H:%M', time.localtime()) <= '10:00':
        if args.type == 0:
            preReadTaskJson(1)
            time.sleep(random.randint(1, 5))
            preReadTaskJson(2)
            time.sleep(random.randint(1, 5))
            preReadTaskJson(3)
            time.sleep(random.randint(1, 5))
        elif args.type == 1:
            preReadTaskJson(1)
        elif args.type == 2:
            preReadTaskJson(2)
        elif args.type == 3:
            preReadTaskJson(3)

    else:
        logging.info("任务列表不在本地,正在尝试下载")
        downloadTaskList()


if __name__ == '__main__':
    if rosterId == "" or accessToken == "" or studentName == "":
        logger.error("无令牌配置请手动填写或运行TokenHelper来获取")
        read_config()
        exit()
    else:
        logger.info('=' * 3 + localDate + studentName+'的签到任务开始执行' + '=' * 3)
        read_config()
        main()
        logger.info('=' * 3 + localDate + studentName+'的签到任务执行完毕' + '=' * 3)
else:
    logger.error("请直接执行而不是调用")
    exit()
