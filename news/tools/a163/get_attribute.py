def get_attribute(api_url, article_url):
    # 如果api的url中带有dy.163，是网易号，无法通过文章url判断属性，需要从api的url来判断，
    # 如果api的url不带有dy.163，则通过文章的url来判断属性，因为有些api返回的文章url列表不全是该api指向的属性的，
    # 有可能一个新闻的api返回了体育的文章
    if 'dy.163' in article_url:
        return get_attribute_api(api_url)
    else:
        return get_attribute_article(article_url)


def get_attribute_article(url):
    if 'sports' in url or '2018.' in url:
        attribute = "体育"
    elif 'ent' in url:
        attribute = "娱乐"
    elif 'tech' in url:
        attribute = "科技"
    elif 'money' in url:
        attribute = "财经"
    elif 'news' in url or 'war.' in url:
        attribute = "新闻"
    else:
        attribute = ''
    return attribute


def get_attribute_api(url):
    if 'sports' in url:
        attribute = "体育"
    elif 'ent' in url:
        attribute = "娱乐"
    elif 'tech' in url:
        attribute = "科技"
    elif 'money' in url:
        attribute = "财经"
    elif 'temp' in url:
        attribute = "新闻"
    else:
        attribute = ''
    return attribute
