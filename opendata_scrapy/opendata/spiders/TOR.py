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
        name = 'TOR'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://datosabiertos.torrent.es/es/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    pages = response.xpath('//*[@class="pagination pagination-centered"]//a//text()').extract()
                    if len(pages)>0:
                        self.num_pages = pages[len(pages)-2]
                        self.num_pages = int(self.num_pages)
                        self.a = False
                    else:
                        self.num_pages = 0
                        self.a = False

                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_complteted = 'http://datosabiertos.torrent.es' + l
                        self.links_next.append(link_complteted)

                    next_page = 'http://datosabiertos.torrent.es/dataset?page=' + str(self.j)
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
                        if "Etiquetas" in i.encode('utf-8'):
                            item['tag'] = desc_metadata[count].split(",")
                        if "Creado" in i.encode('utf-8'):
                            item['date_creation'] = desc_metadata[count]                                                   
                        count += 1
                    
                    item['description'] = response.xpath('//*[@class="notes embedded-content"]/p/text()').extract_first(default="not-found")
                    
                                                            
                    item['city'] = "TOR"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()
                    
                    item['licenses'] = response.xpath('//*[@class="module module-narrow module-shallow license"]/p[1]/a/text()').extract_first(default="not-found")

                    cate =  response.xpath('//*[@class="module module-narrow module-shallow context-info"]//*[@class="heading"]//text()').extract_first(default="not-found")
                    cate = cate.replace("\n","")
                    cate = cate.replace("\t","")
                    cate = cate.strip()
                    item['categories'] = cate                    
                    
                    title = response.xpath('//*[@class="module-content"]/h1/text()').extract_first(default="not-found")
                    title = title.replace("\n","")
                    title = title.replace("\t","")
                    title = title.strip()
                    item['title'] = title

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
