# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import json
from news.tools.general.parse_time import parse_time
from news.tools.sohu.get_attribute import get_attribute


class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = [
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page=1&size=20',  # 时政
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page=1&size=20',  # 国际
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page=1&size=20',  # 财经 以上三个为新闻
                  'http://v2.sohu.com/integration-api/mix/region/82?size=25&adapter=pc&page=1',  # 真·财经
                  'http://v2.sohu.com/integration-api/mix/region/5676?size=25&adapter=pc&page=1',  # 科技  翻30页
                  'http://v2.sohu.com/integration-api/mix/region/131?size=25&adapter=pc&page=1',  # 娱乐
                  'http://v2.sohu.com/integration-api/mix/region/4357?size=25&adapter=pc&page=1',  # 4357-4367都是体育，足球、篮球为主
                  'http://v2.sohu.com/integration-api/mix/region/4302?size=25&adapter=pc&page=1',  # 综合体育
                  ]

    def parse(self, response):
        for index in range(1, 30):
            next_url = response.url.replace('page=1', 'page={}'.format(index))
            yield scrapy.Request(next_url, self.parse_data_list)

    def parse_data_list(self, response):
        if 'public-api' in response.url:# 是新闻类型的API
            data_list = json.loads(response.text)
        elif 'integration-api' in response.url:
            data_list = json.loads(response.text)['data']
        else:
            return
        for data in data_list:
            if ('integration-api' in response.url) and (data['resourceType'] == 3):
                continue
            if data['type'] == 3:  # 是图集
                continue
            items = NewsItem()
            try:
                items['title'] = data['title']
                # items['source_url'] = data['originalSource']  # public-api有来源url，integration无，统一从页面中采集，在网页源代码里有，但JS渲染不可见
                items['url'] = 'http://www.sohu.com/a/' + str(data['id']) + '_' + str(data['authorId'])
                items['date'] = parse_time(str(data['publicTime'])[0:10])
                items['source'] = data['authorName']
            except KeyError:  # 其中一个原因：不是文章而是集合，所以没有authorId，authorName
                print(data_list.index(data))
                print(response.url)
                print(data)
                return
            items['attribute'] = get_attribute(response.url)
            yield scrapy.Request(items['url'], self.parse_article1, meta={'items': items})

    def parse_article1(self, response):
        items = response.meta['items']
        items['content'] = response.xpath(
            '//article[@class="article"]//p//text()').extract()
        if not items['content']:
            items['content'] = response.xpath(
                '//article[@class="article-text"]//p//text()').extract()
        items['source_url'] = response.xpath(
            '//span[@data-role="original-link"]/a/@href').extract()
        yield items
