import os
import requests
from lxml import etree
import json
from datetime import datetime, timedelta

def init_file(filename):
    """初始化文件，写入文件头部信息"""
    if not os.path.exists(filename):  # 仅当文件不存在时才创建
        local_time = datetime.utcnow() + timedelta(hours=8)  # 将 UTC 时间转换为 CST 时间
        local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
        header_info = f"// {os.path.basename(filename)}. (https://github.com/iuu666/ASN.China)\n"
        header_info += f"// Last Updated: CST {local_time_str}\n"
        header_info += "// Made by iuu, All rights reserved.\n\n"
        with open(filename, "w", encoding='utf-8') as file:
            file.write(header_info)

def fetch_asn_data(url):
    """从指定 URL 抓取 ASN 数据"""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    return response.text

def parse_asn_data(html):
    """解析 ASN 数据并返回 ASN 列表"""
    tree = etree.HTML(html)
    asns = tree.xpath('//table[@id="asns"]/tbody/tr')
    asn_list = []
    for asn in asns:
        try:
            asn_number = asn.xpath('td[1]/a/text()')[0].replace('AS', '')
            asn_name = asn.xpath('td[2]/text()')
            if asn_name:
                asn_info = f"IP-ASN,{asn_number} // {asn_name[0].strip()}"
                asn_list.append(asn_info)
        except IndexError:
            continue
    return asn_list

def save_asn_data(filename, asn_list):
    """将 ASN 数据保存到文件，避免重复"""
    existing_asns = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as asn_file:
            existing_asns = set(line.strip() for line in asn_file)
    
    with open(filename, "a", encoding='utf-8') as asn_file:
        for asn_info in asn_list:
            if asn_info not in existing_asns:
                asn_file.write(asn_info + "\n")
                existing_asns.add(asn_info)

def main():
    filename = "ASN.China.list"
    url = "https://bgp.he.net/country/CN"
    
    init_file(filename)  # 初始化文件
    html = fetch_asn_data(url)  # 抓取数据
    if html:
        asn_list = parse_asn_data(html)  # 解析数据
        if asn_list:  # 仅当解析到数据时才保存
            save_asn_data(filename, asn_list)  # 保存数据

if __name__ == "__main__":
    main()
