# fvti_noCovSys_Automation
福州职业技术学院健康励园自动化脚本
(for Fuzhou Polytechnic)
目前功能：
1. 辅导员功能：统计未打卡的学生名字，自动允许某种类型的出入校。
2. 班委功能，以班委账号抓取未打卡的学生名字，并推送
3. 学生功能，自动打卡和自动申请出入校

<h1 style="color:red;">有小道消息称学校可能会改用其他健康日报系统，当前脚本不在更新，转为归档状态</h1>
使用方法:
本项目开发使用`python 3`请确保你用的版本号和我一致或者比我更新!!!<br />

```bash
pip3 install -r requirements.txt
#如果你使用的Python版本3的执行路径是Python，请把我提到的Python3改成Python
```
安装完成依赖包后

<!--~~请自行在手机或者PC安装抓包软件抓取请求头（请确保抓包软件能抓取https请求）<br />点开 健康日报 后返回抓包软件查看接口返回的rosterId和access\ token
之后打开configs.py
把你抓包获得的rosterId,access\ token替换`configs.py`中的值~~-->

> 在config.json中修改 "Username": "这里写学号","Password": "这里写密码"，role": "这里写你的身份：Teacher，Student，SquadLeader",
之后运行Python3 TokenHelper.py
<!--~~并输入你的账号密码~~-->
ID和Token会自动写入config.json
然后执行index.py

```bash
python3 index.py [-t 0 早中晚|1 早报|2 午报|3 晚报|] 
```
### 如果手动填报过了脚本不会自动覆盖

如果没有报错即可
请在17点后使用定时触发器执行`StuAutoReport.py `即可自动填报

也可运行crontab -e 后输入如下代码
```bash
0 17 * * * python3 /root/fvti_noCov_Script/StuAutoReport.py -t 3
15 0 * * * python3 /root/fvti_noCov_Script/StuAutoReport.py -t 1
0 10 * * * python3 /root/fvti_noCov_Script/StuAutoReport.py -t 2
```

初次运行请修改配置文件 config.json
```
{
    "Username": "学号",
    "Password": "密码",
    "role": "Teacher，Student", //如果你是学生，但你能查看日报未打卡情况，请设置你的身份为SquadLeader而非Student
    "Id": "",//TokenHelper自动填写
    "way": "qq",//推送方式
    "stk": "",推送服务令牌
    "isSendToGroup": "False",//是否推送到群组
    "sender": "",//发送者QQ号，使用5i03 QQ推送请填写
    "receiver": "",//接收者
    "xyMsgServerURL": "",//推送服务器地址
    "accessToken": "",//令牌，请执行TokenHelper自动填写
    "Name": "",//TokenHelper自动填写
    "sendHost": "health.fvti.linyisong.top",
    "isGfxReturn": "2",//是否高风险返回
    "isJwReturn": "2",//是否境外返回
    "isContactPatient": "2",//是否接触密结 2 否
    "isContactRiskArea": "2",//是否接触高风险人员 2 否
    "isHealthCodeOk": "2",//健康码绿的吗?2是绿的
    "isSick": "0",//有没有咳嗽什么的0正常
    "liveState": "2",//居住状态1 居家 2 在校 3 实习
    "nowAddress": "福建省福州市闽侯县上街镇113县道福州职业技术学院",
    "nowAddressDetail": "校内学生公寓",
    "nowTiwenState": "1",//现在体温状态
    "nowHealthState": "1",//现在
    "temperature": "36",//体温
    "details": ""
}
```
