# -*- coding: utf-8 -*-

import scrapy
from opendata.items import OpenDataItems

from datetime import datetime

import re
from urlparse import urljoin

import sys 

from geopy.geocoders import Nominatim

from lxml import etree

import json

# Spider habitaclia
# By: Irene

class QuotesSpider(scrapy.Spider):
        name = 'MAN'
        links_next = []
        json_links = []

        sf = False
        i = 0
        j = 2
        k = 1

        def start_requests(self):

            sf = False
            url = 'https://www.arcgis.com/sharing/rest/content/items/956839604945422a8ffdb4c629b5d976/data?&f=json.json'
            yield scrapy.Request(url,self.parse,dont_filter=True)


        def parse(self,response):
                if not self.sf:
                    jsonresponse = json.loads(response.body_as_unicode())
                    htmlresponse = etree.fromstring(jsonresponse['values']['layout']['sections'][1]['rows'][0]['cards'][0]['component']['settings']['markdown'], etree.HTMLParser())
                    #print etree.tostring(htmlresponse, pretty_print=True)
                    links = htmlresponse.xpath('//*[@class="markdown-card ember-view"]//@href')
                    for l in links:
                        if "https://" in l.encode('utf-8'):
                            pass
                        else:
                            link_completed =  "https://dadesobertes-situam.opendata.arcgis.com" + l
                            l = l.replace("/datasets/","")
                            json_completed = "https://opendata.arcgis.com/api/v2/datasets?filter%5Bslug%5D=SITUAM%3A%3A"+l
                            self.json_links.append(json_completed)
                            print self.json_links
                            self.links_next.append(link_completed)
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

                    print self.json_links[self.k-1]
                    metadata = json.loads(self.json_links[self.k-1].body_as_unicode())

                    item['description'] = metadata['data'][0]['attirbutes']['description']
                    item['title'] = metadata['data'][0]['attirbutes']['title']
                    item['url'] = metadata['data'][0]['attirbutes']['url']
                    item['categories'] = metadata['data'][0]['attirbutes']['tags']
                    item['date_actualization'] = metadata['data'][0]['attirbutes']['updatedAt']
                    item['date_created'] = metadata['data'][0]['attirbutes']['createdAt']
                    item['licenses'] = metadata['data'][0]['attirbutes']['licenseInfo']  
                    item['publisher'] = metadata['data'][0]['attirbutes']['description']               
                    item['city'] = "MAN"
                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

    
                    yield item


                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
                    


