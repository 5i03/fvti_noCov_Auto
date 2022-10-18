# # ocr
# from os import urandom
# import re
import requests
import base64
# import ddddocr
# # import time
# # from PIL import ImageGrab
# # tencentcloud-sdk-python-ocr
# # "Wed Oct 05 2022 03:59:37 GMT+0800 (中国标准时间)"
# # ddddocr （个人免费接口） 识别验证码
# def dddd_ocr(Date):
#     # http://health.fvti.linyisong.top/style/v1/images/login/img.jsp?
# # ddddocr = ddddocr.DdddOcr()
# # request captcha from server
# # request=
#     requests.packages.urllib3.disable_warnings()
#     # img=requests.get("http://health.fvti.linyisong.top/style/v1/images/login/img.jsp?="+str(Date))
# # use ddddocr to recognize captcha
#     code = ddddocr.DdddOcr().classification(requests.get("http://health.fvti.linyisong.top/style/v1/images/login/img.jsp?="+str(Date)).content)
#     # print("验证码是:"+code)
#     return code
# # print(img)
# # ocr = ddddocr.DdddOcr()
# # with open('', 'rb') as f:
# #     img_bytes = f.read()
# # ocr = ocr.classification(img_bytes)
# def baidu_ocr():
#     # 等待开发
#     api_addr='https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    
#     pass
# def ali_ocr():
#     # 等待开发
#     api_addr='https://ocrapi-advanced.taobao.com/ocrservice/advanced'
#     pass
# def tencent_ocr():
#     api_addr='https://recognition.image.myqcloud.com/ocr/general'
#     # 等待开发
#     pass
# def huawei_ocr():
#     api_addr='https://ocr.cn-north-4.myhuaweicloud.com/v1.0/ocr/general-text'
#     # 等待开发
#     pass

with open('captcha.jpg', 'rb') as f:
      img_bytes = f.read()
msg='正在识别图像'
print(msg)
requests.packages.urllib3.disable_warnings()

cap_ocr_res=requests.post("https://api.5i03.cn/api/ocr/ddddocr/ocr/b64/text",data=base64.b64encode(img_bytes).decode(),verify=False).text
print(cap_ocr_res)