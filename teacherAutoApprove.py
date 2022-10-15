# coding:utf-8
# author: 5i03
# email:cnyue@5i03.cn
# website(China Mainland):www.5i03.cn
# website(international):www.5i03.net
import codecs
import json
import logging
import os
import random
import sys
import time
import requests
import argparse
import random
import SQLiteOperator
import msgSender
import logging.handlers
import TokenHelper
# import sqlite3


# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

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
msg = ''


def read_config():
    with open('config.json', 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    accessToken = config['accessToken']
    Name = config['Name']
    sendHost = config['sendHost']
    Username = config['Username']
    Password = config['Password']
    role = config['role']
    stk = config['stk']
    sender = config['sender']
    receiver = config['receiver']
    way = config['way']
    # pusher_api=config['pusher_api']
    # assert isinstance(send_hosts, object)
    return accessToken, Name, sendHost, Username, Password, role, stk, sender, receiver, way


accessToken, Name, sendHost, Username, Password, role, stk, sender, receiver, way = read_config()



# ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac"
# at =read_config()
s_header = {
    "Host": sendHost,
    "Content-Type": "application/json",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac", 
    "accessToken": accessToken,
    "Referer": "https://servicewechat.com/wx56b1d7357f3df890/25/page-frame.html",
    # "Content-Length": "null"
}


def queryByCounsellorMobileOutInSchool():
    global s_header
    # try:
    s = requests.packages.urllib3.disable_warnings()
    s = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryByCounsellorMobileOutInSchool.do?currOutApprovalStatus=未审核',
                     headers=s_header, verify=False)
    s_json = json.loads(s.text)
    logger.info('抓取到'+str(len(s_json['rows']))+'条数据')
    for i in range(0, len(s_json['rows'])):
        outInSchoolId = s_json['rows'][i]['outInSchoolId']
        studentName = s_json['rows'][i]['studentName']
        studentCode = s_json['rows'][i]['studentCode']
        destination = s_json['rows'][i]['destination']
        travelPlan = s_json['rows'][i]['travelPlan']
        grade_majorName = str(
            s_json['rows'][i]['grade'])+s_json['rows'][i]['majorName']
        goOutReason = s_json['rows'][i]['goOutReason']
        outSchoolDateRange = s_json['rows'][i]['outSchoolDate']+' ' + \
            s_json['rows'][i]['outSchoolStartRange'] + \
            '-'+s_json['rows'][i]['outSchoolEndRange']
        enterSchoolRange = s_json['rows'][i]['enterSchoolDate']+' ' + \
                s_json['rows'][i]['enterSchoolStartRange'] + \
                '-'+s_json['rows'][i]['enterSchoolEndRange']
        logger.info('发现:'+grade_majorName+' '+studentName+'('+studentCode+') 在'+outSchoolDateRange+' - '+enterSchoolRange + \
                '因'+goOutReason+' 前往 '+destination+' '+travelPlan + \
                ' 的 ' +'('+outInSchoolId+')'+s_json['rows'][i]['currEnterApprovalStatus'])
        if s_json['rows'][i]['goOutType'] == '1':
            
            ot = '市内当日往返计划'
            logger.info('处理:'+grade_majorName+' '+studentName+'('+studentCode+') 在'+outSchoolDateRange+' - '+enterSchoolRange + \
                '因'+goOutReason+' 前往 '+destination+' '+travelPlan + \
                ' 的 ' + ot+'('+outInSchoolId+')成功\n')
            approve_out_in_school(outInSchoolId, studentName,
                                  ot, studentCode, destination, travelPlan, grade_majorName, outSchoolDateRange, enterSchoolRange, goOutReason)
        else:
            ot = '非市内当日往返'
            logger.info('处理:'+s_json['rows'][i]['studentName']+'('+s_json['rows'][i]['studentCode']+')的'+s_json['rows'][i]
                        ['outInSchoolId']+'|'+ot+s_json['rows'][i]['currEnterApprovalStatus'])
            logger.error('错误:'+s_json['rows'][i]['studentName']+'('+s_json['rows'][i]['studentCode']+')的'+s_json['rows'][i]
                         ['outInSchoolId']+''+ot+'忽略')

    # except Exception as e:
    #     logger.error(e)


def approve_out_in_school(outInSchoolId, studentName, ot, studentCode, destination, travelPlan, grade_majorName, outSchoolDateRange, enterSchoolRange, goOutReason):
    global msg
    try:
        r = requests.packages.urllib3.disable_warnings()
        time.sleep(random.randint(1, 3))
        r = requests.post(
            url='https://health.fvti.linyisong.top/api/mTeaApi/saveByTeaOutInSchool.do?outInSchoolId=' +
            outInSchoolId+'&approvalStatus=审核通过&isNeedNext=否&nextApprovalStatusId=&flag=1&outInApprovalId=',
            headers=s_header, verify=False)
        r_json = json.loads(r.text)

        if r_json['isSuccess'] == True:
            logger.info('审核:'+studentName+'('+studentCode+')的' +
                        destination+travelPlan+ot+'('+outInSchoolId+')同意成功')
            msg = msg+''+grade_majorName+' '+studentName+'('+studentCode+') 在'+outSchoolDateRange+' - '+enterSchoolRange + \
                '因'+goOutReason+' 前往 '+destination+' '+travelPlan + \
                ' 的 ' + ot+'('+outInSchoolId+')自动审核成功\n'
            msgSender.send_msg(msg)
    except Exception as e:
        logger.error(e)
        logger.error('审核:'+studentName+'('+studentCode+')的' +
                     ot+'('+outInSchoolId+')失败')
        msg = msg+'\n'+studentName+'('+studentCode+')前往'+destination+' '+travelPlan+'的' + \
            ot+'('+outInSchoolId+')自动审核通过失败\n'



def main():
    read_config()

    # time.sleep(random.randint(1, 3))
    queryByCounsellorMobileOutInSchool()


if __name__ == '__main__':
    main()
