def get_attribute(url):
    # start_urls = ['http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page=1&size=20',  # 时政
    #               'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page=1&size=20',  # 国际
    #               'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page=1&size=20',  # 财经 以上三个为新闻
    #               'http://v2.sohu.com/integration-api/mix/region/82?size=25&adapter=pc&page=1',  # 真·财经
    #               'http://v2.sohu.com/integration-api/mix/region/5676?size=25&adapter=pc&page=1',  # 科技  翻30页
    #               'http://v2.sohu.com/integration-api/mix/region/131?size=25&adapter=pc&page=1',  # 娱乐
    #               'http://v2.sohu.com/integration-api/mix/region/4357?size=25&adapter=pc&page=1',  # 4357-4367都是体育，足球、篮球为主
    #               'http://v2.sohu.com/integration-api/mix/region/4302?size=25&adapter=pc&page=1',  # 综合体育
    #               ]

    if 'public-api' in url:
        return '新闻'
    elif '/82' in url:
        return '财经'
    elif '/5676' in url:
        return '科技'
    elif '/131' in url:
        return '娱乐'
    elif '/4357' in url or '/4302' in url:
        return '体育'
