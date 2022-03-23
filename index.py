import json
import sys
import time
import requests
import urllib.request
import os
import jsonpath
import argparse
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


# send_hosts = "api.5i03.cn"
send_hosts = 'health.fvti.linyisong.top'
baseURL = "https://" + send_hosts
localDate = time.strftime('%Y-%m-%d', time.localtime())
health_report_url = baseURL + '/api/mStuApi/updateHealthReportEpidemicHealthReport.do'
rosterId = ''
access_token = ""
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
# send_data_for_task_list = {
#     "page": "1",
#     "rows": "9"
# }
#
# print(send_data_for_task_list)
# req = urllib.request.Request(
#     url=task_list_url, headers=send_header, data=send_data_for_task_list, method=GET)

########################################
# ---------弃用的方法-------
# 将get请求中url携带的参数封装至字典中
# param = {
#   'query':''
# }
# 对url中的非ascii进行编码
# param = urllib.parse.urlencode(send_header)
# 将编码后的数据值拼接回url中
# baseURL += param
# response = urllib.request.urlopen(url=baseURL)
# k1 = urllib.request.urlopen(req)
# html = k1.read().decode('utf-8')
# print(req)
# req = urllib.request.Request(task_list_url)
# req.add_header(send_header)
# print(req)

# url = ''
# headers = {
# 	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
# 	'Host': 'httpbin.org'
# }
# dict = {
# 	'name': 'Germey'
# }
# send_data_for_task_list_byte = bytes(urllib.parse.urlencode(send_data_for_task_list), encoding = 'utf8')
# send_header_byte =  dict(urllib.parse.urlencode(send_header), encoding = 'utf8')
# response = urllib.request.Request(url=task_list_url, data=send_data_for_task_list, headers=send_header, method='GET')
# response = urllib.request.urlopen(response)
# print(response.read().decode('utf-8'))
########################################
# headers={"Host":"api.5i03.cn","Content-Type":"application/json","Accept-Language":"zh-cn","Accept-Encoding":"gzip,deflate,br","Connection":"keep-alive","Accept":"*/*","User-Agent":"user_agent","accessToken":"eyJhbGciOiJIUzUxMiJ9.eyJuYW1lIjoiMmM5MTgwODI3Yjg4YzU3OTAxN2I4YmJmZWE5YzIzYWMiLCJleHAiOjE2NTAyOTYwNTEsInVzZXJJZCI6IjJjOTE4MDgyN2I4OGM1NzkwMTdiOGJiZmVhOWMyM2FjIiwiaWF0IjoxNjQ3NzA0MDUxLCJ1c2VybmFtZSI6IjJjOTE4MDgyN2I4OGM1NzkwMTdiOGJiZmVhOWMyM2FjIn0.2Jemo_MjwQZgY2SbcKIirMcztzxXgjUVpOW0oH6mYWUd1NaaIJV3CyVYwAHoI_nbnPt8zqz1x4cEyLZmR3LMIA","Referer":"https://servicewechat.com/wx56b1d7357f3df890/25/page-frame.html","Content-Length":"19"}

# with open(rosterId + 'raw_task_list.json', 'w+', encoding='utf-8') as f:
#     f.write(str(data))
#  # 打开文件如果文件不存在，创建该文件。把变量写入文件。

# print(data)
# with open(rosterId + "_" + localDate + '_task_list.json',encoding='utf8') as json_file:
#         config = json.load(json_file)
# pa=json.loads(open(rosterId + "_" + localDate + '_task_list.json'))
# print(config)
# healthId = jsonpath.jsonpath(config, "$.rows[1].healthId")
# endTime = jsonpath.jsonpath(config, "$.rows[1].endTime")
# dataType = jsonpath.jsonpath(config, "$.rows[1].dataType")
# # print(healthId,endTime,dataType)
# exit()
dataDate = "dataDate=" + localDate
# dataDate = "dataDate="+dataDate
# send_datas = {'healthId': healthId,
#               'rosterId': rosterId,
#               'isGfxReturn': '2',
#               'isJwReturn': '2',
#               'isContactPatient': '2',
#               'isContactRiskArea': '2',
#               'isHealthCodeOk': '2',
#               'details': dataDate,
#               'dataType': dataType,
#               'dataStatus': '2',
#               'endTime': endTime,
#               'liveState': '2',
#               'nowAddress': '福建省福州市闽侯县上街镇113县道福州职业技术学院',
#               'nowAddressDetail': '在校',
#               'nowTiwenState': '1',
#               'nowHealthState': '1',
#               'counsellorApprovalStatus': '未审核',
#               'temperature': '36'
#               }
# # rst=urllib.request.urlopen(task_list_url, headers=send_header, data=send_data_for_task_list)

