import requests  # 用于发起 HTTP 请求
from lxml import etree  # 用于解析 HTML 内容
import json  # 用于处理 JSON 数据
from datetime import datetime, timedelta  # 用于时间处理

# 生成头部信息的函数
def get_header(file_name, count):
    utc_time = datetime.utcnow()  # 获取当前的 UTC 时间
    china_time = utc_time + timedelta(hours=8)  # 转换为 CST (UTC+8)
    local_time = china_time.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为字符串
    # 根据文件名生成相应的头部信息
    header = f"""\
// {file_name.replace('.list', '')}
// Link: https://github.com/iuu666/ASN.China
// Total Count: {count}
// Last Updated: CST {local_time}
// Made by iuu, All rights reserved.

"""
    return header  # 返回生成的头部信息

# 数据抓取和保存的主函数
def fetch_and_save(url, file_name, expected_min_count=100):
    try:
        # 发起 GET 请求获取页面内容
        r = requests.get(url)
        if r.status_code != 200:  # 检查请求是否成功
            print(f"Error: Failed to fetch data from {url}. Status code: {r.status_code}")
            return  # 如果请求失败，终止函数

        r_text = r.text  # 获取响应文本

        # 解析 HTML 内容
        tree = etree.HTML(r_text)
        # 提取嵌入的数据
        asns_element = tree.xpath('//*[@data-target="react-app.embeddedData"]')
        if not asns_element:  # 检查数据元素是否成功提取
            print("Error: Failed to locate the embedded data element.")
            return

        asns = asns_element[0].text  # 获取嵌入的数据文本
        if not asns:  # 检查提取的数据是否为空
            print("Error: Extracted data is empty.")
            return

        # 解析 JSON 数据
        try:
            x = json.loads(asns)['payload']['blob']['rawLines']  # 解析 JSON 数据并提取行
        except (json.JSONDecodeError, KeyError) as e:  # 处理 JSON 解析错误
            print(f"Error: Failed to parse JSON data. {str(e)}")
            return

        # 计算总记录数
        count = len(x)

        # 内容验证：检查抓取到的数据行数是否低于预期
        if count < expected_min_count:
            print(f"Warning: Data count is less than expected ({count} records). Data not saved.")
            return  # 如果行数不足，终止函数

        # 保存数据到文件
        with open(file_name, "w", encoding='utf-8') as file:
            # 写入头部信息
            file.write(get_header(file_name, count))
            # 写入数据，并为每条数据添加 "IP-CIDR," 前缀
            for i in x:
                file.write(f"IP-CIDR,{i}")
                file.write('\n')

        print(f"Success: Data successfully fetched and saved to {file_name}")  # 打印成功信息

    except Exception as e:  # 捕获其他意外错误
        print(f"Unexpected error: {str(e)}")

# 各种 IP 列表的 URL
allChina = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china.list"
v4China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china4.list"
v6China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china6.list"

# 执行函数，保存数据
fetch_and_save(allChina, "IP.China.list")  # 抓取和保存中国 IP 列表
fetch_and_save(v4China, "IPv4.China.list")  # 抓取和保存 IPv4 列表
fetch_and_save(v6China, "IPv6.China.list")  # 抓取和保存 IPv6 列表
