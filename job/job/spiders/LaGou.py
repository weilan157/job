# -*- coding: utf-8 -*-
import datetime
import json

import scrapy
import ssl

from job.items import BaseItem

ssl._create_default_https_context = ssl._create_unverified_context


class LagouSpider(scrapy.Spider):
    name = 'LaGou'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/']
    custom_settings = {"ITEM_PIPELINES": {
                            'job.pipelines.LaGouPipeline': 300, },  # 保存数据
                       "AUTOTHROTTLE_START_DELAY": 1, }
    # 覆盖配置文件

    def parse(self, response):
        for index in response.xpath("//div[@class='menu_sub dn']"):
            for node in index.xpath("dl"):
                job_type = node.xpath("dt/span/text()").get()
                # print(job_type)
                for i in node.xpath("dd/a[@data-lg-tj-cid='idnull']/h3/text()"):
                    if i:
                        kw = i.get()
                        yield scrapy.FormRequest(
                            url="https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false",
                            method="POST",
                            formdata={"first": "true",
                                      "pn": "1",
                                      "kd": "{}".format(kw)},
                            meta={"job_type": job_type,
                                  "kw": kw,
                                  "page": 1},
                            callback=self.pare_detail)

    def pare_detail(self, response):
        try:
            item = BaseItem()
            jsonData = json.loads(response.text)
            positionResult = jsonData.get("content", {}).get("positionResult")
            for result in positionResult.get("result", []):
                item["title"] = result.get("positionName")  # 职位名称
                item["enterprise"] = result.get("companyFullName")  # 招聘公司
                if result.get("businessZones"):
                    item["jobAddr"] = "{} {}".format(result.get("district"),
                                                     ' '.join(result.get("businessZones")))  # 工作地点
                else:
                    item["jobAddr"] = "{}".format(result.get("district"))
                item["pay"] = result.get("salary")  # 薪资
                item["releaseDate"] = result.get("createTime")  # 发布时间
                item["academicRequirement"] = result.get("education")  # 学历要求
                item["experienceRequirement"] = result.get("workYear")  # 工作经验
                item["enterpriseNature"] = result.get("financeStage")  # 公司性质
                item["enterpriseScale"] = result.get("companySize")  # 公司规模
                item["abstract"] = result.get("positionAdvantage")  # 摘要
                item["jobType"] = result.get("firstType")  # 职业类型
                item["job"] = result.get("secondType")  # 职业名称
                item["city"] = result.get("city")  # 所属城市
                item["addDate"] = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')  # 采集时间
                item["url"] = "https://www.lagou.com/jobs/{}.html".format(result.get("positionId"))  # 详情url
                yield item
            totalCount = int(positionResult.get("totalCount"))
            if response.meta.get("page") < totalCount:
                yield scrapy.FormRequest(
                    url="https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false",
                    method="POST",
                    formdata={"first": "true",
                              "pn": "1",
                              "kd": "{}".format(response.meta.get("kw"))},
                    meta={"job_type": response.meta.get("job_type"),
                          "kw": response.meta.get("kw"),
                          "page": response.meta.get("page")+1},
                    callback=self.pare_detail)
        except Exception as e:
            print(e)
