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

def fetch_ip_data(url):
    """从指定 URL 抓取 IP 数据"""
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

def parse_ip_data(html):
    """解析 IP 数据并返回 IP 列表"""
    tree = etree.HTML(html)
    ips = tree.xpath('//table[@id="ips"]/tbody/tr')
    ip_list = []
    for ip in ips:
        try:
            ip_address = ip.xpath('td[1]/text()')[0].strip()
            ip_info = f"IP,{ip_address}"
            ip_list.append(ip_info)
        except IndexError:
            continue
    return ip_list

def save_ip_data(filename, ip_list):
    """将 IP 数据保存到文件，避免重复"""
    existing_ips = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as ip_file:
            existing_ips = set(line.strip() for line in ip_file)
    
    with open(filename, "a", encoding='utf-8') as ip_file:
        for ip_info in ip_list:
            if ip_info not in existing_ips:
                ip_file.write(ip_info + "\n")
                existing_ips.add(ip_info)

def main():
    filename = "IP.China.list"
    url = "https://example.com/ipdata"
    
    init_file(filename)  # 初始化文件
    html = fetch_ip_data(url)  # 抓取数据
    if html:
        ip_list = parse_ip_data(html)  # 解析数据
        if ip_list:  # 仅当解析到数据时才保存
            save_ip_data(filename, ip_list)  # 保存数据

if __name__ == "__main__":
    main()
