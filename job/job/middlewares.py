# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import json
import time
import execjs

import requests
from fake_useragent import UserAgent
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

from job.spiders.BoosZhiPin import BooszhipinSpider


class JobSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JobDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    """中间件-随机请求头"""

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            """Gets random UA based on the type setting (random, firefox, chrome, ie)"""
            return getattr(self.ua, self.ua_type)

        request.headers['User-Agent'] = get_ua()


class LocalRetryMiddleware(RetryMiddleware):
    """重试中间件"""

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        if response.status in self.retry_http_codes:
            time.sleep(60 * 30)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response

        # 智联招聘
        if "https://fe-api.zhaopin.com/c/i/sou" in response.url:
            resp_dct = json.loads(response.text)
            data = resp_dct.get("data")
            if resp_dct.get("code") != 200:
                reason = "code异常"
                return self._retry(request, reason, spider) or response
            if data:
                reason = "results为空"
                results = data.get("results")
                if not results:
                    return self._retry(request, reason, spider) or response
            else:
                reason = "data为空"
                return self._retry(request, reason, spider) or response
        # boss直聘
        elif "https://www.zhipin.com/web/common/security-check.html" in response.url:
            cookie = BooszhipinSpider.get_cookie()
            request.cookies.update({"__zp_stoken__": cookie.get("value")})
            reason = "获取cookie"
            return self._retry(request, reason, spider) or response

        # 拉勾网
        elif "lagou.com" in response.url:
            if not request.cookies.get("user_trace_token") and not request.cookies.get("X_HTTP_TOKEN"):
                req = requests.get("https://a.lagou.com/collect?v=1&_v=j31&a=1509746044&t=pageview&_s=1&dl=https%3A"
                                   "%2F%2Fwww.lagou.com%2F&ul=zh-cn&de=UTF-8&dt=%E6%8B%89%E5%8B%BE%E7%BD%91-%E4%B8%93"
                                   "%E4%B8%9A%E7%9A%84%E4%BA%92%E8%81%94%E7%BD%91%E6%8B%9B%E8%81%98%E5%B9%B3%E5%8F%B0"
                                   "&sd=24-bit&sr=1920x1080&vp=1017x921&je=0&_u=MEAAAAQBK~&jid=863640533&cid=9654990"
                                   ".1578493349&tid=UA-41268416-1&_r=1&z=2075111611")
                cookies = req.cookies
                user_trace_token = cookies.get("user_trace_token")
                with open('./track.js') as f:  # 执行 JS 文件
                    ctx = execjs.compile(f.read())
                    X_HTTP_TOKEN = ctx.call('get_token', user_trace_token, int(time.time()))
                request.cookies.update({"user_trace_token": user_trace_token,
                                        "X_HTTP_TOKEN": X_HTTP_TOKEN})
                request.headers['referer'] = "https//www.lagou.com/jobs/list_Java/p-city_0?px=default"
                reason = "获取cookie"
                return self._retry(request, reason, spider) or response
            # print(response.url)

        return response
