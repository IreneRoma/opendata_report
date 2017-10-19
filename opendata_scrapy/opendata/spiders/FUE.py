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
        name = 'FUE'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://datosabiertos.fuengirola.es/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                #if self.a is True : 
                #    self.num_pages = int(response.xpath('//*[@class="pagination pagination-centered"]//li[4]//text()').extract_first(default='not-found'))
                #    self.a = False

                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_complteted = 'http://datosabiertos.fuengirola.es' + l
                        self.links_next.append(link_complteted)

                    #next_page = 'http://opendata.caceres.es/dataset?page=' + str(self.j) THIS WEB HAS ONLY ONE PAGE
                    next_page = None
                    if next_page is not None:
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
                    
                    item['description'] = response.xpath('//*[@class="notes embedded-content"]/p/text()').extract()

                    item['city'] = "FUE"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()

                    title = response.xpath('//*[@class="module-content"]/h1/text()').extract()
                    item['title'] = title[0]
                    item['categories'] = title[1]

                    item['licenses'] = response.xpath('//*[@class="module module-narrow module-shallow license"]/p/a/text()').extract_first(default="not-found")

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
