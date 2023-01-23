import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class SjRuSpider(scrapy.Spider):
    name = 'sj_ru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://kazan.superjob.ru/vacancy/search/?keywords=python&period=7']

    def parse(self, response):
        vacancy_list = response.xpath("//a[contains(@class, 'YrERR _2_Rn8 HyxLN')]/@href").getall()
        for link in vacancy_list:
            yield response.follow(link, callback=self.parse_vacancy)


    def parse_vacancy(self, response:HtmlResponse):
        vacancy_name = response.css('h1::text').get()
        vacancy_url = response.url
        vacancy_salary = response.xpath('//span[@class="_2eYAG _3xCPT rygxv _3GtUQ"]//text()').getall()

        yield ParserJobItem(
            name = vacancy_name,
            url = vacancy_url,
            salary = vacancy_salary
        )