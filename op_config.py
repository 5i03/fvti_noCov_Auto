import json
def read():
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
