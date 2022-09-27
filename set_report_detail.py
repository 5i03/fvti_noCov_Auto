# 设置填报的数据并写入config.json
from asyncio.log import logger
import hashlib
from random import random
import jsonpath
import requests
import json
import time
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename='report.log')
logger = logging.getLogger(__name__)


def read_config():
    with open('config.json', encoding='utf8') as json_file:
        config = json.load(json_file)
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
    return isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, \
        isHealthCodeOk, isSick, details, liveState, nowAddress, \
        nowAddressDetail, nowTiwenState, nowHealthState, temperature


isGfxReturn, isJwReturn, isContactPatient, isContactRiskArea, \
    isHealthCodeOk, isSick, details, liveState, nowAddress, \
    nowAddressDetail, nowTiwenState, nowHealthState, temperature = read_config()


def set_report_detail():
    # 读取配置文件config.json 读取学生名字，健康日报名册ID，和访问令牌,和填报用的数据
    with open('config.json', encoding='utf8') as json_file:
        config = json.load(json_file)
    config['isGfxReturn'] = input('是否从高风险返回? 2为否/1为是:')
    config['isJwReturn'] = input('是否从境外返回? 2为否/1为是:')
    config['isContactPatient'] = input('是否接触过确诊病例? 2为否/1为是:')
    config['isContactRiskArea'] = input('是否接触过疫情风险地区? 2为否/1为是:')
    config['isHealthCodeOk'] = input('是否健康码正常?2为否/1为是:')
    config['isSick'] = input('是否有发热、乏力、干咳、呼吸困难等症状? 0为否/1为是:')
    config['liveState'] = input('居住状态? 1为居家/2为在校/3为实习')
    config['nowAddress'] = input('现居住地（街道/小区）? ')
    config['nowAddressDetail'] = input('现居住地详细地址： ')
    config['nowTiwenState'] = input('体温状态？ 1为正常/2为异常:')
    config['nowHealthState'] = input('健康状态? 1为正常/2为异常:')
    config['temperature'] = input('体温? ')
    with open('config.json', 'w', encoding='utf8') as json_file:
        json.dump(config, json_file, ensure_ascii=False, indent=4)
    logger.info('配置文件已更新')

if __name__ == '__main__':
    set_report_detail()
    