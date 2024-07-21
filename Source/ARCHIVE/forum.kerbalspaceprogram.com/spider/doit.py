from typing import Iterable

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import crawler

class MySpider(CrawlSpider):
	name = 'forum.kerbalspaceprogram.com'
	allowed_domains = ['forum.kerbalspaceprogram.com', 'kerbal-forum-uploads.s3.us-west-2.amazonaws.com']
	start_urls = ['https://forum.kerbalspaceprogram.com/']
	custom_settings = {
		'AUTOTHROTTLE_ENABLED': True,
		'AUTOTHROTTLE_START_DELAY': 1,
		'AUTOTHROTTLE_MAX_DELAY': 300,	# 5 Minutes
		'CONCURRENT_REQUESTS': 64,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 32,
		'RETRY_TIMES': 1024,
		'DOWNLOADER_MIDDLEWARES': {
			'crawler.CustomProxyMiddleware': 350,
		},
		'DUPEFILTER_CLASS': 'crawler.SeenURLFilter',
		'USER_AGENT': "Mozilla/5.0 (Linux; x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
		'DEFAULT_REQUEST_HEADERS': {
			"Accept-Encoding": "identity"
		}
	}

	rules = (
		Rule(LinkExtractor(), callback='parse_item', follow=True),
	)

	def parse_item(self, response):
#		print(response.url)
		urls = response.css('link::attr(href)').getall()
		urls += response.css('script::attr(src)').getall()
		urls += response.css('img::attr(src)').getall()
		for link in urls:
#			print (link)
			if not link.startswith("http"):
				link = f"https:{link}"
			yield {'url': link}
		yield {'url': response.url}

