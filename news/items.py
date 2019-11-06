# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    date = scrapy.Field()
    attribute = scrapy.Field()  # 新闻 | 财经 | 体育 | 娱乐 |  科技 这五类
