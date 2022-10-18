import sqlite3
import json
import sys
import codecs
import logging
import logging.handlers
import os
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

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
# print('Opened database successfully')


def sql_query(dl_sql, dbName):
    conn = sqlite3.connect(dbName)
    # sql="CREATE TABLE STUDENT ( studentName TEXT NOT NULL,studentCode INT PRIMARY KEY,homeAddress TEXT NOT NULL,dataType TEXT NOT NULL,counter INT NOT NULL);"
    conn.execute(dl_sql)
    conn.commit()
    conn.close()
