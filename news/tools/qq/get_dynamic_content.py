import re
import requests


def get_dynamic_content(url):
    # 正则获取动态页面请求JS的id参数
    time_ymd_re = re.compile('/[0-9]+/')
    index = time_ymd_re.search(url).end()
    id_url = url[index:]

    # 用于从动态渲染的网页的请求JS中获取数据（正文），腾讯新闻
    js_url = 'https://openapi.inews.qq.com/getQQNewsNormalContent?id={}&refer=mobilewwwqqcom'.format(id_url)
    response_json = requests.get(js_url).json()
    content_list = response_json['content']
    true_content = []
    for content in content_list:
        if content['type'] == 1:
            true_content.append(content['value'])
    return true_content
