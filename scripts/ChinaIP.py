import requests
from lxml import etree
import json

allChina = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china.list"

v4China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china4.list"

v6China = "https://github.com/cbuijs/ipasn/blob/master/country-asia-china6.list"

r = requests.get(allChina)
tree = etree.HTML(r.text)
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
x = json.loads(asns)['payload']['blob']['rawLines']
with open("IP.China.list", "w", ) as allChinaIP:
    for i in x:
        allChinaIP.write(i)
        allChinaIP.write('\n')
#
r = requests.get(v4China)
tree = etree.HTML(r.text)
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
x = json.loads(asns)['payload']['blob']['rawLines']
with open("IPv4.China.list", "w") as v4ChinaIP:
    for i in x:
        v4ChinaIP.write(i)
        v4ChinaIP.write('\n')

r = requests.get(v6China)
tree = etree.HTML(r.text)
asns = tree.xpath('//*[@data-target="react-app.embeddedData"]')[0].text
x = json.loads(asns)['payload']['blob']['rawLines']
with open("IPv6.China.list", "w") as v6ChinaIP:
    for i in x:
        v6ChinaIP.write(i)
        v6ChinaIP.write('\n')
