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
        name = 'SAB'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'http://opendata.sabadell.cat/ca/inici/fitxes-cataleg'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):


                if not self.sf:
                    links = response.xpath('//*[@class="content clearfix"]/span//@href').extract() 

                    for l in links:
                        link_complteted = 'http://opendata.sabadell.cat/ca' + l
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

                    rep1 = 0
                    rep2 = 0
                    rep3 = 0

                    reload(sys)
                    sys.setdefaultencoding('utf-8')
                    
                    item = OpenDataItems()

                    desc_metadata = response.xpath('//*[@valign="top"]//text()').extract()                    
                    
                    count = 0
                    for i in desc_metadata:
                        if "Tema" in i.encode('utf-8'):
                            item['categories'] = desc_metadata[count+1]
                        if "Font" in i.encode('utf-8'):
                            item['publisher'] = desc_metadata[count+2]
                        if "Etiquetes" in i.encode('utf-8'):
                            item['tag'] = desc_metadata[count+1]                                           
                        if "Llicència" in i.encode('utf-8'):
                            item['licenses'] = desc_metadata[count+2]
                        if rep1 == 0:
                            if "Data creació" in i.encode('utf-8'):
                                item['date_creation'] = desc_metadata[count+1]
                                rep1 = 1
                        if rep2 ==0:
                            if "Data publicació" in i.encode('utf-8'):
                                item['date_actualization'] = desc_metadata[count+1]
                                rep2 = 1
                        if rep3 == 0:
                            if "Freq" in i.encode('utf-8'):
                                item['frequency'] = desc_metadata[count+1]
                                rep3 = 1
                        count += 1
                                                   
                    item['city'] = "SAB"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['formats'] = response.xpath('//*[@style="padding-left: 15px;valign="]//img/@src').extract()              
                    
                    title = response.xpath('//*[@class="title"]//text()').extract_first(default="not-found")
                    title =title.replace("\n", "")
                    item['title'] = title.strip()

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
