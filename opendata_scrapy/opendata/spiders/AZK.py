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
        name = 'AZK'
        links_next = []

        sf = False
        i = 0
        j = 1
        k = 1
        num_pages = 0
        a = True


        def start_requests(self):
            sf = False
            url= 'http://opendataazkoitia.gobernuirekia.eus/es/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    self.num_pages = response.xpath('///*[@class="pager-item"]//text()').extract_first(default='not-found')
                    self.num_pages = int(self.num_pages)
                    self.a = False

                if not self.sf:
                    links = response.xpath('//*[@property="dc:title"]//@href').extract() 

                    for l in links:
                        link_complteted = 'http://opendataazkoitia.gobernuirekia.eus' + l
                        self.links_next.append(link_complteted)

                    next_page = 'http://opendataazkoitia.gobernuirekia.eus/es/dataset?page=' + str(self.j)
                    print next_page
                    if self.j < self.num_pages :
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

                    desc2 = response.xpath('//*[contains(@id,"node-dataset")]//section//tr//text()').extract()
                    
                    print len(desc2)
                    count = 0  
                    
                    for i in desc2:
                        if "Autor" in i:
                            item['publisher'] = desc2[count+1]
                        if "Publicado" in i:
                            item['categories'] = desc2[count+1].split(",")
                        if "Localización" in i.encode('utf-8'):
                            item['geography'] = desc2[count+1]
                        if "Fecha modificación" in i.encode('utf-8'):
                            item['date_actualization'] = desc2[count+1]
                        if "Fecha publicación" in i.encode('utf-8'):
                            item['date_creation'] = desc2[count+1]
                        if "Licencia" in i.encode('utf-8'):
                            item['licenses'] = desc2[count+1]
                        count += 1
                    
                    item['city'] = "AZK"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@class="field field-name-field-tags field-type-taxonomy-term-reference field-label-hidden"]//*[@class="field-item even"]/a//text()').extract()

                    item['title'] = response.xpath('//*[@class="active-trail"]//text()').extract()
                        
                    item['url'] = response.url

                    yield item

                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
