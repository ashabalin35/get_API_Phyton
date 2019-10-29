# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    vacancy_from = scrapy.Field()
    vacancy = scrapy.Field()
    salary = scrapy.Field()
    company = scrapy.Field()
    link = scrapy.Field()
    pass
