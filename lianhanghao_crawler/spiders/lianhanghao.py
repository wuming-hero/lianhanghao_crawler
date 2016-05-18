# -*- coding: utf-8 -*-
import json
import urlparse

import requests
import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

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
    # bank_list = [('1', '中国工商银行'), ('2', '中国农业银行'), ('3', '中国银行'), ('4', '中国建设银行'), ('5', '国家开发银行'),
    #              ('6', '中国进出口银行'), ('7', '中国农业发展银行'), ('8', '交通银行'), ('9', '中国邮政储蓄银行'), ('10', '中信银行'),
    #              ('11', '中国光大银行'), ('12', '华夏银行'), ('13', '中国民生银行'), ('14', '广东发展银行'), ('15', '深圳发展银行'),
    #              ('16', '招商银行'), ('17', '兴业银行'), ('18', '上海浦东发展银行'), ('19', '城市商业银行'), ('20', '农村商业银行'),
    #              ('21', '恒丰银行'), ('22', '农村合作行'), ('23', '渤海银行'), ('24', '徽商银行'), ('25', '城市信用社'), ('26', '农村信用联社'),
    #              ('27', '香港上海汇丰银行'), ('28', '东亚银行'), ('29', '南洋商业银行'), ('30', '恒生银行'), ('31', '中国银行（香港）'),
    #              ('32', '(香港地区)银行'), ('33', '集友银行'), ('34', '星展银行（香港）'), ('35', '永亨银行'), ('36', '美国花旗银行'),
    #              ('37', '美国银行'), ('38', '美国摩根大通银行'), ('39', '日本三菱东京日联银行'), ('40', '日本日联银行'), ('41', '日本三井住友银行'),
    #              ('42', '日本瑞穗实业银行'), ('43', '日本山口银行'), ('44', '韩国外换银行'), ('45', '韩国新韩银行'), ('46', '韩国友利银行'),
    #              ('47', '韩国产业银行'), ('48', '韩国中小企业银行'), ('49', '新加坡星展银行'), ('50', '奥地利中央合作银行'), ('51', '比利时联合银行'),
    #              ('52', '荷兰银行'), ('53', '荷兰商业银行'), ('54', '渣打银行'), ('55', '法国兴业银行'), ('56', '法国巴黎银行'),
    #              ('57', '法国东方汇理银行'), ('58', '德国德累斯登银行'), ('59', '德意志银行'), ('60', '德国商业银行'), ('61', '德国西德银行'),
    #              ('62', '德国巴伐利亚州银行'), ('63', '瑞士信贷银行'), ('64', '加拿大蒙特利尔银行'), ('65', '澳大利亚和新西兰银行集团'),
    #              ('66', '德富泰银行'), ('67', '厦门国际银行'), ('68', '法国巴黎银行（中国）'), ('69', '平安银行'), ('70', '青岛国际银行'),
    #              ('71', '华一银行')]

    # 数据循环太多 有时中间会报 http connect error
    # 为了效率起见 分开执行部分数据量比较大的银行
    banks1 = [('1', '中国工商银行')]
    # banks2 = [('2', '中国农业银行')]
    # banks3 = [('3', '中国银行')]
    # banks4 = [('4', '中国建设银行')]
    # banks5 = [('5', '国家开发银行'), ('6', '中国进出口银行'), ('7', '中国农业发展银行')]
    # banks6 = [('8', '交通银行')]
    # banks7 = [('9', '中国邮政储蓄银行')]
    # banks8 = [('10', '中信银行')]
    # banks9 = [('11', '中国光大银行'), ('12', '华夏银行'), ('13', '中国民生银行'), ('14', '广东发展银行'), ('15', '深圳发展银行')]
    # banks10 = [('16', '招商银行')]
    # banks11 = [('17', '兴业银行')]
    # banks12 = [('18', '上海浦东发展银行'), ('19', '城市商业银行'), ('20', '农村商业银行'),
    #            ('21', '恒丰银行'), ('22', '农村合作行'), ('23', '渤海银行'), ('24', '徽商银行'), ('25', '城市信用社'), ('26', '农村信用联社'),
    #            ('27', '香港上海汇丰银行'), ('28', '东亚银行'), ('29', '南洋商业银行'), ('30', '恒生银行')]
    # banks13 = [('31', '中国银行（香港）'), ('32', '(香港地区)银行'), ('33', '集友银行'), ('34', '星展银行（香港）'), ('35', '永亨银行'),
    #            ('36', '美国花旗银行'), ('37', '美国银行'), ('38', '美国摩根大通银行'), ('39', '日本三菱东京日联银行'), ('40', '日本日联银行'),
    #            ('41', '日本三井住友银行'), ('42', '日本瑞穗实业银行'), ('43', '日本山口银行'), ('44', '韩国外换银行'), ('45', '韩国新韩银行'),
    #            ('46', '韩国友利银行'), ('47', '韩国产业银行'), ('48', '韩国中小企业银行'), ('49', '新加坡星展银行'), ('50', '奥地利中央合作银行'),
    #            ('51', '比利时联合银行'), ('52', '荷兰银行'), ('53', '荷兰商业银行'), ('54', '渣打银行'), ('55', '法国兴业银行'), ('56', '法国巴黎银行'),
    #            ('57', '法国东方汇理银行'), ('58', '德国德累斯登银行'), ('59', '德意志银行'), ('60', '德国商业银行'), ('61', '德国西德银行'),
    #            ('62', '德国巴伐利亚州银行'), ('63', '瑞士信贷银行'), ('64', '加拿大蒙特利尔银行'), ('65', '澳大利亚和新西兰银行集团'),
    #            ('66', '德富泰银行'), ('67', '厦门国际银行'), ('68', '法国巴黎银行（中国）'), ('69', '平安银行'), ('70', '青岛国际银行'),
    #            ('71', '华一银行')]

    province_dict = {'4': '山西省', '24': '贵州省', '8': '黑龙江省', '10': '江苏省', '2': '天津市', '25': '云南省',
                     '34': '澳门', '14': '江西省', '33': '香港', '7': '吉林省', '32': '台湾', '12': '安徽省', '19': '广东省',
                     '5': '内蒙古自治区', '11': '浙江省', '26': '西藏自治区', '18': '湖南省', '9': '上海市', '29': '青海省', '31': '新疆维吾尔族自治区',
                     '15': '山东省', '13': '福建省', '3': '河北省', '23': '重庆市', '16': '河南省', '17': '湖北省', '27': '陕西省',
                     '1': '北京市', '22': '四川省', '28': '甘肃省', '20': '广西壮族自治区', '21': '海南省', '30': '宁夏回族自治区', '6': '辽宁省'}

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath("//table/tbody/tr").extract()
        # 取得当前查询结果的限额条件
        param = self.get_param(response)
        for tr in trs:
            yield self.parse_item(tr, **param)

        if self.first:
            for bank_tuple in self.banks1:
                self.first = False
                for province, province_name in self.province_dict.iteritems():
                    city_list = self.get_city(province)
                    for item in city_list:
                        bank_now = bank_tuple[0]
                        new_start_url = '%s/index.php?&key=&bank=%s&province=%s&city=%s&page=1' % (
                            self.domain, bank_now, province, item['id'])
                        # 取得当前分类 pages的第1页内容
                        print '-----------new_start_url: %s' % new_start_url
                        request = scrapy.Request(new_start_url, callback=self.parse)
                        yield request
        else:
            # 直接获取跳转页全部链接
            pages = sel.xpath("//div[@class='pager']/select/option/@value").extract()
            if len(pages) > 1:
                for page_link in pages[1:]:
                    print '++++++++++++++++++++page_link: %s' % page_link
                    request = scrapy.Request('%s/%s' % (self.domain, page_link), callback=self.parse)
                    yield request

        # 原 pages 控制逻辑 以"下一页" 分页查询
        # pages = sel.xpath("//div[@class='pager']/a/@href").extract()
        # print('pages: %s' % pages)
        # if len(pages) > 2:
        #     # 取倒数第2个链接 即"下一页"的链接 当最后一页时,此时的 page_link 为 N-2页的链接 scrapy 检测到重复 自动停止运行
        #     page_link = pages[-2]
        #     print '----------pages_link: %s' % page_link
        #     request = scrapy.Request('%s/%s' % (self.domain, page_link), callback=self.parse)
        #     yield request

    def parse_item(self, text, **kwargs):
        pass
        sel = Selector(text=text)
        l = ItemLoader(item=LianhanghaoCrawlerItem(), selector=Selector(text=text))
        # 取 tr下面的N个 td 的内容 xpath 的语法竟然是从下标1开始的取值的
        bank_number = sel.xpath("//td[2]//text()").extract()
        bank_name = sel.xpath("//td[3]//text()").extract()
        phone_tmp = sel.xpath("//td[4]//text()").extract()
        phone = phone_tmp if len(phone_tmp) else ""
        address_tmp = sel.xpath("//td[5]//text()").extract()
        address = address_tmp if len(address_tmp) else ""
        l.add_value('bank_number', bank_number)
        l.add_value('bank_name', bank_name)
        l.add_value('phone', phone)
        l.add_value('address', address)

        # 传入限定条件参数
        l.add_value('bank_id', kwargs['bankId'])
        l.add_value('bank', kwargs['bankName'])
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

    def get_param(self, response):
        sel = Selector(response)
        # 获取选中的银行名称
        bank_id = sel.xpath("//select[@id='bank']/option[contains(@selected, 'selected')]/@value").extract()
        bank_name = sel.xpath("//select[@id='bank']/option[contains(@selected, 'selected')]/text()").extract()

        # 获取选中的省份
        province = sel.xpath("//select[@id='province']/option[contains(@selected, 'selected')]/@value").extract()
        province_name = sel.xpath("//select[@id='province']/option[contains(@selected, 'selected')]/text()").extract()

        # 获取选中的城市 城市 js 动态生成 无法获取
        # print sel.xpath("//select[@id='city']/option").extract()
        # city = sel.xpath("//select[@id='city']/option[contains(@selected, 'selected')]/@value").extract()
        # city_name = sel.xpath("//select[@id='city']/option[contains(@selected, 'selected')]/text()").extract()

        # url: http://www.lianhanghao.com/index.php?&key=&bank=1&province=1&city=35&page=1
        url = response.url
        result = urlparse.urlparse(url)
        ret = urlparse.parse_qs(result.query, True)
        city = ''.join(ret['city'])
        city_name = ""
        province_code = ret['province']
        city_list = self.get_city("".join(province_code))
        for item in city_list:
            if item['id'] == city:
                city_name = item['name']
                break
        param = {
            'bankId': bank_id,
            'bankName': bank_name,
            'province': province,
            'provinceName': province_name,
            'city': city,
            'cityName': city_name
        }
        if bank_id != self.bank_now:
            print '============bankId: %s===============bankName: %s' % (bank_id, bank_name)
            self.bank_now = bank_id
        return param
