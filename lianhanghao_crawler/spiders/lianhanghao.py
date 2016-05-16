# -*- coding: utf-8 -*-
import json
import requests
import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.selector import Selector
from urllib3 import request
from lianhanghao_crawler.items import LianhanghaoCrawlerItem


class LianhanghaoSpider(scrapy.Spider):
    name = "lianhanghao"
    domain = "http://www.lianhanghao.com"
    allowed_domains = ["lianhanghao.com"]
    start_urls = (
        '%s/index.php?&key=&bank=1&province=1&city=35&page=1' % domain,
    )
    first = True
    bank_now = "1"
    bank_name_now = u"中国工商银行"
    provice_now = "1"
    province_name_now = u"北京市"
    city_now = "35"
    city_name_now = u"北京市"
    bank_dict = {'38': '美国摩根大通银行', '24': '徽商银行', '54': '渣打银行', '10': '中信银行', '61': '德国西德银行',
                 '64': '加拿大蒙特利尔银行', '7': '中国农业发展银行', '25': '城市信用社', '66': '德富泰银行', '36': '美国花旗银行', '39': '日本三菱东京日联银行',
                 '15': '深圳发展银行', '43': '日本山口银行', '51': '比利时联合银行', '19': '城市商业银行', '63': '瑞士信贷银行', '11': '中国光大银行',
                 '55': '法国兴业银行', '18': '上海浦东发展银行', '57': '法国东方汇理银行', '58': '德国德累斯登银行', '16': '招商银行', '60': '德国商业银行',
                 '41': '日本三井住友银行', '13': '中国民生银行', '47': '韩国产业银行', '3': '中国银行', '12': '华夏银行', '48': '韩国中小企业银行',
                 '42': '日本瑞穗实业银行', '53': '荷兰商业银行', '27': '香港上海汇丰银行', '1': '中国工商银行', '2': '中国农业银行', '56': '法国巴黎银行',
                 '21': '恒丰银行', '30': '恒生银行', '6': '中国进出口银行', '68': '法国巴黎银行（中国）', '4': '中国建设银行', '65': '澳大利亚和新西兰银行集团',
                 '8': '交通银行', '32': '(香港地区)银行', '70': '青岛国际银行', '62': '德国巴伐利亚州银行', '45': '韩国新韩银行', '34': '星展银行（香港）',
                 '71': '华一银行', '44': '韩国外换银行', '14': '广东发展银行', '33': '集友银行', '49': '新加坡星展银行', '40': '日本日联银行',
                 '5': '国家开发银行', '35': '永亨银行', '26': '农村信用联社', '9': '中国邮政储蓄银行', '59': '德意志银行', '46': '韩国友利银行',
                 '52': '荷兰银行', '50': '奥地利中央合作银行', '67': '厦门国际银行', '23': '渤海银行', '29': '南洋商业银行', '17': '兴业银行',
                 '28': '东亚银行', '22': '农村合作银行', '69': '平安银行', '20': '农村商业银行', '37': '美国银行', '31': '中国银行（香港）'}
    province_dict = {'4': '山西省', '24': '贵州省', '8': '黑龙江省', '10': '江苏省', '2': '天津市', '25': '云南省',
                     '34': '澳门', '14': '江西省', '33': '香港', '7': '吉林省', '32': '台湾', '12': '安徽省', '19': '广东省',
                     '5': '内蒙古自治区', '11': '浙江省', '26': '西藏自治区', '18': '湖南省', '9': '上海市', '29': '青海省', '31': '新疆维吾尔族自治区',
                     '15': '山东省', '13': '福建省', '3': '河北省', '23': '重庆市', '16': '河南省', '17': '湖北省', '27': '陕西省',
                     '1': '北京市', '22': '四川省', '28': '甘肃省', '20': '广西壮族自治区', '21': '海南省', '30': '宁夏回族自治区', '6': '辽宁省'}

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath("//table/tbody/tr").extract()
        param = {
            'province': self.provice_now,
            'provinceName': self.province_name_now,
            'city': self.city_now,
            'cityName': self.city_name_now
        }
        for tr in trs:
            # load_item
            yield self.parse_item(tr, **param)

        if self.first:
            for bank, bank_name in self.bank_dict.iteritems():
                self.first = False
                for province, province_name in self.province_dict.iteritems():
                    city_list = self.get_city(province)
                    for item in city_list:
                        city = item['id']
                        self.bank_now = bank
                        self.provice_now = province
                        self.provice_name_now = province_name
                        self.city_now = city
                        self.city_name_now = item['name']
                        new_start_url = '%s/index.php?&key=&bank=%s&province=%s&city=%s&page=1' % (
                            self.domain, self.bank_now, self.provice_now, self.city_now)
                        # 取得当前分类 pages
                        print '-----------new_start_url: %s' % new_start_url
                        request = scrapy.Request(new_start_url, callback=self.parse)
                        yield request
        else:
            pages = sel.xpath("//div[@class='pager']/select/option/@value").extract()
            print '=================pages: %s' % pages
            if len(pages) > 1:
                for page_link in pages[1:]:
                    print '=================page_link: %s' % page_link
                    request = scrapy.Request('%s/%s' % (self.domain, page_link), callback=self.parse)
                    yield request

        # 原 pages 控制逻辑
        # pages = sel.xpath("//div[@class='pager']/a/@href").extract()
        # print('pages: %s' % pages)
        # if len(pages) > 2:
        #     # 取倒数第2个 即"下一页"的链接
        #     page_link = pages[-2]
        #     print ('pages_link: %s' % page_link)
        #     request = scrapy.Request('%s/%s' % ( self.domain, page_link), callback=self.parse)
        #     yield request

    def parse_item(self, text, **kwargs):
        sel = Selector(text=text)
        l = ItemLoader(item=LianhanghaoCrawlerItem(), selector=Selector(text=text))
        tds = sel.xpath("//td").extract()
        # print '%s, %s, %s' % (len(tds), type(tds), tds)
        for index, td in enumerate(tds):
            text_list = Selector(text=td).xpath("//text()").extract()
            if index == 1:
                l.add_value('bank_number', text_list[0])
            elif index == 2:
                l.add_value('bank_name', text_list[0])
            elif index == 3:
                phone = text_list[0] if len(text_list) > 0 else ""
                l.add_value('phone', phone)
            elif index == 4:
                address = text_list[0] if len(text_list) > 0 else ""
                l.add_value('address', address)

        # 传入限定条件参数
        l.add_value('province_name', kwargs['provinceName'])
        l.add_value('province', kwargs['province'])
        l.add_value('city_name', kwargs['cityName'])
        l.add_value('city', kwargs['city'])
        return l.load_item()

    def get_city(self, province):
        url = "%s/area.php?act=ajax&id=%s" % (self.domain, province)
        param = {'act': 'ajax', 'id': province}
        response = requests.get(url, param)
        city_list = json.loads(response.content)['city']
        return city_list
