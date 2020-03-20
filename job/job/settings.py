# -*- coding: utf-8 -*-

# Scrapy settings for job project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'job'

SPIDER_MODULES = ['job.spiders']
NEWSPIDER_MODULE = 'job.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'job (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# Scrapy下载执行现有的最大请求数
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 现有的最大请求数，对于任何单域同时进行
CONCURRENT_REQUESTS_PER_DOMAIN = 32
# 现有的请求的最大数量的同时执行任何单一的IP
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 禁止cookies
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,imag',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #               'Chrome/72.0.3626.119 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'job.middlewares.JobSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'job.middlewares.JobDownloaderMiddleware': 543,
    'job.middlewares.RandomUserAgentMiddleware': 543,
    'job.middlewares.LocalRetryMiddleware': 544,
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'job.pipelines.JobPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# 开始下载时限速并延迟时间
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# 高并发请求时最大延迟时间
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

##################################################
# redis
##################################################
# 指定redis数据库的连接参数
# REDIS_HOST = "182.92.77.158"
# REDIS_PORT = "6379"
# REDIS_PARAMS = {
#     'password': '@ROOTweilan157',  # 服务器的redis对应密码
# }
# 是否允许暂停
# SCHEDULER_PERSIST = True
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 400,
# }

##################################################
# mongodb
##################################################
# ip
MONGODB_HOST = '182.92.77.158'
# 端口号， 默认27017
MONGODB_POST = 27017
# 设置数据库名称
MONGODB_DBNANME = 'db_job'
# 用户名
MONGODB_USERNAME = 'root'
# 密码
MONGODB_PASSWORD = '@ROOTweilan157'

##################################################
# MYsql
##################################################
# ip
MYSQL_HOST = '182.92.77.158'
# 端口号， 默认27017
MYSQL_POST = 3306
# 设置数据库名称
MYSQL_DBNANME = 'db_job'
# 用户名
MYSQL_USERNAME = 'root'
# 密码
MYSQL_PASSWORD = '@ROOTweilan157'
#################################################
#################################################

# 请求头版本
RANDOM_UA_TYPE = "chrome"

RETRY_ENABLED = True  # 是否开启retry
RETRY_TIMES = 100  # 重试次数
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# # web服务  在爬虫运行的时候访问http://localhost:6080/crawler即可查看爬虫运行情况
# EXTENSIONS = {
#     'scrapy_jsonrpc.webservice.WebService': 500,
# }
# JSONRPC_PORT = [6025]
# JSONRPC_ENABLED = True
