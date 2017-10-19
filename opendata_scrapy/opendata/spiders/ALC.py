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
        name = 'ALC'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        num_pages = 0
        a = True


        def start_requests(self):
            sf = False
            url= 'http://datos.alcobendas.org/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)
        
        def add_actualization(self,response):
            item = response.meta['item']
            item['date_actualization'] = response.xpath('//*[@id="content"]/div[3]/div/section/div/table/tbody/tr[1]/td/text()').extract_first(default='not-found')  
            return item
        
        def add_categories(self,response):
            item = response.meta['item']
            item['categories'] = response.xpath('//*[@class="media-heading"]//text()').extract_first(default='not-found')          
            return item


        def parse(self,response):

                if self.a is True : 
                    self.num_pages = response.xpath('//*[@class="pagination pagination-centered"]//li[5]//text()').extract_first(default='not-found')
                    self.num_pages = int(self.num_pages)
                    self.a = False

                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_complteted = 'http://datos.alcobendas.org' + l
                        self.links_next.append(link_complteted)

                    next_page = 'http://datos.alcobendas.org/dataset?page=' + str(self.j)
                    print next_page
                    if self.j < self.num_pages +1 :
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


                    titles_metadata = response.xpath('//*[@class="table table-striped table-bordered table-condensed"]//tbody//th//text()').extract()
                    desc_metadata = response.xpath('//*[@class="table table-striped table-bordered table-condensed"]//tbody//td//text()').extract()                    
                    
                    count = 0
                    for i in titles_metadata:
                        if "Autor" in i.encode('utf-8'):
                            item['publisher'] = desc_metadata[count+4]
                        if "Fecha de la primera" in i.encode('utf-8'):
                            date_creation = desc_metadata[count+2] 
                            date_creation = date_creation.replace("\n","")
                            date_creation = date_creation.strip()
                            item['date_creation'] = date_creation
                        if "Frecuencia" in i.encode('utf-8'):
                            item['frequency'] = desc_metadata[count+4]                                                   
                        count += 1
                        
                    item['description'] = response.xpath('//*[@class="notes embedded-content"]/p/text()').extract_first(default='not-found')
                    
                    item['licenses'] = response.xpath('//*[@class="module module-narrow module-shallow license"]//*[@class="module-content"]/a/text()').extract_first(default='not-found')  
     
                    item['city'] = "ALC"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@class="tag"]//text()').extract()

                    title = response.xpath('//*[@class="module-content"]//h1[1]/text()').extract_first(default='not-found')
                    title = title.replace("\n","")
                    title = title.replace("\r","")
                    title = title.replace("\t","")
                    title = title.strip() 
                    
                    item['title'] = title

                    item['url'] = response.url
                    
                    url_actualization = 'http://datos.alcobendas.org' + response.xpath('//*[@id="dataset-resources"]/ul/li[1]/div[1]/a[1]/@href').extract_first(default='not-found') 
                    request = scrapy.Request(url_actualization, callback = self.add_actualization)
                    request.meta['item'] = item
                    yield request
                    
                    url_categories = 'http://datos.alcobendas.org' + response.xpath('//*[@class="nav nav-tabs"]/li[2]//@href').extract_first(default='not-found')    
                    request = scrapy.Request(url_categories, callback = self.add_categories, meta={'item': item})    
                    yield request

                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
