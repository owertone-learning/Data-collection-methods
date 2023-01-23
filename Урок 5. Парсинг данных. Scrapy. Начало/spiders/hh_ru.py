import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem

class HhRuSpider(scrapy.Spider):
    name = 'hh_ru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?no_magic=true&L_save_area=true&text=python&search_field=name&excluded_text=&area=4&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20']

    def parse(self, response:HtmlResponse):

        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancy_list = response.xpath('//a[@data-qa="serp-item__title"]/@href').getall()
        for link in vacancy_list:
            yield response.follow(link, callback=self.parse_vacancy)
  


    def parse_vacancy(self, response:HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()

        yield ParserJobItem(
            name = vacancy_name,
            url = vacancy_url,
            salary = vacancy_salary
        )
        #print('\n********************************\n%s\n********************************\n'%response.url)