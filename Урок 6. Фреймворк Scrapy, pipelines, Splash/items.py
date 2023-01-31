# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose

def process_name(value):
    name = ''
    name = value[0].replace('\n', '').replace("        ", "").replace('    ','')
    return name

def process_currency(value):
    currency = ''
    currency = value[0].replace(' ', '').replace('.', '')
    return currency

def process_price(value):
    money = ''
    money = value[0].replace('<span>', '').replace("</span>", "").replace(' ', '')
    if '<sup></sup>' in money:
        money = float(money.replace('<sup></sup>', ''))
    else:
        money = float(money.replace('<sup>', '.').replace("</sup>", "").replace(' ', ''))
    return money

class KsParserItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    price_currency = scrapy.Field(input_processor=Compose(process_currency), output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
