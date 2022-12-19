import datetime
import json
import locale

import requests
from lxml import html

url = 'https://lenta.ru/parts/news'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
today = datetime.datetime.now()
news_date = today.strftime("%d %B %Y")


def get_news():
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_list = dom.xpath("//li[contains(@class, 'parts-page__item')]")
    news_dict = {}
    news_dict['News'] = []
    
    for news in news_list:
        title = news.xpath("//h3[contains(@class, 'card-full-news__title')]/text()")
        news_date = news.xpath("//time/text()")
        link = news.xpath("//a[contains(@class, 'card-full-news _parts-news')]/@href")

    for i in range(len(news_list) - 1):
        # У Ленты относительные и абсолютные ссылки. Поэтому, если ссылка относительная, добавляем недостающую часть к url
        if 'https' not in link[i]:
            link[i] = url + link[i]
        # если дата публикации сегодня, добавляем дату, так как лента не публикует дату сегодняшних новостей
        if ',' not in news_date[i]:
            news_date[i] = news_date[i] + ', ' + str(today.strftime("%d %B %Y"))
        news_dict['News'].append({
            'title': title[i],
            'url': link[i],
            'time': news_date[i]
        })
    return news_dict


with open('news.json', 'w', encoding='utf-8') as f:
    json.dump(get_news(), f, ensure_ascii=False, indent=2)
print('Данные загружены!')
