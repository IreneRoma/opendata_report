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
        name = 'MAD'
        links_next = []
        formats_final = []

        sf = False
        i = 0
        j = 2
        k = 1
        num_pages = 0
        a = True


        def start_requests(self):
            sf = False
            url= 'http://datos.madrid.es/portal/site/egob/menuitem.9e1e2f6404558187cf35cf3584f1a5a0/?vgnextoid=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextchannel=374512b9ace9f310VgnVCM100000171f5a0aRCRD&vgnextfmt=default'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="event-info"]/a/@href').extract() 

                    for l in links:
                        link_complteted = "http://datos.madrid.es" + l
                        self.links_next.append(link_complteted)

                    nextnext = response.xpath('//*[@class="next"]/a/@href').extract_first()
                    next_page = "http://datos.madrid.es" + str(nextnext)
                    print ("hola \n")
                    print nextnext
                    print next_page
                    if nextnext is not None:
                        print ("mare meva \n")
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

                    item['title'] = response.xpath('//*[@class="summary-title"]//text()').extract_first(default="not-found")

                    item['description'] = response.xpath('//*[@class="tiny-text"]/p/text()').extract_first(default="not-found")
                    
                    item['categories'] = response.xpath('//*[@class="collapse"]//div//a//text()').extract_first(default="not-found")
                    
                    desc1 = response.xpath('//*[@id="two"]//*[@class="content-box"]//h5//text()').extract()
                    desc = response.xpath('//*[@id="two"]//div//p//text()').extract()
                    
                    count = 0
                    for i in desc1:
                        if "Fecha de creación" in i.encode('utf-8'):
                            item['date_creation'] = desc[count]
                        if "Actualización" in i.encode('utf-8'):
                            item['date_actualization'] = desc[count]
                        if "Frecuencia" in i.encode('utf-8'):
                            item['frequency'] = desc[count]
                        if "Editor" in i.encode('utf-8'):
                            item['publisher'] = desc[count]
                        if "Lugar" in i.encode('utf-8'):
                            geo = desc[count]
                            geo = geo.replace("\n","")                       
                            geo = geo.replace("\r","")     
                            geo = geo.replace("\t","")     
                            item['geography'] = geo
                        if "Licencia" in i.encode('utf-8'):
                            lic = desc[count]
                            lic = lic.replace("\n","")
                            lic = lic.replace("\r","")
                            lic = lic.replace("\t","")
                            item['licenses'] = lic
                        count += 1

                    formats_final = []
                    formats = response.xpath('//*[@class="info-file"]//text()').extract()
                    for i in formats:
                        j = i.split(",")[0]
                        self.formats_final.append(j)
                    item['formats'] = self.formats_final
                    
                    item['city'] = "MAD"

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url
    

                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
