import requests

from lxml.html import fromstring


HEADERS = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/97.0.4692.71 Safari/537.36'
}

params = {
        'lang': 'ru',
    }


URL = 'https://www.yandex.ru'
ITEM_XPATH = "//*[@id='news_panel_news']//li"
LINK_ITEM = "./a/@href"

response = requests.get(URL, headers=HEADERS, params=params)
dom = fromstring(response.text)
items = dom.xpath(ITEM_XPATH)
for item in items:
    href = item.xpath(LINK_ITEM)[0]
    print(href)
print()


/html/body/div[1]/div[3]/div[1]/div/div/div/div[1]/span



