# -*- coding: utf-8 -*-
from datetime import datetime

import pymysql

from common.helpers import daytime_formate

connection = pymysql.connect(host='localhost',
                             user='root',
                             password="",
                             db='fula_local',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

province_dict = {'4': '山西省', '24': '贵州省', '8': '黑龙江省', '10': '江苏省', '2': '天津市', '25': '云南省',
                 '34': '澳门', '14': '江西省', '33': '香港', '7': '吉林省', '32': '台湾', '12': '安徽省', '19': '广东省',
                 '5': '内蒙古自治区', '11': '浙江省', '26': '西藏自治区', '18': '湖南省', '9': '上海市', '29': '青海省', '31': '新疆维吾尔族自治区',
                 '15': '山东省', '13': '福建省', '3': '河北省', '23': '重庆市', '16': '河南省', '17': '湖北省', '27': '陕西省',
                 '1': '北京市', '22': '四川省', '28': '甘肃省', '20': '广西壮族自治区', '21': '海南省', '30': '宁夏回族自治区', '6': '辽宁省'}
try:
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * from fl_lianhanghao where city < 11000 group BY city"
        cursor.execute(sql, ())
        result = cursor.fetchall()
        print len(result), result

        for item in result:
            sql = "SELECT * from `base_city` WHERE parentCode = %s and cityName=%s"
            cursor.execute(sql, ('650000', item['cityName']))
            ret = cursor.fetchone()
            if ret:
                update_sql = "UPDATE `fl_lianhanghao` SET city = %s where city=%s"
                cursor.execute(update_sql, (ret['cityCode'], item['city']))
    # with connection.cursor() as cursor:
    #     now_time = daytime_formate(datetime.now())
    #     insert_data = ('', '', now_time, now_time)
    #     sql = "INSERT INTO fl_bank (id, bank, createTime, modifyTime) VALUES (%s, %s, %s,%s)"
    #     # print '--------item: %s--------data: %s' % (item, insert_data)
    #     cursor.execute(sql, insert_data)
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


finally:
    connection.close()
