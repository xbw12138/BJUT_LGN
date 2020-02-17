import requests
import argparse
import chardet
import re

"""
登陆ipv46 python login.py -u S201861847 -p 12138 -i 0 login
登陆ipv4  python login.py -u S201861847 -p 12138 -i 1 login
登陆ipv6  python login.py -u S201861847 -p 12138 -i 2 login
注销 python login.py logout
"""
parser = argparse.ArgumentParser(description='BJUT 网关登陆')
parser.add_argument("action", type=str, help="输入login or logout")
parser.add_argument('--username', '-u', type=str, default="S201861847", help='网关用户名')
parser.add_argument('--password', '-p', type=str, default="S201861847", help='网关密码')
parser.add_argument('--ipv46', '-i', type=str, default="0", help='登陆ipv4or6, 0 all, 1 ipv4, 2 ipv6')
args = parser.parse_args()

if args.action == "login":
    url = "https://lgn{}.bjut.edu.cn/".format("6" if args.ipv46 == "2" else "")
    payload = 'DDDDD={}&upass={}&v46s={}&v6ip=&f4serip=172.30.201.10&0MKKey='.format(args.username, args.password, args.ipv46)
    response = requests.request("POST", url, data = payload)
    response.encoding=chardet.detect(response.content)['encoding']
    pattern = re.compile(r'<title>(.*?)</title>')
    str = response.text
    login_result = re.findall(pattern,str)
    if login_result and "登录成功窗" in login_result:
        pattern = re.compile(r'UID=\'(.*?)\';')
        user_result = re.findall(pattern,str)
        response = requests.request("GET", url)
        response.encoding=chardet.detect(response.content)['encoding']
        pattern = re.compile(r'flow=\'(.*?)\';')
        str = response.text
        flow_result = re.findall(pattern,str)
        print("用户 {} 登陆成功, 本月已使用流量 {} kb".format(user_result[0].strip(), flow_result[0].strip()))
    else:
        print("登陆失败")
elif args.action == "logout":
    url = "https://lgn{}.bjut.edu.cn/F.htm".format("6" if args.ipv46 == "2" else "")
    response = requests.request("GET", url)
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
