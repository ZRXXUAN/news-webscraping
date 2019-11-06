def get_attribute(url):
    if 'news' in url or 'world' in url or 'society' in url:
        attribute = '新闻'
    elif 'sports' in url:
        attribute = '体育'
    elif 'ent' in url:
        attribute = '娱乐'
    elif 'tech' in url:
        attribute = '科技'
    elif 'finance' in url:
        attribute = '财经'
    else:
        attribute = 'ERROR'

    return attribute
