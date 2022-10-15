import requests
import json
import msgSender
import urllib3
import time

msg=''

def read_config():
    with open('config.json') as f:
        config = json.load(f)
        Name = config["Name"]
        accessToken = config["accessToken"]
        Id = config["Id"]
        sendHost = config["sendHost"]
    return Name, accessToken, Id, sendHost


Name, accessToken, Id, sendHost = read_config()
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


def get_data():
    global msg
    urllib3.disable_warnings()
    response = requests.post(
        'https://'+sendHost+'/api/mStuApi/unregisteredListEpidemicHealthReport.do', headers=s_header, verify=False)
    jsonData = json.loads(response.text)
    msg = msg + '\n早报未打人员名单如下：\n'
    for i in range(0,jsonData['total']):
        if jsonData["rows"][i]['dataType']== 1:
            # print(jsonData["rows"][i]['studentName']+jsonData["rows"][i]['studentCode']+'健康早报未打卡') 
            msg=msg+'@'+jsonData["rows"][i]['studentName']+' '
    msg=msg+'\n午报未打人员名单如下：\n'
    for i in range(0,jsonData['total']):
        if jsonData["rows"][i]['dataType']== 2:
            # print(jsonData["rows"][i]['studentName']+jsonData["rows"][i]['studentCode']+'健康午报未打卡')
            msg=msg+'@'+jsonData["rows"][i]['studentName']+' '
    msg = msg + '\n晚报未打人员名单如下：\n'
    for i in range(0,jsonData['total']):
        if jsonData["rows"][i]['dataType']== 3:
            # print(jsonData["rows"][i]['studentName']+jsonData["rows"][i]['studentCode']+'健康晚报未打卡')
            msg=msg+'@'+jsonData["rows"][i]['studentName']+' '

    msgSender.send_msg('日报未打人员名单如下:' + msg + '\n请及时补打健康日报')

def main():
    get_data()


if __name__ == '__main__':
    # while(1):
    main()
    # get_data()
