# _*_ coding:utf-8 _*_
# 作者:
# 时间:2019/11/15/23:36
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    # process.crawl('51job')
    # process.crawl('BaiPin')
    # process.crawl('BoosZhiPin')
    process.crawl('LaGou')
    # process.crawl('LiePin')
    # process.crawl('ZhiLian')
    process.start()
