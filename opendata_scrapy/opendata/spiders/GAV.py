# -*- coding: utf-8 -*-

import scrapy
from opendata.items import OpenDataItems

from datetime import datetime

import re
from urlparse import urljoin

import sys 

from geopy.geocoders import Nominatim

import json

# Spider habitaclia
# By: Irene

class QuotesSpider(scrapy.Spider):
        name = 'GAV'
        links_next = []

        sf = False
        i = 0
        j = 2
        k = 1


        def start_requests(self):
            sf = False
            url= 'https://gavaobert.gavaciutat.cat/ca/browse'
            yield scrapy.Request(url,self.parse,dont_filter=True)          

        def parse(self,response):

                if not self.sf:
                    links = response.xpath('//*[@class="browse2-results"]//@data-view-id').extract() 
                    print len(links)

                    for l in links:
                        link_completed = "https://gavaobert.gavaciutat.cat/api/views/" + l + ".json"
                        self.links_next.append(link_completed)

                    next_page = response.xpath('//*[@class="next nextLink browse2-pagination-button"]//@href').extract_first()
                    
                    #next_page = None
                    print next_page
                    if next_page is not None:
                        #next_page = response.urljoin(next_page)
                        next_page = 'https://gavaobert.gavaciutat.cat/ca' + next_page
                        yield scrapy.Request(next_page,self.parse)

                    else:
                        self.sf = True
                        print len(self.links_next)
                        next_page = self.links_next[0]
                        yield scrapy.Request(next_page,self.parse,dont_filter=True)
                    
                if self.sf:
                    
                    reload(sys)
                    sys.setdefaultencoding('utf-8')
            
                    item = OpenDataItems() 
                    json_data = json.loads(response.body_as_unicode())

                    item['description'] = json_data['description'] if 'description' in json_data else None

                    item['categories'] = json_data['category'] if 'category' in json_data else None

                    item['city'] = 'GAV'

                    #item['formats'] = scrapy.Field()

                    item['frequency'] = json_data['metadata']["custom_fields"]["Dataset Information"]['Update Frequency']

                    #item['geography'] = scrapy.Field()

                    #item['lenguage'] = scrapy.Field()

                    updatedat = json_data['rowsUpdatedAt']
                    updatedat = '{:<010d}'.format( updatedat )
                    updatedat = datetime.fromtimestamp( int(updatedat)  )
                    item['date_actualization'] = datetime.strftime(updatedat, '%Y/%m/%d_%H:%M:%S')

                    publicatedat = json_data['publicationDate']
                    publicatedat = '{:<010d}'.format( publicatedat )
                    publicatedat = datetime.fromtimestamp( int(publicatedat) )
                    item['date_creation'] = datetime.strftime(publicatedat, '%Y/%m/%d_%H:%M:%S')

                    item['licenses'] = json_data['license']['name'] if 'license' in json_data else None

                    item['publisher'] = json_data['tableAuthor']['displayName'] if 'tableAuthor' in json_data else None

                    item['tag'] = json_data['tags'] if 'tags' in json_data else None

                    item['title'] = json_data['name'] if 'name' in json_data else None

                    item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

                    item['url'] = response.url

                    yield item

                    if self.k < len(self.links_next):
                        next_item = self.links_next[self.k]
                        self.k+=1
                        yield scrapy.Request(next_item,self.parse,dont_filter=True)
