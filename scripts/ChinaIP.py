
### 更新后的代码

将 `init_file` 函数中的头部信息修改为不包含“Data for”的版本：

```python
import requests
from lxml import etree
import json
import logging
import os
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def fetch_and_save(url, filename, xpath_expression, retries=3, delay=5):
 """从 URL 获取数据并保存到文件"""
 session = requests.Session()
 for attempt in range(retries):
     try:
         # 初始化文件并写入头部信息
         init_file(filename)
         
         r = session.get(url, timeout=10)
         r.raise_for_status()  # 确保请求成功
         tree = etree.HTML(r.text)
         asns = tree.xpath(xpath_expression)[0].text
         data = json.loads(asns).get('payload', {}).get('blob', {}).get('rawLines', [])
         
         with open(filename, "a", encoding='utf-8') as file:  # 追加模式写入数据
             for line in data:
                 file.write(line + '\n')
         logging.info(f"Data saved to {filename}")
         return  # 成功则返回，退出函数
     except (requests.RequestException, IndexError, json.JSONDecodeError, TypeError) as e:
         logging.error(f"Error fetching or processing data from {url}: {e}")
         if attempt < retries - 1:
             logging.info(f"Retrying in {delay} seconds...")
             time.sleep(delay)
 logging.error(f"Failed to fetch and save data from {url} after {retries} attempts")

# URL 和文件名以及 XPath 表达式
urls_and_files = {
 ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china.list", '//*[@data-target="react-app.embeddedData"]'): "IP.China.list",
 ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china4.list", '//*[@data-target="react-app.embeddedData"]'): "IPv4.China.list",
 ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china6.list", '//*[@data-target="react-app.embeddedData"]'): "IPv6.China.list"
}

# 处理每个 URL 和文件名
for (url, xpath), filename in urls_and_files.items():
 fetch_and_save(url, filename, xpath)
