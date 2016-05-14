# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader, Identity
from scrapy.selector import Selector

from lianhanghao_crawler.items import LianhanghaoCrawlerItem


class LianhanghaoSpider(scrapy.Spider):
    name = "lianhanghao"
    allowed_domains = ["lianhanghao.com"]
    start_urls = (
        'http://www.lianhanghao.com/index.php?bank=&key=&province=&city=&page=1',
    )

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath("//table/tbody/tr").extract()
        for tr in trs:
            p = self.parse_item(tr)
            yield p

        pages = sel.xpath("//div[@class='pager']/a/@href").extract()
        print('pages: %s' % pages)
        if len(pages) > 2:
            page_link = pages[-2]
            print ('pages_link: %s' % page_link)
            request = scrapy.Request('http://www.lianhanghao.com/%s' % page_link, callback=self.parse)
            yield request

    def parse_item(self, text):
        # [u'<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>',
        #  u'<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>',
        #  u'<a href="image3.html">Name: My image 3 <br><img src="image3_thumb.jpg"></a>',
        #  u'<a href="image4.html">Name: My image 4 <br><img src="image4_thumb.jpg"></a>',
        #  u'<a href="image5.html">Name: My image 5 <br><img src="image5_thumb.jpg"></a>']
        # for index, link in enumerate(links):
        #     args = (index, link.xpath('@href').extract(), link.xpath('img/@src').extract())
        #     print 'Link number %d points to url %s and image %s' % args
        # sel = Selector(text=text)
        # l = ItemLoader(item=LianhanghaoCrawlerItem(), selector=Selector(text=text))
        # tds = sel.xpath("//td/text()").extract()
        # print '%s, %s, %s' % (len(tds), type(tds), tds)
        # l.add_value('bank_number', tds[1])
        # l.add_value('bank_name', tds[2])
        # # 过滤没有电话和地址
        # if len(tds) >= 4:
        #     l.add_value('phone', tds[3])
        # else:
        #     l.add_value('phone', u'')
        # if len(tds) >= 5:
        #     l.add_value('address', tds[4])
        # else:
        #     l.add_value('address', u'')
        # return l.load_item()

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
        return l.load_item()
