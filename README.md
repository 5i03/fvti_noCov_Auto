# fvti_nCov_Auto_Reporter
福州职业技术学院健康励园自动日报脚本,The daily health report automation script of the "JianKangLiYuan" applet of Fuzhou Polytechnic(fvti)

使用方法:
本项目开发使用`python 3.6.5`请确保你用的版本号和我一致或者比我更新!!!<br />
不要用python 2 用python 3!<br />
不要用python 2 用python 3!<br />
不要用python 2 用python 3!<br />
重要事情说三遍
用PIP安装依赖
```bash
pip3 install -r requirements.txt
#如果你使用的Python版本3的执行路径是Python，请把我提到的Python3改成Python
```
安装完成依赖包后

~~请自行在手机或者PC安装抓包软件抓取请求头（请确保抓包软件能抓取https请求）<br />点开 健康日报 后返回抓包软件查看接口返回的rosterId和access\ token
之后打开configs.py
把你抓包获得的rosterId,access\ token替换`configs.py`中的值~~

运行Python3 get_token.py
并输入你的账号密码
学生ID和Token会自动写入config.json
然后执行index.py

```bash
python3 index.py
```

如果没有报错即可
请在17点后使用定时触发器执行`python3 index.py`即可自动填报

目前已经写好基本的函数,其他功能的还在做,敬请期待,谢谢!
后期可能会增加多用户,更丰富的自定义选项等,先凑合着用吧~
有bug,建议啥的直接发issue,我会做出修改的!
