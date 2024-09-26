import requests
from lxml import etree
from datetime import datetime, timedelta

def initFile(file_name):
    """
    初始化文件，写入头部信息，包括文件名、总数计数器、更新时间等。
    """
    # 获取当前的 UTC 时间
    utcTime = datetime.utcnow()
    # 将 UTC 时间转换为 CST (UTC+8)
    chinaTime = utcTime + timedelta(hours=8)
    # 格式化时间为字符串
    localTime = chinaTime.strftime("%Y-%m-%d %H:%M:%S")
    
    # 初始化文件并写入头部信息
    with open(file_name, "w", encoding='utf-8') as file:
        file.write(f"// {file_name.replace('.list', '')}\n")  # 写入文件名
        file.write("// Link: https://github.com/iuu666/ASN.China\n")  # 添加仓库链接
        file.write("// Total Count: 0\n")  # 初始计数为 0
        file.write(f"// Last Updated: CST {localTime}\n")  # 写入当前更新时间
        file.write("// Made by iuu, All rights reserved.\n\n")  # 作者信息

def saveLatestASN():
    """
    从 BGP 网站获取最新的中国 ASN 数据，并保存到文件中。
    """
    # BGP ASN 数据的 URL
    url = "https://bgp.he.net/country/CN"
    # 请求头，模拟浏览器访问
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }
    
    try:
        # 发起 GET 请求获取页面内容
        r = requests.get(url=url, headers=headers)
        # 验证响应状态码
        if r.status_code != 200:
            raise Exception(f"Failed to fetch data. Status code: {r.status_code}")
        # 转换为文本格式
        page_content = r.text
    except Exception as e:
        print(f"Error during request: {e}")
        return  # 终止操作

    # 解析 HTML 内容
    tree = etree.HTML(page_content)
    
    # 提取 ASN 信息
    asns = tree.xpath('//*[@id="asns"]/tbody/tr')
    
    # 验证是否提取到 ASN 数据
    if not asns:
        print("No ASN data found on the page.")
        return  # 终止操作
    
    # 文件名
    file_name = "ASN.China.list"
    # 初始化文件，写入初始头部
    initFile(file_name)
    
    # 计数器，用于统计 ASN 数量
    count = 0
    
    # 打开文件，追加写入 ASN 信息
    with open(file_name, "a", encoding='utf-8') as file:
        for asn in asns:
            # 获取 ASN 编号
            asnNumber = asn.xpath('td[1]/a')[0].text.replace('AS', '')
            # 获取 ASN 名称
            asnName = asn.xpath('td[2]')[0].text
            if asnName is not None:
                # 格式化 ASN 信息
                asnInfo = f"IP-ASN,{asnNumber} // {asnName}"
                # 写入文件
                file.write(asnInfo)
                file.write("\n")
                count += 1  # 增加计数
    
    # 更新文件中的计数信息
    updateFileCount(file_name, count)

def updateFileCount(file_name, count):
    """
    更新文件中的 Total Count 信息，表示总计抓取了多少条 ASN 记录。
    """
    # 读取文件并修改 Total Count 行
    with open(file_name, "r+", encoding='utf-8') as file:
        lines = file.readlines()
        # 找到 Total Count 行并更新
        for i, line in enumerate(lines):
            if line.startswith("// Total Count:"):
                lines[i] = f"// Total Count: {count}\n"  # 更新计数
                break
        # 将更新后的内容写回文件
        file.seek(0)
        file.writelines(lines)

# 执行函数，保存最新的 ASN 信息
saveLatestASN()
