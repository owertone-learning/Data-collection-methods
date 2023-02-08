from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from ks_parser.spiders.castoramaru import CastoramaruSpider

# Запуск паука и вывод поля для ввода поискового запроса по которому будут парситься данные
# 15 Поисковый запрос обрабатывается в соответствии принятыми на сайте правилами
# 16 Передаем обработанный запрос в скрипт паука castoramaru.py
if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    search = input('Введите поисковый запрос: ').lower().replace(' ', '+')
    runner.crawl(CastoramaruSpider, search=search)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()