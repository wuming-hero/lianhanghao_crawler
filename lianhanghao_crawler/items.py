# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianhanghaoCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bank_number = scrapy.Field()
    bank_name = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
