# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import json
from news.tools.a163.get_data_163 import get_date
from news.tools.a163.get_attribute import get_attribute
from news.tools.a163.not_news_url import not_news_url


class A163Spider(scrapy.Spider):
    name = '163'
    allowed_domains = ['163.com']
    start_urls = [
                  'https://temp.163.com/special/00804KVA/cm_yaowen.js',  # 要闻 一页70条
                  'https://temp.163.com/special/00804KVA/cm_guoji.js',  # 国际
                  'https://temp.163.com/special/00804KVA/cm_guonei.js',  # 国内  前三个为新闻
                  'https://sports.163.com/special/000587PR/newsdata_n_index.js',  # 体育要闻
                  'https://sports.163.com/special/000587PR/newsdata_n_nba.js',  # NBA
                  'https://sports.163.com/special/000587PR/newsdata_n_world.js',  # 国际足球
                  'https://sports.163.com/special/000587PR/newsdata_n_china.js',  # 国内足球
                  'https://sports.163.com/special/000587PR/newsdata_n_cba.js',  # CBA
                  'https://sports.163.com/special/000587PR/newsdata_n_allsports.js',  # 综合
                  'https://ent.163.com/special/000380VU/newsdata_index.js',  # 娱乐首页
                  'https://ent.163.com/special/000380VU/newsdata_star.js',  # 明星
                  'https://ent.163.com/special/000380VU/newsdata_movie.js',  # 电影
                  'https://ent.163.com/special/000380VU/newsdata_tv.js',  # 电视剧
                  'https://ent.163.com/special/000380VU/newsdata_show.js',  # 综艺
                  'https://ent.163.com/special/000380VU/newsdata_music.js',  # 音乐
                  'http://tech.163.com/special/gd2016/',  # 科技滚动，这个比较特殊，有单独地滚动页面，并且收入还挺丰富，
                  'https://money.163.com/special/00259BVP/news_flow_index.js',  # 财经首页
                  'https://money.163.com/special/00259BVP/news_flow_stock.js',  # 股票
                  'https://money.163.com/special/00259BVP/news_flow_biz.js',  # 商业
                  'https://money.163.com/special/00259BVP/news_flow_licai.js',  # 理财
                  'https://money.163.com/special/00259BVP/news_flow_fund.js',  # 基金
                  'https://money.163.com/special/00259BVP/news_flow_house.js',  # 房产
                  'https://money.163.com/special/00259BVP/news_flow_car.js',  # 汽车
                  ]
    # http://news.163.com/special/0001220O/news_json.js
    # 网易的api不全，我选择从每种类型新闻的主页的js请求入手，每个主页有后缀_1/2/3可当成页码
    # 新闻选择要闻、国际、国内，或有重复，不过能通过redis过滤，但是在要闻中有杂项，一个是“网易数据”，data.163.com；一个是别的类型的新闻，目前设想通过url前缀来过滤或识别

    def parse(self, response):
        if 'tech' in response.url:  # 科技比较特殊，滚动页面内容收入丰富，且不用请求JS
            yield scrapy.Request(response.url, self.parse_techlist)  # 对初始url进行分析
            for index in range(2, 6):
                next_url = response.url.replace('gd2016', 'gd2016_{:0>2d}'.format(index))
                yield scrapy.Request(next_url, self.parse_techlist)
        else:
            yield scrapy.Request(response.url, self.parse_jslist)
            for index in range(2, 6):  # 实际以新闻要闻为例，5页内为较近新闻，需要一天内多次增量爬取
                next_url = response.url.replace('.js', '_{:0>2d}.js'.format(index))
                yield scrapy.Request(next_url, self.parse_jslist)


    def parse_techlist(self, response):  # 一页20条
        for index in range(1, 21):
            news_item = NewsItem()
            news_item['title'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//h3/a/text()'.format(index)).extract()
            news_item['title'] = news_item['title'][0]
            news_item['url'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//h3/a/@href'.format(index)).extract()
            news_item['url'] = news_item['url'][0]  # 因为是用xpath，所以结果是列表，先转换为字符串，下面的date同理
            if not_news_url(news_item['url']):  # 舍弃不是文章的url
                continue
            news_item['attribute'] = get_attribute(response.url, news_item['url'])
            news_item['date'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//p[@class="sourceDate"]/text()'.format(index)).extract()
            news_item['date'] = news_item['date'][0][:-3]
            yield scrapy.Request(news_item['url'], self.parse_article1, meta={'news_item': news_item})

    def parse_jslist(self, response):
        news_list = json.loads(response.text[14:-1])
        for news in news_list:
            if not_news_url(news['docurl']) or news['newstype'] != 'article':
                continue
            news_item = NewsItem()
            news_item['url'] = news['docurl']
            news_item['attribute'] = get_attribute(response.url, news_item['url'])
            news_item['date'] = get_date(news['time'])
            yield scrapy.Request(news_item['url'], self.parse_article1, meta={'news_item': news_item})

    def parse_article1(self, response):
        news_item = response.meta['news_item']
        if 'dy.163' in response.url:
            self.parse_article2(news_item, response)
            return
        news_item['title'] = response.xpath('//h1/text()').extract()
        news_item['content'] = response.xpath(
            '//div[@id="endText"]//p[not(style)]//text()').extract()
        if not news_item['content']:  # 不保存，只在日志中输出错误
            # news_item['content'] = "ERROR"
            print("news_item is None", response.url)
            return
        news_item['source'] = response.xpath(
            '//div[@class="post_time_source"]/a[@id="ne_article_source"]/text()').extract()
        # 一般来说格式是可以了，但是有些会后带一个地方分部门之类的东西，如下面注释中北京，考虑在pipeline中修改
        news_item['source_url'] = response.xpath(
            '//div[@class="post_time_source"]/a[@id="ne_article_source"]/@href').extract()
        if isinstance(news_item['source_url'], list):
            if len(news_item['source_url']) != 0:
                news_item['source_url'] = news_item['source_url'][0]
            else:
                news_item['source_url'] = 'ERROR'
        if "#" in news_item['source_url']:
            news_item['source_url'] = ''
        yield news_item

    def parse_article2(self, news_item, response):  # 网易号dy(订阅)
        news_item['title'] = response.xpath('//h2/text()').extract()
        news_item['content'] = response.xpath(
            '//div[@class="content"]//p//text()').extract()
        news_item['source'] = response.xpath(
            '//p[@class="time"]/span[3]/text()').extract()
        news_item['source_url'] = ''
        yield news_item

    # def parse_article3(self, news_item, response):  # http://data.2018.163.com/match_detail.html#/prospect/13245886
    #     news_item['content'] = response.xpath(
    #         '//div[@class="article_body"]//p//text()').extract()
    #     news_item['source'] = response.xpath(
    #         '//p[@class="post_time_source clearfix"]/span[2]/text()').extract()
    #     news_item['source_url'] = ''
    #     yield news_item

# 等待适配的网页 http://nba.sports.163.com/2018/match/stat/520010015.html
# http://sports.163.com/18/0608/14/DJPM4T5I00058MJK.html  #不适配
# http://cs.sports.163.com/match/report/1227464.html  # 不适配
