# -*- coding: utf-8 -*-
import datetime

import scrapy
from job.items import Item


class A51jobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = ['https://51job.com/']
    custom_settings = {"ITEM_PIPELINES": {
        'job.pipelines.A51jobPipeline': 300, },  # 保存数据
    }

    def parse(self, response):
        a_list = response.xpath("//div[@id='area_channel_homepage_all']//span/a")
        for index in a_list:
            print("https:{}".format(index.attrib.get("href")))
            print(index.xpath("text()").get())
            yield scrapy.Request(url="https:{}".format(index.attrib.get("href")),
                                 meta={"city": index.xpath("text()").get()},
                                 callback=self.pare_list)

    def pare_list(self, response):
        for div in response.xpath("//div[@class='sbt']/div[@class='hle']"):
            for index in div.xpath("div/a"):
                print(div.xpath("span/text()").get())
                print(index.attrib.get("href"))
                print(index.xpath("text()").get())
                yield scrapy.Request(url=index.attrib.get("href"),
                                     meta={"jobType": div.xpath("span/text()").get(),
                                           "job": index.xpath("text()").get(),
                                           "city": response.meta.get("city")},
                                     callback=self.pare_detail)

    def pare_detail(self, response):
        item = Item()
        detail_box = response.xpath("//div[@class='detlist gbox']")
        if detail_box:
            for index in detail_box.xpath("div"):
                data = {"title": index.xpath("p[@class='info']/span[@class='title']//text()").get(),  # 职位名称
                        "enterprise": index.xpath("p[@class='info']/a[@class='name']//text()").get(),  # 招聘公司
                        "jobAddr": index.xpath("p[@class='info']/span[@class='location name']//text()").get(),  # 工作地点
                        "pay": index.xpath("p[@class='info']/span[@class='location']//text()").get(),  # 薪资
                        "releaseDate": index.xpath("p[@class='info']/span[@class='time']//text()").get(),  # 发布时间
                        "academicRequirement": index.xpath("p[@class='order']//text()")[0].get().split("学历要求：")[1],  # 学历要求
                        "experienceRequirement": index.xpath("p[@class='order']//text()")[2].get().split("工作经验：")[1],  # 工作经验
                        "enterpriseNature": index.xpath("p[@class='order']//text()")[4].get().split("公司性质：")[1],  # 公司性质
                        "enterpriseScale": index.xpath("p[@class='order']//text()")[6].get().split("公司规模：")[1],  # 公司规模
                        "abstract": index.xpath("p[@class='text']//text()").get(),  # 摘要
                        "jobType": response.meta.get("jobType"),  # 职业类型
                        "job": response.meta.get("job"),  # 职业名称
                        "city": response.meta.get("city"),  # 所属城市
                        "addDate": (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),  # 采集时间
                        "url": index.xpath("p[@class='info']/span[@class='title']/a").attrib.get("href"),  # 详情url
                        }
                item["data"] = data
                yield item
        next_page = response.xpath("//div[@class='p_in']/ul/li[@class='bk'][2]/a")
        if next_page:
            next_url = next_page.attrib.get("href")
            yield scrapy.Request(url=next_url,
                                 meta={"jobType": response.meta.get("jobType"),
                                       "job": response.meta.get("job"),
                                       "city": response.meta.get("city")},
                                 callback=self.pare_detail)
