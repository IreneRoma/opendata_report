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
        name = 'ALB'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1


        def start_requests(self):
            sf = False
            url= 'http://www.albacete.es/es/webs-municipales/datos-abiertos/catalogo-datos'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="rlist_tit"]//@href').extract() 

                    for l in links:
                        link_complteted = 'https://www.bilbao.eus' + l
                        self.links_next.append(link_complteted)

                    next_page = 'https://www.bilbao.eus/opendata/es/catalogo/temas/formatos/frecuencias/nombre-ascendente?np=' + str(self.j)
                    print next_page
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

                    desc1 = response.xpath('//*[@class="margen_iz4"]//text()').extract()

                    desc2 = response.xpath('//*[@class="fondo_blanco"]//text()').extract()
                    
                    if len(desc1) > 0:
                        
                        item['description'] = desc1[0]
                        item['licence'] = desc1[1]  

                    count = 0    
                    for i in desc2:
                        if "Publicador" in i:
                            item['publisher'] = desc2[count+1]
                        if "Tema" in i:
                            item['topic'] = desc2[count+1].split(",")
                        if "geográfico" in i.encode('utf-8'):
                            item['geography'] = desc2[count+1]
                        if "Idioma" in i.encode('utf-8'):
                            item['lenguage'] =  desc2[count+1].split(",") 
                        if "creación" in i.encode('utf-8'):
                            item['date_creation'] = desc2[count+1]
                        if "Fecha de actualización" in i.encode('utf-8'):
                            item['date_actualization'] = desc2[count+1]
                        if "Frecuencia de actualización" in i.encode('utf-8'):
                            item['frequency'] = desc2[count+1]
                        count += 1
                    
                    item['city'] = "ALB"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="rlist_ul_temario"]//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@class="etiquetas"]//text()').extract()

                    title = response.xpath('//*[@class="blq-col"]//text()').extract()

                    item['title'] = title[1]

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
