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
        name = 'ZAR'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1
        a = True


        def start_requests(self):
            sf = False
            url= 'https://www.zaragoza.es/sede/portal/datos-abiertos/servicio/catalogo/'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if self.a is True : 
                    pages = response.xpath('//*[@class="btn btn-primary btn-mini"]//text()').extract()
                    if len(pages)>0:
                        self.num_pages = pages[len(pages)-2]
                        self.num_pages = int(self.num_pages)
                        self.a = False
                    else:
                        self.num_pages = 0
                        self.a = False

                if not self.sf:
                    links = response.xpath('//*[@class="card nomargin"]//@href').extract() 

                    for l in links:
                        link_complteted = 'https://www.zaragoza.es/sede/servicio/catalogo/' + l
                        self.links_next.append(link_complteted)

                    next_page = 'https://www.zaragoza.es/sede/servicio/catalogo/?&start=' + str(50*(self.j-1))
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

                    desc_metadata = response.xpath('//*[@class="card"]//text()').extract()                    
                    
                    count = 0
                    for i in desc_metadata:
                        if "Idiomas" in i.encode('utf-8'):
                            item['lenguage'] = desc_metadata[count+3]
                        if "creación" in i.encode('utf-8'):
                            item['date_creation'] = desc_metadata[count+2]
                        if "modificación" in i.encode('utf-8'):
                            item['date_actualization'] = desc_metadata[count+2]                                           
                        if "Periodicidad" in i.encode('utf-8'):
                            item['frequency'] = desc_metadata[count+2]
                        if "Editor" in i.encode('utf-8'):
                            item['publisher'] = desc_metadata[count+2]
                        if "Licencia" in i.encode('utf-8'):
                            licenses = desc_metadata[count+3]
                            licenses = licenses.replace("\n","")
                            item['licenses'] = licenses.strip()
                        if "Lugar" in i.encode('utf-8'):
                            item['geography'] = desc_metadata[count+2]
                        count += 1
                    
                    description = response.xpath('//*[@property="dcat:description"]/p/text()').extract()
                    item['description'] = " ".join(description)

                    item['categories'] = response.xpath('//*[@id="rscont"]/div[1]/a[1]/text()').extract_first(default='not-found')
                                                            
                    item['city'] = "ZAR"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    formats = []
                    formats1 = response.xpath('//*[@id="rscont"]/div[1]/div/div[1]/ul//a/text()').extract()
                    formats2 = response.xpath('//*[@class="badge alert-primary"]//text()').extract() 
                    if not formats1:
                        pass
                    else: 
                        formats.append(formats1)
                    if not formats2:
                        pass
                    else:
                        formats.append(formats2)
                    
                    item['formats'] = formats       
                    
                    title = response.xpath('//*[@property = "dct:title"]//text()').extract_first(default="not-found")
                    item['title'] = title

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
