import requests
from lxml import etree
from datetime import datetime, timedelta

def initFile():
    utcTime = datetime.utcnow()  # 获取当前的 UTC 时间
    chinaTime = utcTime + timedelta(hours=8)  # 转换为 CST (UTC+8)
    localTime = chinaTime.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为字符串
    with open("ASN.China.list", "w") as asnFile:
        asnFile.write("// ASN Information in China. (https://github.com/iuu666/ASN.China) \n")
        asnFile.write("// Last Updated: CST " + localTime + "\n")
        asnFile.write("// Made by iuu, All rights reserved. " + "\n\n")
        
def saveLatestASN():
    url = "https://bgp.he.net/country/CN"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    r = requests.get(url=url, headers=headers).text
    tree = etree.HTML(r)
    asns = tree.xpath('//*[@id="asns"]/tbody/tr')
    initFile()
    for asn in asns:
        asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS', '')
        asnName = asn.xpath('td[2]')[0].text
        if asnName is not None:
            asnInfo = "IP-ASN,{} // {}".format(asnNumber, asnName)
            with open("ASN.China.list", "a", encoding='utf-8') as asnFile:
                asnFile.write(asnInfo)
                asnFile.write("\n")

saveLatestASN()
