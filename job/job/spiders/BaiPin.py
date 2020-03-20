# -*- coding: utf-8 -*-
import scrapy
# from scrapy_redis.spiders import RedisCrawlSpider


class BaipinSpider(scrapy.Spider):
    name = 'BaiPin'
    allowed_domains = ['zhaopin.baidu.com']
    start_urls = ['http://zhaopin.baidu.com/']

    def parse(self, response):
        pass