# 自定义 len() 函数


def get_today_list():
    global rosterId
    if os.path.isfile(rosterId + "_" + localDate + 'raw_task_list.json'):
        print("原始文件已存在")
    # elif os.path.isfile(rosterId + "_" + localDate + 'task_list.json'):
    #     print("分离当天任务成功")
    else:
        print("文件不存在")
################################


def D_t_l():
    # download_task_list
    # 本函数用于下载当天任务的原始文件
    send_data_for_task_list = {
        "page": "1",
        "rows": "9"
    }
    global baseURL, rosterId, healthId, localDate, file_rs
    task_list_url = baseURL + "/api/mStuApi/queryByStuEpidemicHealthReport.do"
    r = requests.get(url=task_list_url, headers=send_header,
                     data=send_data_for_task_list, verify=False, timeout=30)
    # print(r)
    with open(rosterId + "_" + localDate+"_task_list.json", 'w+', encoding='utf-8') as f:
        f.write(r.text)
        f.close()
    # main()
    # exit()
    return

# 3


def r_s_t(dataType):
    # report_singal_task提交健康日报
    global health_report_url, send_header, dataDate, rosterId
    with open(rosterId + "_" + localDate + '_task_list.json', encoding='utf8') as json_file:
        config = json.load(json_file)
    if dataType == 1:
        # dataType= '1'
        healthId = jsonpath.jsonpath(config, "$.rows[1].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[1].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[1].dataType")
    elif dataType == 2:
        # dataType= '3'
        healthId = jsonpath.jsonpath(config, "$.rows[2].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[2].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[2].dataType")
    elif dataType == 3:
        # dataType= '3'
        healthId = jsonpath.jsonpath(config, "$.rows[3].healthId")
        endTime = jsonpath.jsonpath(config, "$.rows[3].endTime")
        dataType = jsonpath.jsonpath(config, "$.rows[3].dataType")
    else:
        print("暂时不支持这种任务类型,请提交issue反馈")
        exit()
    # dataDate=localDate
    send_datas = send_datas = {'healthId': healthId, 'rosterId': rosterId, 'isGfxReturn': '2', 'isJwReturn': '2', 'isContactPatient': '2', 'isContactRiskArea': '2', 'isHealthCodeOk': '2', 'isSick': '0', 'details': dataDate, 'dataType': dataType,
                               'dataStatus': '2', 'endTime': endTime, 'liveState': '2', 'nowAddress': '福建省福州市闽侯县上街镇113县道福州职业技术学院', 'nowAddressDetail': '在校', 'nowTiwenState': '1', 'nowHealthState': '1', 'counsellorApprovalStatus': '未审核', 'temperature': '36'}
    # send_datas='healthId='+ healthId +'&rosterId='+rosterId+'=dataDate%3D"+localDate+"&isGfxReturn=+2&isJwReturn=2&isContactPatient=2&isContactRiskArea=2&isHealthCodeOk=2&isSick=0&symptomAndHandle=&otherThing=&dataDate=&dataType=&dataStatus=&endTime=&liveState=2&nowAddress=%E7%A6%8F%E5%BB%BA%E7%9C%81%E7%A6%8F%E5%B7%9E%E5%B8%82%E9%97%BD%E4%BE%AF%E5%8E%BF%E4%B8%8A%E8%A1%97%E9%95%87113%E5%8E%BF%E9%81%93%E7%A6%8F%E5%B7%9E%E8%81%8C%E4%B8%9A%E6%8A%80%E6%9C%AF%E5%AD%A6%E9%99%A2&nowAddressDetail=%E5%9C%A8%E6%A0%A1&nowTiwenState=1&nowHealthState=1&counsellorApprovalStatus=&temperature=36'

    # send_datas=type(str(send_datas))
    r = requests.post(url=health_report_url,
                      headers=send_header,params=send_datas, verify=False)
    print(r.text)

def main():
    if os.path.isfile(rosterId + "_" + localDate + '_task_list.json'):
        # D_t_l()
        r_s_t(1)
        r_s_t(2)
        r_s_t(3)


    # elif os.path.isfile(rosterId + "_" + localDate + 'task_list.json'):
    #     # print("分离当天任务成功")
    #     pass
    else:
        # print("文件不存在")
        # exit()
        D_t_l()
        main()


main()




