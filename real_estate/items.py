# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader.processors import MapCompose, Join, TakeFirst


def str_strip(str_value):
    return str_value.strip()


def extract_num(str_value):
    return re.findall(r'^[1-9]\d*\.\d*|0\.\d*[1-9]\d*$', str_value)


def extract_integer(str_value):
    return re.findall(r'^[1-9]\d*', str_value)


class RealEstateItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field(
        output_processor=TakeFirst()
    )

    # 站点目前主要包括 lianjia,shoufang,5i5j
    domain = scrapy.Field(
        output_processor=TakeFirst()
    )
    # 简单的描述信息
    title = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 小区名称
    housing_estate = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )
    # 房产总价万元
    price_num = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 小区地址
    address = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 房型介绍
    rooms = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 房源编号
    house_code = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 抓取的url
    url = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 建筑面积

    floorage = scrapy.Field(
        input_processor=MapCompose(str_strip, extract_num),
        output_processor=TakeFirst()
    )

    # 装修 0-毛坯 1-简装 2 中等装修 3 精装
    decoration_situation = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 每平方米单价
    price_unit_num = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 楼层
    floor = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 小区年限
    term = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 建成时间
    year = scrapy.Field(
        input_processor=MapCompose(str_strip, extract_integer),
        output_processor=TakeFirst()
    )

    # 朝向
    orientation = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 标签
    tags = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=Join()
    )

    # 城市名称
    city = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )

    # 所处的区域
    district = scrapy.Field(
        input_processor=MapCompose(str_strip),
        output_processor=TakeFirst()
    )
    # 数据创建时间
    create_time = scrapy.Field(
        output_processor=TakeFirst()
    )

