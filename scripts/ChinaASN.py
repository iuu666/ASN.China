import requests
from lxml import etree
from datetime import datetime, timedelta

def initFile():
    # 获取当前的 UTC 时间
    utcTime = datetime.utcnow()
    # 将 UTC 时间转换为 CST (UTC+8)
    chinaTime = utcTime + timedelta(hours=8)
    # 格式化时间为字符串
    localTime = chinaTime.strftime("%Y-%m-%d %H:%M:%S")
    
    # 初始化文件并写入头部信息
    with open("ASN.China.list", "w", encoding='utf-8') as asnFile:
        asnFile.write("// ASN Information in China. (https://github.com/iuu666/ASN.China) \n")
        asnFile.write("// Last Updated: CST " + localTime + "\n")
        asnFile.write("// Made by iuu, All rights reserved. " + "\n\n")

def saveLatestASN():
    # BGP ASN 数据的 URL
    url = "https://bgp.he.net/country/CN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    
    # 发起 GET 请求获取页面内容
    r = requests.get(url=url, headers=headers).text
    # 解析 HTML 内容
    tree = etree.HTML(r)
    # 提取 ASN 信息
    asns = tree.xpath('//*[@id="asns"]/tbody/tr')
    
    # 初始化文件
    initFile()
    
    # 写入 ASN 信息到文件
    for asn in asns:
        # 获取 ASN 编号
        asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS', '')
        # 获取 ASN 名称
        asnName = asn.xpath('td[2]')[0].text
        if asnName is not None:
            # 格式化 ASN 信息
            asnInfo = "IP-ASN,{} // {}".format(asnNumber, asnName)
            # 追加 ASN 信息到文件
            with open("ASN.China.list", "a", encoding='utf-8') as asnFile:
                asnFile.write(asnInfo)
                asnFile.write("\n")

# 执行函数，保存最新的 ASN 信息
saveLatestASN()
