# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
import pymysql
from common.helpers import daytime_formate


class LianhanghaoCrawlerPipeline(object):
    def process_item(self, item, spider):
        # print '---------------item: %s' % item
        # item = {'address': [u'\u5c71\u897f\u7701\u592a\u539f\u5e02\u8fce\u6cfd\u5927\u8857213\u53f7'],
        #         'bank': [u'\u6e24\u6d77\u94f6\u884c'],
        #         'bank_id': [u'23'],
        #         'bank_name': [u'\u6e24\u6d77\u94f6\u884c\u80a1\u4efd\u6709\u9650\u516c\u53f8\u592a\u539f\u5206\u884c'],
        #         'bank_number': [u'318161000018'],
        #         'city': ['48'],
        #         'city_name': [u'\u592a\u539f\u5e02'],
        #         'phone': [u'0351-8385093'],
        #         'province': [u'4'],
        #         'province_name': [u'\u5c71\u897f\u7701']}
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password="",
                                     db='fula_local',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # 修正省份数据
                sql = "SELECT * FROM base_province WHERE provinceName=%s"
                cursor.execute(sql, (item['province_name'],))
                result = cursor.fetchone()
                if result:
                    item['province'] = result['provinceCode']
                # 修正城市数据
                sql = "SELECT * FROM base_city WHERE parentCode=%s AND cityName=%s"
                cursor.execute(sql, (item['province'], item['city_name']))
                ret = cursor.fetchone()
                if ret:
                    item['city'] = ret['cityCode']

            with connection.cursor() as cursor:
                # Create a new record
                now_time = daytime_formate(datetime.now())
                insert_data = (item['bank_id'], item['bank'], item['bank_number'], item['bank_name'], item['province'],
                               item['province_name'], item['city'], item['city_name'], item['phone'], item['address'],
                               now_time, now_time)
                print '--------item: %s---------data: %s' % (item, insert_data)
                sql = "INSERT INTO fl_lianhanghao (bankId, bank, bankNumber, bankName, province, provinceName, city, cityName, phone, address, createTime, modifyTime) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)"
                cursor.execute(sql, insert_data)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        finally:
            connection.close()
