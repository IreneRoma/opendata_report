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
        name = 'EIB'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://eibar.gipuzkoairekia.eus/es/datu-irekien-katalogoa'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@id="catalogo"]//@href').extract() 

                    for l in links:
                        self.links_next.append(l)
                        self.i += 1

                    next_page = response.xpath('//*[@class="pager lfr-pagination-buttons"]/li[3]/a//@href').extract_first()
                    if next_page == "javascript:;":
                        next_page= None
                    else:
                        pass
                    #next_page = None
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
                    
                    item['description'] = response.xpath('//*[@class="span9 contenido detalle"]/p//text()').extract_first(default="not-found")

                    info = response.xpath('//*[@id="datos"]//text()').extract()
                    
                    count = 0
                    for i in info:
                        if "Fecha actualización" in i.encode('utf-8'):
                            item['date_actualization'] = info[count+2]
                        if "Tema" in i.encode('utf-8'):
                            item['categories'] = info[count+2]
                        if "Tipo de Licencia" in i.encode('utf-8'):
                            item['licenses'] = info[count+2]
                        if "Autor" in i.encode('utf-8'):
                            item['publisher'] = info[count+2]                            
                        count += 1 
                    
                    info2 = response.xpath('//*[@class="caja"]//*[@class="info"]//text()').extract()

                    count = 0
                    for i in info2:
                        if "Fecha de creación" in i.encode('utf-8'):
                            item['date_creation'] = info2[count+2]
                        if "Frecuencia" in i.encode('utf-8'):
                            item['frequency'] = info2[count+2]                      
                        count += 1 
                    
                    item['city'] = "EIB"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="tipo"]//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@id="etiquetas"]/ul/li//text()').extract()

                    item['title'] = response.xpath('//*[@class="taglib-header"]//*[@class="header-title"]//text()').extract_first(default="not-found")

                    item['url'] = response.url
    

                    yield item


                    if self.k<self.i:
                        next_page = response.urljoin(self.links_next[self.k])
                        self.k+=1
                        yield scrapy.Request(next_page,self.parse,dont_filter=True)
