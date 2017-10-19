# -*- coding: utf-8 -*-

import scrapy
from opendata.items import OpenDataItems

from datetime import datetime

import re
from urlparse import urljoin

import sys 

from geopy.geocoders import Nominatim

from lxml import etree

# Spider habitaclia
# By: Irene

class QuotesSpider(scrapy.Spider):
        name = 'MAN'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1

        def start_requests(self):
            sf = False
            url= 'https://dadesobertes-situam.opendata.arcgis.com/pages/catleg-de-dades'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="markdown-card ember-view"]//@href').extract() #no agafa els links, why
                    for l in links:
                        index = substring-after(substring-before(l, "/info"), "items/")
                        link_completed =  "https://www.arcgis.com/home/item.html?id=" + index
                        self.links_next.append(link_completed)
                    print len(links)
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

                    '''desc = response.xpath('//*[@id="description"]/div//text()').extract()

                    count  = 0
                    for i in desc:
                        if "Descripción" in i.encode('utf-8'):
                            item['description'] = desc[count+2]
                        if "Temas" in i.encode('utf-8'):
                            categories = desc[count+3]
                            categories = categories.replace("/n", "")
                            categories = categories.replace("/r", "")
                            categories = categories.strip()
                            item['categories'] = categories
                        if "Fuente" in i.encode('utf-8'):
                            publisher = desc[count +2]
                            publisher = publisher.replace("/n", "")
                            publisher = publisher.replace("/r", "")
                            publisher = publisher.strip()
                            item['publisher'] = publisher
                        if "Creado" in i.encode('utf-8'):
                            item['date_creation'] = desc[count +2]
                        if "Actualizado" in i.encode('utf-8'):
                            item["date_actualization"] = desc[count+2]
                        if "Tipo de actualización" in i.encode('utf-8'):
                            item['frequency'] = desc[count+2]
                        if "Licencia" in i.encode('utf-8'):
                            item["licenses"] = desc[count+2]
                        if "Etiquetas" in i.encode('utf-8'):
                            tag = desc[count +3]
                            tag = tag.replace("/n", "")
                            tag = tag.replace("/r", "")
                            tag = tag.strip()
                            item['tag'] = tag
                        count +=1
                    
                    item['title'] = response.xpath('//*[@class="container"]//*[@class="pull-left"]//text()').extract_first(default="not-found")

                    item['formats'] = response.xpath('//*[@class="list-unstyled"]//label//text()').extract()'''
                    
                    item['city'] = "MAN"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    
                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
                    


