import os
import requests
from lxml import etree
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

def update_ip_file(filename, ip_list):
    """更新 IP 文件，删除重复项并写入数据"""
    existing_ips = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding='utf-8') as file:
            existing_ips = set(line.strip() for line in file)
    
    new_ips = set(ip_list)
    all_ips = existing_ips.union(new_ips)
    
    with open(filename, "w", encoding='utf-8') as file:
        # Write header if file was newly created
        if not existing_ips:
            init_file(filename)
        
        for ip_info in sorted(all_ips):
            file.write(ip_info + "\n")

def main():
    filename = "IP.China.list"
    url = "https://example.com/ipdata"
    
    html = fetch_ip_data(url)  # 抓取数据
    if html:
        ip_list = parse_ip_data(html)  # 解析数据
        if ip_list:  # 仅当解析到数据时才更新
            update_ip_file(filename, ip_list)  # 更新文件

if __name__ == "__main__":
    main()
