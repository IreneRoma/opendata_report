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
        name = 'GAS'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://www.vitoria-gasteiz.org/j34-01w/catalogo/buscadorDocumentos'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="row result-elements"]/article//@href').extract() 

                    for l in links:
                        link_completed = 'http://www.vitoria-gasteiz.org' + l
                        self.links_next.append(link_completed)
                        self.i += 1

                    next_pages = response.xpath('//*[@class="pagination"]//@href').extract()
                    if len(next_pages) == 1:
                        next_page = next_pages[0]
                    else:
                        if len(next_pages) == 2:
                            next_page = None
                        else:
                            next_page = next_pages[len(next_pages)-1]    
                    

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
                    
                    item['title'] = response.xpath('//*[@id="wb021contenido"]/h3/text()').extract_first(default="not-found")

                    item['description'] = response.xpath('//*[@id="wb021contenido"]//p[2]//text()').extract_first(default="not-found")

                    info = response.xpath('//*[@id="wb021contenido"]//ul//li//text()').extract()
                    
                    count = 0
                    for i in info:
                        if "Cobertura temporal" in i.encode('utf-8'):
                            date_creation = i.replace("Cobertura temporal\t:","")
                            item['date_creation'] = date_creation
                        if "Frequencia de" in i.encode('utf-8'):
                            frequency = i.replace("Frecuencia de actualización: ","")
                            item['frequency'] = frequency     
                        if "Fecha de última" in i.encode('utf-8'):
                            date_actualization = i.replace("Fecha de última actualización: ","")
                            item['date_actualization'] = date_actualization 
                        if "Licencia" in i.encode('utf-8'):
                            item['licenses'] = i                       
                        count += 1 
                    
                    item['city'] = "GAS"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="j34-distribuciones"]//span//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@id="wb021contenido"]//*[@class="btn"]//text()').extract()

                    item['url'] = response.url
    

                    yield item


                    if self.k<self.i:
                        next_page = response.urljoin(self.links_next[self.k])
                        self.k+=1
                        yield scrapy.Request(next_page,self.parse,dont_filter=True)
