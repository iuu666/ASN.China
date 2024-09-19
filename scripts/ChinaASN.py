import os
import requests
from lxml import etree
from datetime import datetime, timedelta

def init_file(filename):
    """初始化文件，写入文件头部信息"""
    local_time = datetime.utcnow() + timedelta(hours=8)  # 将 UTC 时间转换为 CST 时间
    local_time_str = local_time.strftime("%Y-%m-%d %H:%M:%S")
    header_info = f"// {os.path.basename(filename)}. (https://github.com/iuu666/ASN.China)\n"
    header_info += f"// Last Updated: CST {local_time_str}\n"
    header_info += "// Made by iuu, All rights reserved.\n"
    
    # 仅当文件不存在时才创建
    if not os.path.exists(filename):
        with open(filename, "w", encoding='utf-8') as file:
            file.write(header_info + "\n")  # 在写入头部信息后加一个换行

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

def update_asn_file(filename, asn_list):
    """更新 ASN 文件，删除重复项并写入数据"""
    existing_asns = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as file:
            existing_asns = set(line.strip() for line in file)
    
    new_asns = set(asn_list)
    all_asns = existing_asns.union(new_asns)
    
    with open(filename, "w", encoding='utf-8') as file:
        # 写入头部信息，仅当文件为空时
        if not existing_asns:
            init_file(filename)
        
        # 确保不重复，按顺序写入数据
        for asn_info in sorted(all_asns):
            file.write(asn_info + "\n")

def main():
    filename = "ASN.China.list"
    url = "https://bgp.he.net/country/CN"
    
    html = fetch_asn_data(url)  # 抓取数据
    if html:
        asn_list = parse_asn_data(html)  # 解析数据
        if asn_list:  # 仅当解析到数据时才更新
            update_asn_file(filename, asn_list)  # 更新文件

if __name__ == "__main__":
    main()
