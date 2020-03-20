# -*- coding: utf-8 -*-
import scrapy


class LiepinSpider(scrapy.Spider):
    name = 'LiePin'
    allowed_domains = ['liepin.com']
    start_urls = ['http://liepin.com/']

    def parse(self, response):
        pass
