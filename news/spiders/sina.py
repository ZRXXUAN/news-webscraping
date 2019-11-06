# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import json
from news.tools.general.parse_time import parse_time
from news.tools.sina.get_attribute import *
import requests


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    # headers = {
    #               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    #               'Accept-Encoding': 'gzip, deflate, br',
    #               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    #               'Cache-Control': 'no-cache',
    #               'Pragma': 'no-cache',
    #               'Upgrade-Insecure-Requests': '1',
    #               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    # }  # 加了cookie也没用，新浪把服务器的ip给封了

    def start_requests(self):
        urls = [
            # https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2974&k=&num=50&page=2&r=0.1585142920888456&callback=jQuery11120942672074972815_1564159887601&_=1564159887603
            # 07270052
            'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page=1'.format(NEWS),
            'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page=1'.format(SPORTS),
            'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page=1'.format(ENTERTAINMENT),
            'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page=1'.format(TECHNOLOGY),
            'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page=1'.format(FINANCE),
        ]
        for url in urls:
            for page in range(1, 5):  # 对前几页进行增量爬取
                next_page_url = url.replace('page=1', 'page={}'.format(page))
                # for index in range(1, 5):  # 测试出可用的代理ip  #实际测试发现scrapy有请求失败重新发起请求的机制，但是万一一个ip就是不行怎么办？我想着加一个下载器中间件
                #     response_ip = requests.get("http://proxypool:5555/random")
                #     proxy_ip = response_ip.text
                #     try:
                #         response = requests.get(next_page_url, proxies={'http': 'http://{}'.format(proxy_ip),
                #                                                         'https': 'http://{}'.format(proxy_ip)})
                #     except Exception as e:
                #         print('代理测试Error: ', e)
                #     else:
                #         if response.status_code == 200:
                #             break
                response_ip = requests.get("http://proxypool:5555/random")
                proxy_ip = response_ip.text
                yield scrapy.Request(url=next_page_url, callback=self.parse_data_list, meta={'proxy': 'http://{}'.format(proxy_ip)})

    def parse_data_list(self, response):
        response_dict = json.loads(response.text)
        data_list = response_dict['result']['data']  # 一个列表
        lid = response_dict['result']['lid']
        for data in data_list:
            if 'video' in data['url'] or 'k.sina' in data['url']:
                continue
            news_item = NewsItem()
            news_item['title'] = data['title']
            news_item['date'] = parse_time(data['ctime'])
            news_item['source'] = data['media_name']
            news_item['url'] = data['url']
            news_item['attribute'] = lid  # 这里只是为了方便之后对属性的解析，不是最终结果
            yield scrapy.Request(url=data['url'], callback=self.parse_article1, meta={'news_item': news_item})

    def parse_article1(self, response):
        # news_item = NewsItem()
        news_item = response.meta['news_item']
        news_item['attribute'] = get_attribute(news_item['attribute'])
        news_item['content'] = response.xpath(
            '//div[@id="artibody"]//p//text()').extract()  # 这里text()前面的双斜杠很重要，因为有些p节点里面还有设置字体类型的span
        if not news_item['content']:
            news_item['content'] = response.xpath(
                '//div[@id="article"]//p//text()').extract()
        news_item['source_url'] = response.xpath(
            '//a[@data-sudaclick="media_name"]/@href|//a[@data-sudaclick="content_media_p"]/@href|//span[@data-sudaclick="media_name"]/a/@href').extract()
        yield news_item
