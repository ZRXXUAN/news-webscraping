import requests
HEADERS = {'Content-Type': 'application/json'}
TEST_ITEM = {
    'title': '测试',
    'attribute': '测试',
    'content': '重复保存测试2',
    'date': '2019-09-16 16:59:00',
    'url': '测试',
    'source': '测试',
    'source_url': '测试',
}


def save(item, save_url):
    save_url = save_url
    data_json = {
            "newTitle": item['title'],
            "newType": item['attribute'],
            "author": None,
            "text": item['content'],
            "publishDate": item['date'],
            "url": item['url'],
            "source": item['source'],
            "actualUrl": item['source_url'],
        }
    try:
        response = requests.post(url=save_url, json=data_json, headers=HEADERS)
    except Exception as e:
        print("REQUESTS ERROR: "+str(e))
    else:
        if response.status_code != 200:
            print("SAVE ERROR: response code is not equal to 200")
        elif 'code' in response.json() and response.json()['code'] != 200:
            print("SAVE ERROR: save code is not equal to 200")


def get():
    get_url = 'http://120.24.90.180:8008/v1/api/new/all'
    get_url = get_url
    print(requests.get(url=get_url, headers=HEADERS).text)


# save(TEST_ITEM, 'http://120.24.90.180:8008/v1/api/new/add')
get()
