# coding:utf-8
import codecs
import json
import logging
import os
import random
from re import S
import sys
import time
from wsgiref import headers
import jsonpath
import requests
import argparse
import random
import send_msg

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='report.log')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='script_log.log')
logger = logging.handlers.HTTPHandler()
logger = logging.getLogger(__name__)
# 透过系统时间获取今天的日期
localDate = time.strftime('%Y-%m-%d', time.localtime())

with open('cookie.json', 'r', encoding='utf-8') as f:
    cookie = json.load(f)
    jsid = cookie['value']
if cookie['value'] == '':
    # longin_as_human.begain_selenium('edge', '2017010553', '094557')
    print('cookie is empty')
    exit()
else:
    SESSION_ID = jsid
hearders = {
    "Host": "health.fvti.linyisong.top",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "http://health.fvti.linyisong.top",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Referer": "http://health.fvti.linyisong.top/main.do",
    "Cookie": "JSESSIONID="+SESSION_ID
}

def qioandappr(slipt):
    global headers
    data = {
        "enterSchoolDate": "",
        "outSchoolDate": "",
        "student.studentCode": "",
        "student.studentName": "",
        "student.major.majorId": "",
        "student.executiveClazz.executiveClassName": "",
        "student.grade": "",
        "goOutType": "1",
        "destinationProvince": "",
        "destinationCity": "",
        "destinationArea": "",
        "outStatus": "",
        "enterStatus": "",
        "page": 1,
        "rows": slipt
    }
    print('设定限制处理'+str(slipt)+'条数据')
    requests.packages.urllib3.disable_warnings()
    response = requests.post(
        "http://health.fvti.linyisong.top/outInSchool/queryCounsellorOutInSchool.do", data=data, headers=hearders)
    response = json.loads(response.text)
    print('共有'+str(len(response['rows']))+'条数据')
    for (i) in range(0, len(response['rows'])):

        if response['rows'][i]['currEnterApprovalStatus'] == '审核通过':
            continue
        else:
            print('正在处理第'+str(i+1)+'条数据')
            print('学生：'+response["rows"][i]['studentName']+'('+response["rows"]
                  [i]['studentCode']+')的'+response["rows"][i]['outInSchoolId']+'前往'+response["rows"][i]['destination']+'未被审核')
            requests.packages.urllib3.disable_warnings()
            oisid = str(response["rows"][i]['outInSchoolId'])
            data_2_appr = {

                'ids': oisid,
                'approvalStatus': '审核通过',
                'isNeedNext': '否',
                'outInApprovalId': ''
            }
            appr_req = requests.post(
                "http://health.fvti.linyisong.top/outInSchool/mulSaveByTeaOutInSchool.do", data=data_2_appr, headers=hearders)
            # print(appr_req.text)
            appr_res = json.loads(appr_req.text)
            # print(str(appr_res['isSuccess']))
            if str(appr_res['isSuccess']) == 'True':
                print('学生：'+response["rows"][i]['studentName']+'('+response["rows"]
                      [i]['studentCode']+')的'+response["rows"][i]['outInSchoolId']+'前往'+response["rows"][i]['destination']+'审核成功')

            else:
                print('学生：'+response["rows"][i]['studentName']+'('+response["rows"]
                      [i]['studentCode']+')的'+response["rows"][i]['outInSchoolId']+'前往'+response["rows"][i]['destination']+'审核失败')

qioandappr(512)
