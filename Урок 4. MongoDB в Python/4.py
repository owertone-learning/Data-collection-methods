import datetime
import locale
from pprint import pprint

import requests
from lxml import html
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
today = datetime.datetime.now()
news_date = today.strftime("%d %B %Y")

client = MongoClient('mongodb://localhost:27017/')
db = client.news_db
db.news


def get_news_lenta():
    url = 'https://lenta.ru/parts/news/'
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_list = dom.xpath("//li[contains(@class, 'parts-page__item')]")
    # news_dict = {}
    for news in news_list:
        title = news.xpath("//h3[contains(@class, 'card-full-news__title')]/text()")
        news_date = news.xpath("//time/text()")
        link = news.xpath("//a[contains(@class, 'card-full-news _parts-news')]/@href")
    for i in range(len(news_list) - 1):
        # У Ленты относительные и абсолютные ссылки. Поэтому, если ссылка относительная, добавляем недостающую часть к url
        if 'https' not in link[i]:
            link[i] = 'https://lenta.ru' + link[i]
        # если дата публикации сегодня, добавляем дату, так как лента не публикует дату сегодняшних новостей
        if ',' not in news_date[i]:
            news_date[i] = news_date[i] + ', ' + str(today.strftime("%d %B %Y"))
        db.news.insert_one({
            'source': 'Lenta.ru',
            'title': title[i],
            'url': link[i],
            'time': news_date[i]
        })
    # return news_dict


def get_news_mail():
    url = 'https://news.mail.ru'
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_list = dom.xpath("//li[contains(@class, 'list__item')]")
    # news_dict = {}
    for news in news_list:
        title = news.xpath("//a/text()")
        news_date = news.xpath("//time/text()")
        link = news.xpath("//a/@href")
    for i in range(len(news_list) - 1):
        if ' ' in title[i]:
            title[i] = title[i].replace(' ', ' ')
        if 'https' not in link[i]:
            link[i] = url + link[i]
        db.news.insert_one({
            'source': 'Mail.ru',
            'title': title[i],
            'url': link[i]
        })
    # return news_dict


def get_news_rambler():
    url = 'https://news.rambler.ru/world/'
    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)
    news_list = dom.xpath("//article[contains(@class, '_2bIZW')]")
    # news_dict = {}
    for news in news_list:
        title = news.xpath("//div[contains(@class, '_1tnKf')]/text()")
        news_date = news.xpath("//time/text()")
        link = news.xpath("//a[contains(@class, '_6bF6i')]/@href")
    for i in range(len(title)):
        if ' ' in title[i]:
            title[i] = title[i].replace(' ', ' ')
        if 'https' not in link[i]:
            link[i] = url + link[i]
        db.news.insert_one({
            'source': 'Rambler.ru',
            'title': title[i],
            'url': link[i]
        })
    # return news_dict


get_news_lenta()
get_news_mail()
get_news_rambler()
for document in db.news.find():
    pprint(document)
print('Данные загружены!')
