import argparse
import requests
import json
import time
import datetime
import os
import sys
import re
import random
import urllib3
import logging
import requests
import logging.handlers
import codecs
import threading
import msgSender
import SQLiteOperator
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
msg = ''
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


def read_config():
    with open(os.path.normpath(sys.path[0]+'/config.json'), 'r', encoding='utf8') as json_file:
        config = json.load(json_file)
    accessToken = config['accessToken']
    Name = config['Name']
    Username = config['Username']
    Password = config['Password']
    role = config['role']
    sendHost = config['sendHost']

    return accessToken, Name, Username, Password, role, sendHost


accessToken, Name, Username, Password, ro, sendHost = read_config()


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_date():
    return time.strftime("%Y-%m-%d", time.localtime())


def get_time_stamp():
    return int(time.time())


def get_time_stamp_13():
    return int(round(time.time() * 1000))


def get_time_stamp_10():
    return int(time.time())


ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E217 MicroMessenger/6.8.0(0x16080000) NetType/WIFI Language/en Branch/Br_trunk MiniProgramEnv/Mac"
# at =read_config()
s_header = {
    "Host": sendHost,
    "Content-Type": "application/json",
    "Accept-Language": "zh-cn",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "User-Agent": ua,
    "accessToken": accessToken,
    "Referer": "https://servicewechat.com/wx56b1d7357f3df890/25/page-frame.html",
    # "Content-Length": "null"
}


def getDataTypeNotReport():
    global msg
    try:
        urllib3.disable_warnings()
        logger.info("正在尝试获取当天晨报的班级的汇报情况")
        rb = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/querytotalListByCounsellorEpidemicHealthReport.do?dataDate=' +
                          get_date()+'&dataType=1', headers=s_header, verify=False)
        rb_json = json.loads(rb.text)
        # print(rb_json)
        logger.info('晨报总计:'+str(rb_json['total'])+' 个班级')

        for i in range(0, rb_json['total']):
            msg = ''
            logger.info('正在尝试获取早报第'+str(i+1)+'个班级')
            if 'nofill' in rb_json['rows'][i]:
                logger.info('班级:'+rb_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
                    rb_json['rows'][i]['nofill'])+' 编码:' + rb_json['rows'][i]['executiveClassId'])
                re = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryFillDetailByExecutiveClassEpidemicHealthReport.do?dataDate=' +
                                  get_date()+'&dataType=1&executiveClassId='+rb_json['rows'][i]['executiveClassId']+'&page=1&rows=128', headers=s_header, verify=False)
                re_json = json.loads(re.text)
                msg='\n早报:\n'
                for k in range(0, re_json['total']):
                    
                    logger.info(re_json['rows'][k]['studentName'] +
                                '(' + re_json['rows'][k]['studentCode']+')早报未报')
                    msg = msg+' '+re_json['rows'][k]['studentName']
                    # print(msg)
                logger.info('班级:'+rb_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
                    rb_json['rows'][i]['nofill'])+' 编码:' + rb_json['rows'][i]['executiveClassId'])
                re = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryFillDetailByExecutiveClassEpidemicHealthReport.do?dataDate=' +
                                  get_date()+'&dataType=2&executiveClassId='+rb_json['rows'][i]['executiveClassId']+'&page=1&rows=128', headers=s_header, verify=False)
                re_json = json.loads(re.text)
                msg=msg+'\n午报:\n'
                for k in range(0, re_json['total']):
                    logger.info(re_json['rows'][k]['studentName'] +
                                '(' + re_json['rows'][k]['studentCode']+')午报未报')
                    msg = msg+' '+re_json['rows'][k]['studentName'] 
                # print(msg)
                logger.info('班级:'+rb_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
                    rb_json['rows'][i]['nofill'])+' 编码:' + rb_json['rows'][i]['executiveClassId'])
                re = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryFillDetailByExecutiveClassEpidemicHealthReport.do?dataDate=' +
                                  get_date()+'&dataType=3&executiveClassId='+rb_json['rows'][i]['executiveClassId']+'&page=1&rows=128', headers=s_header, verify=False)
                re_json = json.loads(re.text)
                msg=msg+'\n晚报:\n'
                for k in range(0, re_json['total']):
                    logger.info(re_json['rows'][k]['studentName'] +
                                '(' + re_json['rows'][k]['studentCode']+')晚报未报')
                    msg = msg+' '+re_json['rows'][k]['studentName']
                msg=rb_json['rows'][i]['executiveClassName']+'\n未填学生姓名:'+msg
                msgSender.send_msg(msg)
            else:
                logger.info('班级:'+rb_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
                    'NULL')+' 编码:' + rb_json['rows'][i]['executiveClassId'])
                msg = msg+re_json['rows'][k]['executiveClassName']+'\n'+rb_json['rows'][i]['executiveClassId']+'\n'+re_json['rows'][k]['studentName'] + \
                        '(' + re_json['rows'][k]['studentCode']+')早报未报\n'
                pass
    except Exception as err:
        logger.error(err)


