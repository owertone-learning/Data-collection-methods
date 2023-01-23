# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from pymongo import MongoClient


class ParserJobPipeline:
    def __init__(self):
        #client = MongoClient('localhost:27017')
        #self.mongo_db = client.parser_job
        pass

    def process_item(self, item, spider):
        vacancy_salary = []
        nums = item['salary']
        vacancy_name = item['name']
        vacancy_url = item['url']
        for i in nums:
            if '\xa0' in i:
                i = i.replace('\xa0', '')
                vacancy_salary.append(i)
        if len(vacancy_salary) > 1:
            vacancy_money_from = vacancy_salary[0]
            vacancy_money_to = vacancy_salary[1]
        else:
            if 'от ' in nums:
                vacancy_money_from = vacancy_salary[0]
                vacancy_money_to = '---'
            if 'до ' in nums:
                vacancy_money_from = '---'
                vacancy_money_to = vacancy_salary[0]
        if 'з/п не указана' in nums:
            vacancy_money_from = '---'
            vacancy_money_to = '---'
        if 'По договорённости' in nums:
            vacancy_money_from = '---'
            vacancy_money_to = '---'
        print('#'*50)
        print(
            f'Вакансия: {vacancy_name}\n'
            f'Зарплата от: {vacancy_money_from}\n'
            f'Зарплата до: {vacancy_money_to}\n'
            f'Ссылка: {vacancy_url}\n'
        )
        print('#'*50)

        #collection = self.mongo_db[spider.name]
        #collection.insert_one({
        #    'Vacany name': vacancy_name,
        #    'Salary from': vacancy_money_from,
        #    'Salary to': vacancy_money_to,
        #    'Vacany URL': vacancy_url
        #})

        

        return item
