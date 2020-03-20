# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import Item


class ZhiLianSpider(scrapy.Spider):
    name = 'ZhiLian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://zhaopin.com/citymap']
    custom_settings = {"ITEM_PIPELINES": {
                            'job.pipelines.ZhiLianPipeline': 300, },  # 保存数据
                       "AUTOTHROTTLE_START_DELAY": 30, }
    # 覆盖配置文件

    def parse(self, response):
        cityMapList = {}
        for index in response.xpath("//script[not(@*)]/text()"):
            text = index.get().strip()
            if "__INITIAL_STATE__" in text:
                cityList = json.loads(text.replace("__INITIAL_STATE__=", '')).get("cityList")
                if cityList:
                    cityMapList = cityList.get("cityMapList")  # 返回城市首字母集合（dict）
                else:
                    print("[ERROR]获取所有城市信息异常")
                break
        for index in list(cityMapList):
            for node in cityMapList.get(index, [""]):
                """:return
                    {'name': '鞍山', 'url': '//www.zhaopin.com/anshan/', 'code': '601', 'pinyin': 'anshan'}
                """
                print(node)
                url = "http://zhaopin.com"
                yield scrapy.Request(url=url,
                                     meta=node,
                                     callback=self.pare_detail,
                                     dont_filter=True)

    def pare_detail(self, response):
        """
        :param
            https://fe-api.zhaopin.com/c/i/sou?
            start=0&  ### start=90&  # 开始页数
            pageSize=90&   # 一页数据量
            cityId=530&   # 城市id
            salary: 1,1000&  # 薪资筛选
            industry: 200010000,200020000&  # 行业筛选
            workExperience=-1&  # 工作经验
            education=-1&    # 学历要求
            companyType=-1&  # 公司性质
            employmentType=-1&
            jobWelfareTag=-1&  # 职位标签
            kw=Java%E5%BC%80%E5%8F%91&   # 搜索关键字
            kt=3&
            _v=0.14457681&
            x-zp-page-request-id=b38cfe6dbf2743e99a05cf401d15d441-1573998204485-431858&
            x-zp-client-id=aba478b1-e5c2-4dfb-b573-f21ff000c2e9&
            MmEwMD=49XN4YhuFk3bp0Whq1Bl.S6ViV268mAWv_e_ohd24ySeOdm3sjMrAHERWe9IYDMPPWlVdnTQutLot62sDX10rf8Gp_TPDQo5sT3J7wb6SYS2KPYvJpL2DXysR7H3IiRII04GZjA0wxBvsTM1GYHnlcocpuLzTd1T3lmA6U5U.5ARpJMrTBVcW1CsbPFtr8vbIOccgR3zbaS7Dp1GOeHuiQPKcYAeMcUlndnKgvu31TbZwe3fj7I9ZeLPW4SV_218ZiqUHglWGwLK8XXAJ7zzmMk7PxSkBVCqwCfjZXllGIVJkYunEcQRi.rdFLvrDCo_JXvZkrei7X5or.meJdYK0sXW3Qd8saqON3vH_TvVcMeCri4PZwNz8j6XtWOY4oEW5NZ0aVY.aizG3T3dzChgMSMx4
        """
        for node in response.xpath('//a[@class="zp-jobNavigater__pop--href"]/text()'):
            jobName = node.get().strip()
            url = "https://fe-api.zhaopin.com/c/i/sou?start={}&" \
                  "pageSize=90&cityId={}&workExperience=-1&education=-1&" \
                  "companyType=-1&employmentType=-1&jobWelfareTag=-1&" \
                  "kw={}&kt=3".format(0, response.meta.get("code"), jobName)
            yield scrapy.Request(url=url,
                                 meta={"cityCode": response.meta.get("code"), "kw": jobName, "startPage": 0},
                                 callback=self.parse_api,
                                 dont_filter=False)

    def parse_api(self, response):
        item = Item()
        startPage = response.meta.get("startPage", 0) + 90  # 翻页
        jsonData = json.loads(response.text)
        data = jsonData.get("data")
        if data:
            results = data.get("results")
            if results:
                for index in results:
                    item["data"] = index
                    yield item
                url = "https://fe-api.zhaopin.com/c/i/sou?start={}&" \
                      "pageSize=90&cityId={}&workExperience=-1&education=-1&" \
                      "companyType=-1&employmentType=-1&jobWelfareTag=-1&" \
                      "kw={}&kt=3".format(startPage,
                                          response.meta.get("code"),
                                          response.meta.get("kw"))
                yield scrapy.Request(url=url,
                                     meta={"cityCode": response.meta.get("code"),
                                           "kw": response.meta.get("kw"),
                                           "startPage": startPage},
                                     callback=self.parse_api,
                                     dont_filter=False)
