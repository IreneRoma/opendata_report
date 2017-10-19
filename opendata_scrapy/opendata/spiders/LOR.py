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
        name = 'LOR'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1


        def start_requests(self):
            sf = False
            url= 'http://datos.lorca.es/catalogo/busquedat'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="catalogo"]//@href').extract() 

                    for l in links:
                        link_complteted = "http://datos.lorca.es/catalogo/" + l
                        self.links_next.append(link_complteted)

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

                    desc1 = response.xpath('//*[@id="main"]/h2/text()').extract()
                    desc = response.xpath('//*[@class="catalogo"]/li/text()').extract()

                    count  = 0
                    if (len(desc)>0):
                        for i in desc1:
                            if ("Descripción" in i.encode('utf-8') and "de los" not in i.encode('utf-8')):
                                item['description'] = desc[count-1]
                            if "Categoría" in i.encode('utf-8'):
                                item['categories'] = desc[count-1]
                            if "Etiquetas" in i.encode('utf-8'):
                                item['tag'] = desc[count-1]
                            if "Fecha de creación" in i.encode('utf-8'):
                                item['date_creation'] = desc[count-1]
                            if "Fecha última" in i.encode('utf-8'):
                                item["date_actualization"] = desc[count-1]
                            if "Frequencia de actualización" in i.encode('utf-8'):
                                item['frequency'] = desc[count-1]
                            if "Fuente" in i.encode('utf-8'):
                                item["publisher"] = desc[count-1]
                            count +=1
                    
                    item['title'] = response.xpath('//*[@id="main"]//h1//text()').extract_first(default="not-found")

                    item['formats'] = response.xpath('//*[@style="list-style-type:none;"]//@alt').extract()
                    
                    item['city'] = "LOR"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    
                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
                    


