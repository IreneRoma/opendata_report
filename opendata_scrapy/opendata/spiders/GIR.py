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
        name = 'GIR'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1


        def start_requests(self):
            sf = False
            url= 'http://www.girona.cat/opendata/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_completed = "http://www.girona.cat" + l 
                        self.links_next.append(link_completed)

                    page = response.xpath('//*[@class="pagination pagination-centered"]//a/text()').extract()
                    hrefpage = response.xpath('//*[@class="pagination pagination-centered"]//@href').extract()
                    if "»" in page[len(page)-1].encode('utf-8'):
                        next_page = hrefpage[len(hrefpage)-1]
                    else:
                        next_page = None
                    if next_page is not None:
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
                                 
                    description = response.xpath('//*[@class="notes embedded-content"]/p/text()').extract()

                    item['description'] = " ".join(description)

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()

                    title = response.xpath('//*[@class="module-content dataset"]/h1/text()').extract_first(default="not-found")
                    title = title.replace("\n","")
                    item['title'] = title.strip()

                    categories = response.xpath('//*[@class="nav-item"]/a/text()').extract_first(default="not-found")
                    categories = categories.replace("\n", "")
                    item['categories'] = categories.strip()

                    item['licenses'] = response.xpath('//*[@class="module module-narrow module-shallow license"]/p/a/text()').extract_first(default="not-found")

                    item['tag'] = response.xpath('//*[@class="tag-list well"]/li/a/text()').extract()

                    item['publisher'] = response.xpath('//*[@property="dc:creator"]//text()').extract_first(default="not-found")
           
                    item['city'] = "GIR"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    
                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
                    


