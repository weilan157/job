# -*- coding: utf-8 -*-
import datetime
import time

import scrapy

from selenium import webdriver
from job.items import BaseItem
# from scrapy_redis.spiders import RedisCrawlSpider


class BooszhipinSpider(scrapy.Spider):
    name = 'BoosZhiPin'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://zhipin.com/?city=100010000']  # 全国
    custom_settings = {"ITEM_PIPELINES": {
        'job.pipelines.BooszhipinPipeline': 300, },  # 保存数据
    }

    def parse(self, response):
        cookie = self.get_cookie()
        for li in response.xpath("//div[@class='job-menu']//li"):
            job_type = li.xpath("h4/text()").get()
            for a in li.xpath("div/a"):
                job = a.xpath("text()").get()
                url = 'https://zhipin.com{}'.format(a.attrib.get("href"))
                yield scrapy.Request(url=url,
                                     cookies={'__zp_stoken__': cookie},
                                     meta={"type": job_type,
                                           "job": job,
                                           # "dont_merge_cookies": True,  # 不保存cookie
                                           },
                                     callback=self.pare_detail)

    def pare_detail(self, response):
        data = BaseItem()
        for index in response.xpath("//div[@class='job-list']/ul/li"):
            data["title"] = index.xpath("//div[@class='job-title']/text()").get()  # 职位名称
            data["enterprise"] = index.xpath("//div[@class='info-company']//a/text()").get()  # 招聘公司
            data["jobAddr"] = index.xpath("//div[@class='info-primary']/p//text()")[0].get()  # 工作地点
            data["pay"] = index.xpath("//span[@class='red']//text()").get()  # 薪资
            data["releaseDate"] = ""  # 发布时间
            data["academicRequirement"] = index.xpath("//div[@class='info-primary']/p//text()")[2].get()  # 学历要求
            data["experienceRequirement"] = index.xpath("//div[@class='info-primary']/p//text()")[1].get()  # 工作经验
            data["enterpriseNature"] = index.xpath("//div[@class='company-text']/p//text()")[1].get()  # 公司性质
            data["enterpriseScale"] = index.xpath("//div[@class='company-text']/p//text()")[2].get()  # 公司规模
            data["abstract"] = ""  # 摘要
            data["jobType"] = response.meta.get("type")  # 职业类型
            data["job"] = response.meta.get("job")  # 职业名称
            data["city"] = ""  # 所属城市
            data["addDate"] = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  # 采集时间
            data["url"] = "https://www.zhipin.com{}".format(
                index.xpath("//div[@class='info-primary']/h3/a").attrib.get("href"))  # 详情url
            yield data
        next_page = response.xpath("//div[@class='page']/a[@class='next']")
        if next_page:
            next_url = next_page.attrib.get("href")
            yield scrapy.Request(url="https://www.zhipin.com{}".format(next_url),
                                 callback=self.pare_detail)

    @staticmethod
    def get_cookie():
        options = webdriver.ChromeOptions()
        options.add_argument("User-Agent="
                             "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                             " like Gecko) Chrome/79.0.3945.88 Safari/537.36'")
        # options.binary_location = r"D:\Program Files\Google\Chrome\Application\chrome.exe"
        options.add_argument('--no-sandbox')  # 让Chrome在root权限下跑
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

        driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
        # driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
        driver.get("https://www.zhipin.com/c100010000-p100199/?ka=search_100199")
        # driver.get("https://www.baidu.com")
        time.sleep(2)
        cookie = driver.get_cookie("__zp_stoken__")
        driver.quit()
        return cookie.get("value")
