
'''
cron:  0 20 8 * * ? felix_hefen10086.py
new Env('和粉');
'''
import time
import requests
import os

if "hefen_token" in os.environ:
    if len(os.environ["hefen_token"]) > 1:
        hefen_token = os.environ["hefen_token"]
        print("已获取并使用环境变量中 hefen_token")

if "hefen_mobile" in os.environ:
    if len(os.environ["hefen_mobile"]) > 1:
        hefen_mobile = os.environ["hefen_mobile"]
        print("已获取并使用环境变量中纬度 hefen_mobile :" + hefen_mobile)
def checkin(num, token):
    hd = {'FROM': 'X0003', 'Host': 't.hefen.10086.cn', 'MSGNAME': 'userSignReq', 'Origin': 'https://t.hefen.10086.cn',
          'Referer': 'https://t.hefen.10086.cn/html5/views/person_center/person_sign.html?zrsign=0&rwId=5',
          'TIMESTAMP': str(int(time.time() * 1000)), 'TO': 'X0001', 'X-Requested-With': 'XMLHttpRequest',
          'TOKEN': token,
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
          'Content-Type': 'application/x-www-form-urlencoded, application/json; charset=utf-8'}
    data = {"mobile": num}
    r = requests.post('https://t.hefen.10086.cn/afservice/service/invoke.do', json=data, headers=hd)
    return r.json()

if __name__ == '__main__':
    checkin(hefen_mobile, hefen_token)
