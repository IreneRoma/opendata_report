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
        name = 'PAL'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://datosabiertos.laspalmasgc.es/data/'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    self.num_pages = int(int(response.xpath('//*[@class="left"]/strong/text()').extract_first())/10)+1
                    self.a = False
                    #print self.num_pages

                if not self.sf:
                    links = response.xpath('//*[@class="datasetTitle"]//@href').extract() 

                    for l in links:
                        self.links_next.append(l)

                    numeration = (self.j -1)*10
                    #print numeration
                    next_page = 'http://datosabiertos.laspalmasgc.es/data/?offset=' + str(numeration) + '&limit=10'
                    if self.j < self.num_pages +1 :
                        print next_page
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
                    
                    desc_metadata = response.xpath('//*[@class="expand-body"]//text()').extract()                    
                    
                    count = 0
                    for i in desc_metadata:
                        if "Condiciones de uso" in i.encode('utf-8'):
                            item['licenses'] = desc_metadata[count+2]
                        if "Publicador" in i.encode('utf-8'):
                            item['publisher'] = desc_metadata[count+1]                                           
                        if "Frecuencia" in i.encode('utf-8'):
                            freq = desc_metadata[count+1]
                            freq = freq.replace("\n","")
                            item['frequency'] = freq.strip()
                        if "Fecha de creación" in i.encode('utf-8'):
                            item['date_creation'] = desc_metadata[count+1]
                        if "Última actualización" in i.encode('utf-8'):
                            item['date_actualization'] = desc_metadata[count+1]
                        count += 1

                    item['description'] = response.xpath('//*[@id="content"]/section/div/div/div[2]/div[1]/p//text()').extract_first(default="not-found")
                                                        
                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['categories'] = response.xpath('//*[@id="content"]/aside/div[4]//li//text()').extract()

                    item['formats'] = response.xpath('//*[@id="content"]/aside/div[3]//li//text()').extract()              
                    
                    item['tag'] = response.xpath('//*[@id="content"]/aside/div[2]//li//text()').extract()

                    item['title'] = response.xpath('//*[@class="group"]//h2/text()').extract_first(default="not-found")

                    item['city'] = "PAL"

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
