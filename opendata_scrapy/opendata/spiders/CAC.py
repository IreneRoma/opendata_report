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
        name = 'CAC'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://opendata.caceres.es/dataset'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    self.num_pages = int(response.xpath('//*[@class="pagination pagination-centered"]//li[4]//text()').extract_first(default='not-found'))
                    self.a = False

                if not self.sf:
                    links = response.xpath('//*[@class="dataset-heading"]//@href').extract() 

                    for l in links:
                        link_complteted = 'http://opendata.caceres.es' + l
                        self.links_next.append(link_complteted)

                    next_page = 'http://opendata.caceres.es/dataset?page=' + str(self.j)
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
                    
                    desc1 = response.xpath('//*[@class="notes embedded-content"]//node()[following-sibling::h2[not(preceding-sibling::h2)]]//text()').extract()

                    item['description'] = ''.join(desc1)
                            
                    item['publisher'] = response.xpath('//*[@class="additional-info"]//tr[1]//a//text()').extract_first(default="not-found")
                    
                    date_actualization = response.xpath('//*[@class="additional-info"]//tr[3]//span//text()').extract_first(default="not-found")
                    date_actualization = date_actualization.replace("\n", "")
                    date_actualization = date_actualization.strip()
                    item['date_actualization'] = date_actualization

                    date_creation = response.xpath('//*[@class="additional-info"]//tr[4]//span//text()').extract_first(default="not-found")
                    date_creation = date_creation.replace("\n", "")
                    date_creation = date_creation.strip()
                    item['date_creation'] = date_creation
                    
                    item['frequency'] = response.xpath('//*[@class="additional-info"]//tr[5]//td//text()').extract_first(default="not-found")
                    
                    item['city'] = "CAC"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@class="format-label"]//text()').extract()
                    
                    item['tag'] = response.xpath('//*[@class="tag"]//text()').extract()

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
