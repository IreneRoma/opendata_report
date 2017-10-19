# -*- coding: utf-8 -*-

import scrapy
from opendata.items import OpenDataItems

from datetime import datetime

import re
from urlparse import urljoin

import sys 

from geopy.geocoders import Nominatim

# Spider habitaclia
# By: Irene

class QuotesSpider(scrapy.Spider):
        name = 'BAR'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        num_pages = 0
        a = True


        def start_requests(self):
            sf = False
            url= 'http://opendata-ajuntament.barcelona.cat/data/es/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    self.num_pages = response.xpath('//*[@class="pagination pagination-centered"]//li[5]//text()').extract_first(default='not-found')
                    self.num_pages = int(self.num_pages)
                    self.a = False


                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_complteted = "http://opendata-ajuntament.barcelona.cat" + l
                        self.links_next.append(link_complteted)

                    next_page = 'http://opendata-ajuntament.barcelona.cat/data/es/dataset?page=' + str(self.j)
                    print next_page
                    if self.j < (self.num_pages+1):
                        self.j +=1
                        next_page = response.urljoin(next_page)
                        yield scrapy.Request(next_page,self.parse)


                    else:
                        self.sf = True
                        next_page = self.links_next[0]
                        yield scrapy.Request(next_page,self.parse,dont_filter=True)

                if self.sf:

                    reload(sys)
                    sys.setdefaultencoding('utf-8')
                    
                    item = OpenDataItems()

                    cate1 = response.xpath('//*[@class="dataset-groups"]//*[@class="parent"]/a/text()[2]').extract_first(default="not-found")
                    cate2 = response.xpath('//*[@class="dataset-groups"]//*[@class="child"]/a/text()[2]').extract_first(default="not-found")
                    cate1 = cate1.replace("\n", "")
                    cate1 = cate1.strip()
                    cate2 = cate2.replace("\n", "")
                    cate2 = cate2.strip()

                    item['categories'] = cate1 + ", " + cate2

                    desc = response.xpath('//*[@class="additional-info"]//tbody//text()').extract()

                    count  = 0
                    for i in desc:
                        if "Título" in i.encode('utf-8'):
                            item['title'] = desc[count+2]
                        if "Fuente" in i.encode('utf-8'):
                            item['publisher'] = desc[count +2]
                        if "Fecha publicación" in i.encode('utf-8'):
                            item['date_creation'] = desc[count +2]
                        if "Frecuencia de" in i.encode('utf-8'):
                            item['frequency'] = desc[count+2]
                        count +=1
                    
                    item['licenses'] = response.xpath('//*[@rel="dc:rights"]//text()').extract_first(default='not-found')

                    item['tag'] = response.xpath('//*[@class="tag-list"]//li/a/text()').extract()

                    item['description'] = response.xpath('//*[@class="notes embedded-content"]/p/text()').extract_first(default='not-found')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()
                    
                    item['city'] = "BAR"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
