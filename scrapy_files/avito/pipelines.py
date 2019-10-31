# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.avito_auto

    def process_item(self, item, spider):
        item['sale'] = int(item['sale'])
        new_param = {}
        for i in range(len(item['param'])):
            if i % 2 == 0:
                key = item['param'][i][:-2]
                value = item['param'][i+1]
                if value[-1] == ' ':
                    value = value[:-1]
                new_param[key] = value
        item['param'] = new_param

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

class AvitoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item



