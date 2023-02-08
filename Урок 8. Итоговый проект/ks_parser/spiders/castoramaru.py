import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from ks_parser.items import KsParserItem

# получение данных
class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

# создание стартовой страницы парстинга в зависимости от поискового запроса
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={kwargs.get("search")}']

# переход по страницам и получение ссылки на каждый товар

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="next i-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']/@href")
        for link in links:
            yield response.follow(link, callback=self.parse_kst)

# получение данных со страницы товара

    def parse_kst(self, response: HtmlResponse):
        base_url = 'castorama.ru'
        photo_relative_url = response.xpath("//div[@class='js-zoom-container']/img/@data-src").getall()
        photos = []
        print()
        for photo in photo_relative_url:
            absolute_url = response.urljoin(photo)
            photos.append(absolute_url)
        loader = ItemLoader(item=KsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span")
        loader.add_xpath('price_currency', "//span[@class='currency']/text()")
        loader.add_value('photos', photos)
        loader.add_xpath('sku', "//span[@itemprop='sku']/text()")
        loader.add_value('url', response.url)

        yield loader.load_item()