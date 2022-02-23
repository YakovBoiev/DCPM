import requests

from lxml.html import fromstring
from pymongo import MongoClient

HEADERS = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/97.0.4692.71 Safari/537.36'
}

params = {
        'lang': 'ru',
    }

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'news'
URL = 'https://www.rambler.ru'
ITEM_XPATH = '//div[@class="ILgW"]'
LINK_ITEM = './a/@href'
LINK_DATA = '//div[@class="_3XkdF"]//a'
NEWS = '//div[@class="_3XkdF"]/h1'


def create_news_dict(link, news, news_agency, date):
    return {
        'link': link,
        'news': news,
        'news_agency': news_agency,
        'date': date,
    }


def write_data_db(db, data):
    collection = db['news']
    for news in data:
        if collection.find_one({'link': news['link']}):
            continue
        collection.insert_one(news)


def make_request():
    data = []
    response = requests.get(URL, headers=HEADERS, params=params)
    dom = fromstring(response.text)
    items = dom.xpath(ITEM_XPATH)
    for item in items:
        link = item.xpath(LINK_ITEM)[0]
        response = requests.get(link, headers=HEADERS, params=params)
        dom_news = fromstring(response.text)
        news = dom_news.xpath(NEWS)[0].text
        spam = dom_news.xpath(LINK_DATA)
        if spam:
            date = spam[0].attrib['href']
            news_agency = spam[1].text
            news_data = create_news_dict(link, news, news_agency, date)
            data.append(news_data)
    return data


def pipeline():
    data = make_request()
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        write_data_db(db, data)


if __name__ == "__main__":
    pipeline()




