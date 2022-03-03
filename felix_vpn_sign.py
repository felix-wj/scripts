# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/21 12:01
@Auth ： Icrons
@IDE ：PyCharm
//魔改版 by George_Li
//修改内容：增加多网站登录，多用户登录，改为github workflow定时执行
//使用方法：创建secrets 名字：MYKEY 内容的写法：
//机场的名字(方便自己看)|机场的网址(https:www.xxxx...)|第一个邮箱(用户名),密码;第二个邮箱,密码;...
//每两个机场用回车键隔开
//例如: 某某云|https://www.yun.com|jjjj@qq.com,password

cron:  0 20 9 * * ? felix_vpn_sign.py
new Env('VPN签到');

"""
import requests
import os
import re
import json
try:
    from notify import send
except Exception as err:
    logger.debug(str(err))
    logger.info("无推送文件")

requests.urllib3.disable_warnings()

#初始化环境变量开头
datas = os.environ["vpn_key"]

if(datas == ''):
  print('您没有输入任何信息')
  exit
groups = datas.split('\n')
#初始化环境变量结尾

class SspanelQd(object):
    def __init__(self,name,site,username,psw):
        ###############登录信息配置区###############
        #机场的名字
        self.name = name
        #签到流量
        self.flow = 0
        # 机场地址
        self.base_url = site
        # 登录信息
        self.email = username
        self.password = psw
        ###########################################


    def checkin(self):
        email = self.email.split('@')
        email = email[0] + '%40' + email[1]
        password = self.password
        try:
            session = requests.session()
            session.get(self.base_url, verify=False)

            login_url = self.base_url + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = 'email=' + email + '&passwd=' + password + '&code='
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                'Referer': self.base_url + '/user'
            }

            response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
            # print(response.text)
            msg = (response.json()).get('msg')
            print(msg)
        except:
            return False

        info_url = self.base_url + '/user'
        response = session.get(info_url, verify=False)
        """
        以下只适配了editXY主题
        """
        try:
            level = re.findall(r'\["Class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["Class_Expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["Unused_Traffic", "(.*?)"]', response.text)[0]
            msg = "- 今日签到信息：" + str(msg) + "\n- 用户等级：" + str(level) + "\n- 到期时间：" + str(day) + "\n- 剩余流量：" + str(rest)
            print(msg)
            return msg
        except:
            return msg
    def getflow(self , msg):
      pattern = re.compile('获得了(.+)MB')
      if(msg == ""):
        return 0
      num = pattern.findall(msg)
      if num == []:
        return 0
      else:
        return num[0]
    

    def main(self):
        msg = self.checkin()
        if msg == False:
            print("网址不正确或网站禁止访问。")
            msg = self.name + "签到失败"
        send("VPN签到",msg)


i = 0
while i < len(groups):
  group = groups[i]
  i += 1
  prop = group.split('|')
  site_name = prop[0]
  web_site = prop[1]
  prof = prop[2]
  profiles = prof.split(';')
  j = 0
  while j < len(profiles):
    profile = profiles[j]
    profile = profile.split(',')
    username = profile[0]
    pswd = profile[1]
    print(site_name)
    print(web_site)
    print(username)
    print(pswd)
    
    run = SspanelQd(site_name, web_site ,username ,pswd)
    run.main()
    j += 1