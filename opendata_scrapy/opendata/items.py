# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class OpenDataItems(scrapy.Item):

    categories = scrapy.Field()

    city = scrapy.Field()

    date_actualization = scrapy.Field()

    date_creation = scrapy.Field()

    date_extraction = scrapy.Field()

    description = scrapy.Field()

    formats = scrapy.Field()

    frequency = scrapy.Field()

    geography = scrapy.Field()

    lenguage = scrapy.Field()

    licenses = scrapy.Field()

    publisher = scrapy.Field()

    tag = scrapy.Field()

    title = scrapy.Field()

    url = scrapy.Field()
    
    pass
