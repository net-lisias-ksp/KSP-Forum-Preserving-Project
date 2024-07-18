import os
from urllib.parse import urlparse

class CustomProxyMiddleware(object):
	def __init__(self):
		self.proxy = dict()
		self.proxy['*'] = 'http://steamdeck:8081'		# Content
		self.proxy['gif'] = 'http://steamdeck:8082'		# Images
		self.proxy['png'] = 'http://steamdeck:8082'
		self.proxy['jpg'] = 'http://steamdeck:8082'
		self.proxy['jpeg'] = 'http://steamdeck:8082'
		self.proxy['webp'] = 'http://steamdeck:8082'
		self.proxy['svg'] = 'http://steamdeck:8082'
		self.proxy['css'] = 'http://steamdeck:8083'		# CSS
		self.proxy['woff2'] = 'http://steamdeck:8083'
		self.proxy['js'] = 'http://steamdeck:8083'

	def process_request(self, request, spider):
		if 'proxy' not in request.meta:
			path = urlparse(request.url).path
			ext = os.path.splitext(path)[1]
			selector = ext[1:].lower()
			if not selector in self.proxy:
				selector = '*'
			request.meta['proxy'] = self.proxy[selector]
		print ("** SELECTED", request.meta['proxy'])

	def get_proxy(self):
		return self.proxy['*']

