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
        name = 'GIJ'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1


        def start_requests(self):
            sf = False
            url= 'http://transparencia.gijon.es/page/1808-catalogo-de-datose'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="_titulo"]//@href').extract() 

                    for l in links:
                        link_completed = "http://transparencia.gijon.es" + l 
                        self.links_next.append(link_completed)

                    next_page = response.xpath('//*[@class="next_page"]//@href').extract_first()
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
                    
                    description = response.xpath('//*[@class="descripcion"]/text()').extract()
                    if len(description)>0:
                        item['description'] = description[1]
                    
                    dates = response.xpath('//*[@class="sector"]/span[2]/text()').extract()
                    if len(dates)>0:
                        item['date_actualization'] = dates[1]
                        item['date_creation'] = dates[0]

                    item['categories'] = response.xpath('//*[@class="sector"]/a/text()').extract()
                    
                    info = response.xpath('//*[@class="actualizacion"]/a/text()').extract()
                    
                    if len(info)>0:
                        item['publisher'] = info[1]
                        item['geography'] = info[2]
                        item['licenses'] = info[3]                     
                    
                    frequency = response.xpath('//*[@class="fecha"]//strong/text()').extract_first(default='not-found')
                    frequency = frequency.replace("/n","")
                    frequency = frequency.replace("/r","")  
                    frequency = frequency.strip()                                         
                    item['frequency'] = frequency
                                    
                    title = response.xpath('//*[@class="item-detail risp_dataset"]//h2/text()').extract_first(default="not-found")
                    title = title.replace("/n","")
                    title = title.replace("/r","")  
                    title = title.strip()                                         
                    item['title'] = title

                    item['formats'] = response.xpath('//*[@class="dataset-formats"]//@alt').extract()
                    
                    item['city'] = "GIJ"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    
                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
                    


