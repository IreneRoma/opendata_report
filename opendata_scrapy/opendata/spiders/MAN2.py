# -*- coding: utf-8 -*-
import scrapy
import zlib
from opendata.items import OpenDataItems
from datetime import datetime
import re
from urlparse import urljoin
import sys 
from geopy.geocoders import Nominatim
from lxml import etree
import json
from unicodedata import normalize
import time
class QuoteSpider(scrapy.Spider):
	'''
	Es un diccionari on la clau es un hash (crc32)
	de la url de la foto dels formats (perque la
	url era molt enorme) i el valor es una list amb els 
	formats que significa
	'''
	format_url_hash_to_format_name = {
		-517885671 : ["csv", "json"],
		-1231666856 : ["csv", "kml", "shp", "json"],
		-506161355 : ["csv", "kml", "shp", "json"],
		-1320056335 : ["csv", "kml", "shp", "json"],

	}
	name = 'MAN'
	#Attributes
	dataset_list = []
	def start_requests(self):
		url = ('https://opendata.arcgis.com/api/v2/datasets?filter%5Bcatalogs%5D=dadesobertes-situam.opendata.arcgis.com'
				'&include=organizations%2Cgroups&page%5Bnumber%5D=1&page%5Bsize%5D=1000')
		yield scrapy.Request(url, self.parse_datasets, dont_filter=True)

	def parse_datasets(self, response):
		jsonresponse = json.loads(response.body_as_unicode())
		item = OpenDataItems()
		for dataset in jsonresponse['data']:
			normalized_descr = normalize("NFKD", dataset['attributes']['description'])
			try:
				item['description'] = re.search(r'(.*)-[ ]{0,3}Font', normalized_descr).group(1).strip()
			except Exception, e:
				item['description'] = normalized_descr

			item['title'] = dataset['attributes']['title']
			item['url'] = dataset['attributes']['landingPage']
			item['categories'] = dataset['attributes']['tags']
			item['date_actualization'] = dataset['attributes']['updatedAt']
			item['date_creation'] = dataset['attributes']['createdAt']
			item['licenses'] = dataset['attributes']['structuredLicense'].get('url', None)
			item['publisher'] = dataset['attributes']['owner']
			item['city'] = "MAN"
			item['date_extraction'] = datetime.strftime(datetime.now(), '%Y/%m/%d_%H:%M:%S')

			try:
				item['frequency'] = re.search(ur'ó: (.*) -[ ]{0,1}Formats', dataset['attributes']['description'].replace(u'\xa0', u' ')).group(1)
			except Exception, e:
				item['frequency'] = None
			try:
				regexp = r'<img src="(.*)">'
				formats_url = re.search(regexp, normalized_descr).group(1)
				item['formats'] = self.format_url_hash_to_format_name.get(zlib.crc32(formats_url), None)
			except AttributeError, e:
				item['formats'] = None
				
			
			


