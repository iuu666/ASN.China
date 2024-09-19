import requests
from lxml import etree
from datetime import datetime, timedelta

def initFile(file_name):
    # 获取当前的 UTC 时间
    utcTime = datetime.utcnow()
    # 将 UTC 时间转换为 CST (UTC+8)
    chinaTime = utcTime + timedelta(hours=8)
    # 格式化时间为字符串
    localTime = chinaTime.strftime("%Y-%m-%d %H:%M:%S")
    
    # 初始化文件并写入头部信息
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(f"// {file_name.replace('.list', '')}\n")
        file.write("// Link: https://github.com/iuu666/ASN.China\n")
        file.write("// Total Count: 0\n")  # 初始计数为 0
        file.write(f"// Last Updated: CST {localTime}\n")
        file.write("// Made by iuu, All rights reserved.\n\n")

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
    
    # 文件名
    file_name = "ASN.China.list"
    # 初始化文件
    initFile(file_name)
    
    # 计数器
    count = 0
    
    # 写入 ASN 信息到文件
    with open(file_name, "a", encoding='utf-8') as file:
        for asn in asns:
            # 获取 ASN 编号
            asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS', '')
            # 获取 ASN 名称
            asnName = asn.xpath('td[2]')[0].text
            if asnName is not None:
                # 格式化 ASN 信息
                asnInfo = f"IP-ASN,{asnNumber} // {asnName}"
                # 追加 ASN 信息到文件
                file.write(asnInfo)
                file.write("\n")
                count += 1  # 增加计数
    
    # 更新计数信息
    updateFileCount(file_name, count)

def updateFileCount(file_name, count):
    # 读取当前文件内容并更新计数
    with open(file_name, "r+", encoding='utf-8') as file:
        lines = file.readlines()
        # 找到 Total Count 行并更新
        for i, line in enumerate(lines):
            if line.startswith("// Total Count:"):
                lines[i] = f"// Total Count: {count}\n"
                break
        # 将更新后的内容写回文件
        file.seek(0)
        file.writelines(lines)

# 执行函数，保存最新的 ASN 信息
saveLatestASN()
