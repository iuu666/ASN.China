import requests
from lxml import etree
import json
from datetime import datetime, timedelta

# 生成头部信息
def get_header(file_name):
    utc_time = datetime.utcnow()  # 获取当前的 UTC 时间
    china_time = utc_time + timedelta(hours=8)  # 转换为 CST (UTC+8)
    local_time = china_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为字符串
    # 根据文件名生成相应的头部信息
    header = f"""\
# {file_name.replace('.list', '')} (https://github.com/iuu666/ASN.China)
# Last Updated: CST {local_time}
# Made by iuu, All rights reserved.
"""
    return header

# 各种 IP 列表的 URL
allChina = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china.list"
v4China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china4.list"
v6China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china6.list"

# 获取所有 IP 地址的列表
r = requests.get(allChina)
# 解析 HTML 内容
tree = etree.HTML(r.text)
# 提取嵌入的数据
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
# 解析 JSON 数据
x = json.loads(asns)['payload']['blob']['rawLines']
# 保存所有 IP 地址到文件
with open("IP.China.list", "w", encoding='utf-8') as allChinaIP:
    allChinaIP.write(get_header("IP.China.list"))
    for i in x:
        allChinaIP.write(i)
        allChinaIP.write('\n')

# 获取 IPv4 地址列表
r = requests.get(v4China)
# 解析 HTML 内容
tree = etree.HTML(r.text)
# 提取嵌入的数据
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
# 解析 JSON 数据
x = json.loads(asns)['payload']['blob']['rawLines']
# 保存 IPv4 地址到文件
with open("IPv4.China.list", "w", encoding='utf-8') as v4ChinaIP:
    v4ChinaIP.write(get_header("IPv4.China.list"))
    for i in x:
        v4ChinaIP.write(i)
        v4ChinaIP.write('\n')

# 获取 IPv6 地址列表
r = requests.get(v6China)
# 解析 HTML 内容
tree = etree.HTML(r.text)
# 提取嵌入的数据
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
# 解析 JSON 数据
x = json.loads(asns)['payload']['blob']['rawLines']
# 保存 IPv6 地址到文件
with open("IPv6.China.list", "w", encoding='utf-8') as v6ChinaIP:
    v6ChinaIP.write(get_header("IPv6.China.list"))
    for i in x:
        v6ChinaIP.write(i)
        v6ChinaIP.write('\n')
