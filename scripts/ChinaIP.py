import requests
from lxml import etree
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_and_save(url, filename, xpath_expression):
    """从 URL 获取数据并保存到文件"""
    session = requests.Session()
    try:
        r = session.get(url)
        r.raise_for_status()  # 确保请求成功
        tree = etree.HTML(r.text)
        asns = tree.xpath(xpath_expression)[0].text
        data = json.loads(asns).get('payload', {}).get('blob', {}).get('rawLines', [])
        
        with open(filename, "w") as file:
            for line in data:
                file.write(line + '\n')
        logging.info(f"Data saved to {filename}")
    except (requests.RequestException, IndexError, json.JSONDecodeError, TypeError) as e:
        logging.error(f"Error fetching or processing data from {url}: {e}")

# URL 和文件名以及 XPath 表达式
urls_and_files = {
    ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china.list", '//*[@data-target="react-app.embeddedData"]'): "IP.China.list",
    ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china4.list", '//*[@data-target="react-app.embeddedData"]'): "IPv4.China.list",
    ("https://github.com/cbuijs/ipasn/blob/master/country-asia-china6.list", '//*[@data-target="react-app.embeddedData"]'): "IPv6.China.list"
}

# 处理每个 URL 和文件名
for (url, xpath), filename in urls_and_files.items():
    fetch_and_save(url, filename, xpath)