# def getDataType2NotReport():
#     global s_header
#     try:
#         urllib3.disable_warnings()
#         logger.info("正在尝试获取当天午报的班级的汇报情况")
#         rc = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/querytotalListByCounsellorEpidemicHealthReport.do?dataDate=' +
#                           get_date()+'&dataType=2', headers=s_header, verify=False)
#         rc_json = json.loads(rc.text)
#         logger.info('午报总计:'+str(rc_json['total'])+' 个班级')
#         for i in range(0, rc_json['total']):
#             logger.info('正在尝试获取午报第'+str(i+1)+'个班级的信息')
#             logger.info('班级:'+rc_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
#                 rc_json['rows'][i]['nofill'])+' 编码:' + rc_json['rows'][i]['executiveClassId'])
#             re = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryFillDetailByExecutiveClassEpidemicHealthReport.do?dataDate=' +
#                               get_date()+'&dataType=2&executiveClassId='+rc_json['rows'][i]['executiveClassId']+'&page=1&rows=128', headers=s_header, verify=False)
#             re_json = json.loads(re.text)
#             for k in range(0, re_json['total']):
#                 logger.info(re_json['rows'][k]['studentName'] +
#                             '(' + re_json['rows'][k]['studentCode']+')未报')
#     except Exception as err:
#         logger.error(err)


# def getDataType3NotReport():
#     try:
#         logger.info("正在尝试获取当天晚报的班级的汇报情况")
#         rd = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/querytotalListByCounsellorEpidemicHealthReport.do?dataDate=' +
#                           get_date()+'&dataType=3', headers=s_header, verify=False)
#         rd_json = json.loads(rd.text)
#         logger.info('晚报总计:'+str(rd_json['total'])+' 个班级')
#         for i in range(0, rd_json['total']):
#             logger.info('正在尝试获取晚报第'+str(i+1)+'个班级的信息')
#             logger.info('班级:'+rd_json['rows'][i]['executiveClassName'] + ' 未填:'+str(
#                 rd_json['rows'][i]['nofill'])+' 编码:' + rd_json['rows'][i]['executiveClassId'])
#             re = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/queryFillDetailByExecutiveClassEpidemicHealthReport.do?dataDate=' +
#                               get_date()+'&dataType=3&executiveClassId='+rd_json['rows'][i]['executiveClassId']+'&page=1&rows=128', headers=s_header, verify=False)
#             re_json = json.loads(re.text)
#             # sql='insert into '+re_json['rows'][i]['executiveClassName']+ ' values '
#             # SQLiteOperator.sql_query(sql,'STUDENT')
#             for k in range(0, re_json['total']):
#                 logger.info(re_json['rows'][k]['studentName'] + '(' +
#                             re_json['rows'][k]['studentCode']+')未报')

    # except Exception as err:
        # logger.error(err)
        # logger.info("正在尝试获取当天的未填写的学生的信息")


def getSummaryAll():
    try:
        urllib3.disable_warnings()
        logger.info("正在尝试获取当天的总计")
        ra = requests.get('https://health.fvti.linyisong.top/api/mTeaApi/querytotalByCounsellorEpidemicHealthReport.do?dataDate=' +
                          get_date(), headers=s_header, verify=False)
        ra_json = json.loads(ra.text)
        nofill1 = str(ra_json['rows'][0]['nofill'])
        # fill1=str(ra_json['rows'][0]['fill'])
        fillNum1 = str(ra_json['rows'][0]['fillNum'])
        nofill2 = str(ra_json['rows'][1]['nofill'])
        # fill2=str(ra_json['rows'][1]['fill'])
        fillNum2 = str(ra_json['rows'][1]['fillNum'])
        nofill3 = str(ra_json['rows'][2]['nofill'])
        # fill3=str(ra_json['rows'][2]['fill'])
        fillNum3 = str(ra_json['rows'][2]['fillNum'])
        logger.info('晨报:'+' '+nofill1+' / '+fillNum1+'人 午报'+' '+nofill2 +
                    ' / '+fillNum2+'人 晚报'+nofill3+' / '+fillNum3+'人 未填/总计')
        msg = '当前日报填写情况(未填/总计)\n'+'晨报:'+nofill1+' / '+fillNum1+'\n午报:' + \
            nofill2+' / '+fillNum2+'\n晚报:'+nofill3+' / '+fillNum3+''
        msgSender.send_msg(msg)
    except Exception as e:
        logger.error(e)
        nofill1 = 'NULL'
        nofill2 = 'NULL'
        nofill3 = 'NULL'
        logger.info('晨报:'+nofill1+'人 午报'+nofill2+'人 晚报'+nofill3+'人 未填写')
        msg = '晨报:'+nofill1+'人 午报'+nofill2+'人 晚报'+nofill3+'人 未填写'
        msgSender.send_msg(msg)


if __name__ == '__main__':
    try:
        # getSummaryAll()
        getDataTypeNotReport()
        # getDataType2NotReport()
        # getDataType3NotReport()
        # sendNotification()
        # get_summary_all()
    except Exception as err:
        logger.error(err)
