# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
import json
from news.tools.qq.get_attribute import get_attribute
from news.tools.general.parse_time import get_today_date, get_yesterday_date
from news.tools.qq.get_dynamic_content import get_dynamic_content


class QqSpider(scrapy.Spider):  # 观察专题，怎么爬，是否要爬，这个在JS里有吗  # 滚动新闻和推荐新闻都要爬，因为都不完全
    # article_type=0文章 =11专题 =56, =3视频
    # 新闻下拉https://pacaio.match.qq.com/irs/rcd?cid=137&page=0&token=d0f13d594edfc180f5bf6b845456f3ea&ext=top
    # 滚动新闻https://pacaio.match.qq.com/openapi/json?key=news:20190530&num=15&page=0
    name = 'qq'
    allowed_domains = ['qq.com']
    start_urls = [
        'https://pacaio.match.qq.com/openapi/json?key=news:{}&num=15&page=0'.format(get_today_date()),  # 新闻
        'https://pacaio.match.qq.com/openapi/json?key=sports:{}&num=15&page=0'.format(get_today_date()),  # 体育
        'https://pacaio.match.qq.com/openapi/json?key=ent:{}&num=15&page=0'.format(get_today_date()),  # 娱乐
        'https://pacaio.match.qq.com/openapi/json?key=tech:{}&num=15&page=0'.format(get_today_date()),  # 科技
        'https://pacaio.match.qq.com/openapi/json?key=finance:{}&num=15&page=0'.format(get_today_date()),  # 财经 以上为滚动新闻
        'https://pacaio.match.qq.com/openapi/json?key=news:{}&num=15&page=0'.format(get_yesterday_date()),  # 新闻昨天的新闻也爬爬，因为前一天的定时任务结束后可能又产生新的新闻
        'https://pacaio.match.qq.com/openapi/json?key=sports:{}&num=15&page=0'.format(get_yesterday_date()),  # 体育
        'https://pacaio.match.qq.com/openapi/json?key=ent:{}&num=15&page=0'.format(get_yesterday_date()),  # 娱乐
        'https://pacaio.match.qq.com/openapi/json?key=tech:{}&num=15&page=0'.format(get_yesterday_date()),  # 科技
        'https://pacaio.match.qq.com/openapi/json?key=finance:{}&num=15&page=0'.format(get_yesterday_date()),  # 财经 以上为滚动新闻
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=news&page=0',  # 新闻，以下为热点精选
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=world&page=0',  # 国际新闻
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=society&page=0',  # 社会新闻
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=sports&page=0',  # 体育
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=ent&page=0',  # 娱乐
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=tech&page=0',  # 科技
        'https://pacaio.match.qq.com/irs/rcd?cid=146&token=49cbb2154853ef1a74ff4e53723372ce&ext=finance&page=0',  # 财经 注意token会不会失效
    ]

    def parse(self, response):
        if 'openapi' in response.url:
            index = 20
        else:
            index = 19  # 似乎18之后的都是视频，虽然日期可能有当日的，前十八应该是时间顺序来的
        for page in range(0, index):
            next_url = response.url.replace('page=0', 'page={}'.format(page))
            yield scrapy.Request(next_url, self.parse_data_list)

    def parse_data_list(self, response):
        data_list = json.loads(response.text)['data']
        if not data_list:
            return
        for data in data_list:
            if data['article_type'] != 0:  # 确保只爬文章类型的链接
                continue
            items = NewsItem()
            if 'openapi' in response.url:
                items['url'] = data['url']
            else:
                items['url'] = data['vurl']
            items['date'] = data['publish_time'][:16]
            items['title'] = data['title']
            items['source'] = data['source']
            items['attribute'] = get_attribute(response.url)
            items['source_url'] = ''
            yield scrapy.Request(items['url'], self.parse_article1, meta={'items': items})

    def parse_article1(self, response):
        items = response.meta['items']
        if 'https://new.qq.com/notfound.htm' in items['url']:
            print('404page in url')
        items['content'] = response.xpath(
            '//div[@class="content-article"]//p//text()').extract()
        if not items['content']:
            print("invoke get_dynamic_content(), url: ", items['url'])
            items['content'] = get_dynamic_content(items['url'])
        return items

    # def parse_article2(self, items):  # 动态页面，没有html后缀
    #     # 正则获取动态页面请求JS的id参数
    #     items['content'] = get_dynamic_content(items['url'])
    #     return items

