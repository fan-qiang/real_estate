# -*- coding: utf-8 -*-
import re
from datetime import datetime
from uuid import uuid1

import scrapy
from scrapy.loader import ItemLoader

from real_estate.items import RealEstateItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = "su.lianjia.com"
    # start_urls = ["http://su.lianjia.com/ershoufang/rs"]
    content_page_url = "http://su.lianjia.com{}"

    def start_requests(self):
        url_template = "http://su.lianjia.com/ershoufang/gongyeyuan/d{}rs"
        for idx in range(101, 197):
            yield scrapy.Request(url=url_template.format(idx), callback=self.parse, dont_filter=True)

    def parse(self, response):
        for href in response.xpath('//*[@class="text link-hover-green js_triggerGray js_fanglist_title"]/@href').extract():
            url = self.content_page_url.format(href)
            yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        item = ItemLoader(item=RealEstateItem(), response=response)

        item.add_value("id", str(uuid1()))

        item.add_value("domain", 'lianjia')

        # 简单的描述信息
        item.add_xpath("title", '//*[@class="header-title"]/text()')

        # 小区名称
        item.add_xpath("housing_estate", "//*[@class='maininfo-estate-name']/a[1]/text()")

        # 房产总价万元
        item.add_xpath("price_num", '//*[@class="price-num"]/text()')

        # 小区地址
        item.add_xpath("address", "//*[@class='item-cell maininfo-estate-address']/text()")

        # 房型介绍

        item.add_xpath("rooms", '//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[1]/span[2]/text()')

        # 房源编号

        item.add_xpath("house_code", '//*[@class="maininfo-minor maininfo-item"]/li[4]/span[2]/text()[1]')

        # 抓取的url
        item.add_value("url", response.url)

        # 建筑面积

        item.add_xpath("floorage", '//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[2]/ul/li[3]/span[2]/text()')

        # 装修 0-毛坯 1-简装 2 中等装修 3 精装

        item.add_xpath("decoration_situation",
                       '//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li[2]/span[2]/text()')

        # 每平方米单价

        item.add_xpath("price_unit_num", '//*[@class="price-unit-num"]/span/text()')

        # 楼层
        item.add_xpath("floor", '//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li[1]/span[2]/text()')

        # 房本年限
        item.add_xpath("term", '//*[@id="js-baseinfo-header"]/div[1]/div[2]/div[2]/ul/li[2]/span[2]/text()')

        # 建成时间

        item.add_xpath("year", '//*[@class="main-item u-tr"]/p[2]/text()')

        # 朝向

        item.add_xpath("orientation", '//*[@id="js-baseinfo-header"]/div[1]/div[1]/div[3]/ul/li[3]/span[2]/text()[1]')

        # 标签

        item.add_xpath("tags", '//*[@id="js-baseinfo-header"]/div[1]/div[4]/div[2]/ul/li/span/text()')

        # 城市名称

        item.add_value("city", "苏州")

        # 所处的区域

        item.add_value("district", "工业园区")
        # 数据创建时间

        item.add_value("create_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return item.load_item()




