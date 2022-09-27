# coding:utf-8
import codecs
from distutils.command.config import config
# from configs import *
import json
import logging
# import urllib.request
import os
from random import random
import sys
import time
import jsonpath
import requests
import argparse
import random
import get_token

# from configs import *
# import demjson
# 预防中文导致报错，规范输出为utf8
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
# 日志服务初始化
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='report.log')
logger = logging.getLogger(__name__)
# 透过系统时间获取今天的日期
localDate = time.strftime('%Y-%m-%d', time.localtime())


def read_config():
    # 读取配置文件config.json 读取学生名字，健康日报名册ID，和访问令牌,和填报用的数据
    with open('config.json', encoding='utf8') as json_file:
        config = json.load(json_file)
    rosterId = config['rosterId']
    access_token = config['access_token']
    studentName = config['studentName']
    send_hosts = config['send_hosts']
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
    # assert isinstance(send_hosts, object)
    return rosterId, access_token, studentName, send_hosts, \
        isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, \
        isHealthCodeOk, isSick, details, liveState, nowAddress, \
        nowAddressDetail, nowTiwenState, nowHealthState, temperature


rosterId, access_token, studentName, send_hosts, isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, isHealthCodeOk, isSick, details, liveState, nowAddress, nowAddressDetail, nowTiwenState, nowHealthState, temperature = read_config()
baseURL = "https://" + send_hosts
user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac"
send_header = {
    "Host": send_hosts,
    "Content-Type": "application/json",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": user_agent,
    "accessToken": access_token,
    "Referer": "https://servicewechat.com/wx56b1d7357f3df890/25/page-frame.html",
    # "Content-Length":"19"
    # "Content-Length": "null"
}
# which path i am in
wpiai = sys.path[0]
task_save_2 = wpiai + "/task/"
dataDate = "dataDate=" + localDate


# task_file_to_operate=str(rosterId + "_" + localDate + '_task_list.json', encoding='utf8')


def get_today_list():
    global rosterId, task_save_2
    if os.path.isfile(task_save_2 + rosterId + '_' + localDate + '_task_list.json'):
        logger.info("今日任务文件已存在,跳过下载")
        return True
    else:
        logger.info("今日任务文件不存在,开始下载")
        download_task_list()
        logger.info("今日任务已下载完成，开始处理")
        return True


def download_task_list():
    # download_task_list
    # 本函数用于下载当天任务的原始文件
    send_data_for_task_list = {
        "page": "1",
        "rows": "9"
    }
    global baseURL, rosterId, healthId, localDate, file_rs, task_save_2
    task_list_epurl = baseURL + "/api/mStuApi/queryByStuEpidemicHealthReport.do"
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url=task_list_epurl, headers=send_header,
                     data=send_data_for_task_list, verify=False, timeout=30)
    with open(task_save_2 + rosterId + "_" + localDate + "_task_list.json", 'w+', encoding='utf-8') as f:
        f.write(r.text)
        f.close()
    return True


def report_data_for_task(dataType):
    global baseURL, send_header, dataDate, rosterId, isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, isHealthCodeOk, isSick, details, liveState, nowAddress, nowAddressDetail, nowTiwenState, nowHealthState, temperature
    with open(task_save_2 + rosterId + "_" + localDate + '_task_list.json', encoding='utf8') as json_file:
        config = json.load(json_file)
    if dataType == 1:
        logger.info("开始处理早报任务")
        logtype = "早报"
        healthId = jsonpath.jsonpath(config, "$.rows[0].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[0].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[0].dataType")
    elif dataType == 2:
        logger.info("开始处理午报任务")
        logtype = "午报"
        healthId = jsonpath.jsonpath(config, "$.rows[1].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[1].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[1].dataType")
    elif dataType == 3:
        logger.info("开始处理晚报任务")
        logtype = "晚报"
        healthId = jsonpath.jsonpath(config, "$.rows[2].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[2].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[2].dataType")
    else:
        logger.error("不支持的任务类型,请提交issue反馈")
        exit()
    send_datas = {'healthId': healthId,
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
                      headers=send_header, params=send_datas, verify=False)
    # q=demjson.decode(r.text)
    # print(r.text)
    # logger.info(r.text)
    json_data = json.loads(r.text)
    if json_data['isSuccess'] == True:
        logger.info("任务" + str(logtype) + "上报成功")
    else:
        logger.error("任务" + str(logtype) + "上报失败")
        logger.error("错误信息:" + json_data['message'])


def main():
    read_config()
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', type=int, default=0,
                        help='上报类型,1为早报,2为午报,3为晚报,默认为0为全部上报')
    args = parser.parse_args()

    if get_today_list() == True:
        # if time.strftime('%H:%M', time.localtime()) >= '00:15' and time.strftime('%H:%M', time.localtime()) <= '10:00':
        # report_data_for_task(1)
        # if time.strftime('%H:%M', time.localtime()) >= '10:00' and time.strftime('%H:%M', time.localtime()) <= '17:00':
        # report_data_for_task(2)
        # if time.strftime('%H:%M', time.localtime()) >= '17:00' and time.strftime('%H:%M', time.localtime()) <= '23:59':
        # report_data_for_task(3)
        if args.type == 0:
            report_data_for_task(1)
            time.sleep(random.randint(1, 5))
            report_data_for_task(2)
            time.sleep(random.randint(1, 5))
            report_data_for_task(3)
            time.sleep(random.randint(1, 5))
        elif args.type == 1:
            report_data_for_task(1)
        elif args.type == 2:
            report_data_for_task(2)
        elif args.type == 3:
            report_data_for_task(3)

    else:
        logging.info("任务列表不在本地,正在尝试下载")
        download_task_list()
        main()
        return 0


if __name__ == '__main__':
    if rosterId == "" or access_token == "" or studentName == "":
        logger.error("config.json中未找到令牌 正在引导获得令牌")
        get_token.get_token()
        read_config()
    else:
        logger.info('=' * 3 + localDate + studentName+'的签到任务开始执行' + '=' * 3)
        read_config()
        main()
        logger.info('=' * 3 + localDate + studentName+'的签到任务执行完毕' + '=' * 3)
else:
    logger.error("请直接执行而不是调用")
    exit()
