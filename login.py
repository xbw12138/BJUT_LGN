import requests
import argparse
import chardet
import re

"""
登陆 python login.py -u S201861847 -p 12138 login
注销 python login.py logout
"""
parser = argparse.ArgumentParser(description='BJUT 网关登陆')
parser.add_argument("action", type=str, help="输入login or logout")
parser.add_argument('--username', '-u', type=str, default="S201861847", help='网关用户名')
parser.add_argument('--password', '-p', type=str, default="S201861847", help='网关密码')
args = parser.parse_args()
headers = {
            'Host': 'lgn.bjut.edu.cn',
            'Origin': 'https://lgn.bjut.edu.cn',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1 Safari/605.1.15',
            'Referer': 'https://lgn.bjut.edu.cn/',
            'Accept-Language': 'zh-cn'
        }
if args.action == "login":
    url = "https://lgn.bjut.edu.cn/"
    username = args.username
    password = args.password
    payload = 'DDDDD={}&upass={}&v46s=1&v6ip=&f4serip=172.30.201.10&0MKKey='.format(username, password)
    response = requests.request("POST", url, headers=headers, data = payload)
    response.encoding=chardet.detect(response.content)['encoding']
    pattern = re.compile(r'<title>(.*?)</title>')
    str = response.text
    login_result = re.findall(pattern,str)
    if login_result and "登录成功窗" in login_result:
        pattern = re.compile(r'UID=\'(.*?)\';')
        user_result = re.findall(pattern,str)
        response = requests.request("GET", url, headers=headers)
        response.encoding=chardet.detect(response.content)['encoding']
        pattern = re.compile(r'flow=\'(.*?)\';')
        str = response.text
        flow_result = re.findall(pattern,str)
        print("用户 {} 登陆成功, 本月已使用流量 {} kb".format(user_result[0].strip(), flow_result[0].strip()))
    else:
        print("登陆失败")
elif args.action == "logout":
    url = "https://lgn.bjut.edu.cn/F.htm"
    response = requests.request("GET", url, headers=headers)
    response.encoding=chardet.detect(response.content)['encoding']
    pattern = re.compile(r'Msg=(.*?);')
    str = response.text
    logout_result = re.findall(pattern,str)
    if logout_result and "14" in logout_result:
        pattern = re.compile(r'flow=\'(.*?)\';')
        str = response.text
        flow_result = re.findall(pattern,str)
        print("注销成功, 本月已使用流量 {} kb".format(flow_result[0].strip()))
    else:
        print("注销失败")
