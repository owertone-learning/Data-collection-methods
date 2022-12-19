import datetime
import json
import locale

import requests
from lxml import html
from pprint import pprint
url = 'https://news.mail.ru'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
today = datetime.datetime.now()
news_date = today.strftime("%d %B %Y")

def get_news():
    response = requests.get(url, headers=headers)
    print(response.status_code)
    #print(response.json())
    dom = html.fromstring(response.text)
    news_list = dom.xpath("//li[contains(@class, 'list__item')]")
    news_dict = {}
    news_dict['News'] = []
    #print(articles)
    print(news_list)
    for news in news_list:
        title = news.xpath("//a/text()")
        #print(title)
        #source = news.xpath("//span/text()")
        #print(source)
        news_date = news.xpath("//time/text()")
        #print(news_date)
        link = news.xpath("//a/@href")
    for i in range(len(news_list) - 1):
        if ' ' in title[i]:
            title[i] = title[i].replace(' ', ' ')
        if 'https' not in link[i]:
            link[i] = url + link[i]
        news_dict['News'].append({
            'title': title[i],
            'url': link[i],
            #'time': news_date[i]
        })
        print(news_dict)
    return news_dict


with open('mail_news.json', 'w', encoding='utf-8') as f:
    json.dump(get_news(), f, ensure_ascii=False, indent=2)
print('Данные загружены!')
