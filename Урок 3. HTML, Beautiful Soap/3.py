import json
import re

import requests
from bs4 import BeautifulSoup as bs

url = 'https://hh.ru/search/vacancy?text=python&from=suggest_post&area=1'
url_start = 'https://hh.ru/search/vacancy?text=python&salary=&area=1&ored_clusters=true&enable_snippets=true'
url_end = 'hhtmFrom=vacancy_search_list'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}
response = requests.get(url=url, headers=headers)
vacancy_full = []
v = 0


def get_vacancy():
    v_dict = {}
    vacancy_list = {}
    response = requests.get(url=full_url, headers=headers)
    dom = bs(response.text, 'html.parser')
    vac_div_list = dom.find_all('div', {'class': 'serp-item'})
    for vac_div in vac_div_list:
        if vac_div.find('span', {'class': 'bloko-header-section-3'}):
            vacancy_money = vac_div.find('span', {'class': 'bloko-header-section-3'}).text
        else:
            vacancy_money = str('-')
        if ' ' in vacancy_money:
            vacancy_money = vacancy_money.replace(' ', '')
        if 'руб' in vacancy_money:
            vacancy_money_currency = 'руб'
        elif 'USD' in vacancy_money:
            vacancy_money_currency = 'USD'
        elif 'EUR' in vacancy_money:
            vacancy_money_currency = 'EUR'
        else:
            vacancy_money_currency = '-'
        nums = re.findall(r'\d+', vacancy_money)
        if 'от' in vacancy_money:
            vacancy_money_from = int(nums[0])
            vacancy_money_to = '-'
        elif 'до' in vacancy_money:
            vacancy_money_from = '-'
            vacancy_money_to = int(nums[0])
        elif 'от' in vacancy_money and 'до' in vacancy_money:
            vacancy_money_from = int(nums[0])
            vacancy_money_to = int(nums[1])
        else:
            if len(nums) > 1:
                vacancy_money_from = int(nums[0])
                vacancy_money_to = int(nums[1])
            elif len(nums) > 0 & len(nums) < 1:
                vacancy_money_from = int(nums[0])
                vacancy_money_to = '-'
            else:
                vacancy_money_from = '-'
                vacancy_money_to = '-'
        if ' ' in vac_div.find('a', {'class': 'bloko-link_kind-tertiary'}).text:
            vacancy_company = vac_div.find('a', {'class': 'bloko-link_kind-tertiary'}).text.replace(' ', ' ')
        else:
            vacancy_company = vac_div.find('a', {'class': 'bloko-link_kind-tertiary'}).text
        if ' ' in vac_div.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text:
            vacancy_location = vac_div.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.replace(' ', ' ')
        else:
            vacancy_location = vac_div.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text

        vacancy_url = vac_div.find('a').get('href')
        vacancy_url = vacancy_url.split("?")[0]

        v_dict = {
            'vacancy name': vac_div.find('a').text,
            # 'vacancy money': vacancy_money,
            'vacancy_money_from': vacancy_money_from,
            'vacancy_money_to': vacancy_money_to,
            'vacancy money currency': vacancy_money_currency,
            'vacancy company': vacancy_company,
            'vacancy location': vacancy_location,
            'vacancy url': vacancy_url
        }
        vacancy_list = v_dict.copy()
        vacancy_list.update(vacancy_list)
        vacancy_full.append(vacancy_list)
    return vacancy_full


while True:
    page_number = 'page=' + str(v)
    full_url = '{}&{}&{}'.format(url_start, page_number, url_end)
    response = requests.get(url=full_url, headers=headers)
    if response.status_code == 200:
        get_vacancy()
    else:
        print('End of the pages!')
        break
    v += 1

with open('vacancy_hh.json', 'a', encoding='utf-8') as f:
    json.dump(vacancy_full, f, ensure_ascii=False, indent=2)
print('Data loaded!')
