# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Item(scrapy.Item):
    # # define the fields for your item here like:
    # # name = scrapy.Field()
    # pass
    data = scrapy.Field()


class BaseItem(scrapy.Item):
    """基础字段"""
    title = scrapy.Field()  # 职位名称
    enterprise = scrapy.Field()  # 招聘公司
    jobAddr = scrapy.Field()  # 工作地点
    pay = scrapy.Field()  # 薪资
    releaseDate = scrapy.Field()  # 发布时间
    academicRequirement = scrapy.Field()  # 学历要求
    experienceRequirement = scrapy.Field()  # 工作经验
    enterpriseNature = scrapy.Field()  # 公司性质
    enterpriseScale = scrapy.Field()  # 公司规模
    abstract = scrapy.Field()  # 摘要
    jobType = scrapy.Field()  # 职业类型
    job = scrapy.Field()  # 职业名称
    city = scrapy.Field()  # 所属城市
    addDate = scrapy.Field()  # 采集时间
    url = scrapy.Field()  # 详情url
