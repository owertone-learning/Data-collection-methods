# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline, ImageException
from itemadapter import ItemAdapter
from pymongo import MongoClient

class KsParserPipeline:

# создаем базу данных и записываем в отдельную коллецию по поисковому запросу, чтобы для каждого запроса была своя коллекция
# из поискового запроса удалем "+" просто для более понятных записей в базе

    def process_item(self, item, spider):
        print(f'KsParserPipeline: {item}')
        client = MongoClient('mongodb://localhost:27017/')
        db = client.castorama_db
        item_name = spider.search.replace('+', ' ')
        db[item_name].insert_one({
            'item': item
        })
        return item

class KsPhotosPipeline(ImagesPipeline):

# загружаем фотографии

    def get_media_requests(self, item, info):
        if item.get('photos'):
            for img in item.get('photos'):
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
            print(f'item new way: {item}')
        return item
