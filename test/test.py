import json

import requests

from lianhanghao_crawler.spiders.lianhanghao import LianhanghaoSpider

a = [11, 12, 13, 24]
for item in a:
    print item

province = "1"
url = "http://www.lianhanghao.com/area.php?act=ajax&id=" + province
param = {'act': 'ajax', 'id': province}
response = requests.get(url, param)
print response.url, response.status_code
city_list = json.loads(response.content)['city']
print city_list