# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
from . import settings


class JobPipeline(object):
    def process_item(self, item, spider):
        return item


class BasePipeline(object):
    def __init__(self):
        self.client = None
        self.db = None
        self.coll = None
        self.conn = None
        self.cur = None
        self.initMongodb()
        self.initMysql()

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def initMongodb(self):
        try:
            # 链接数据库
            self.client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_POST)
            # 数据库登录需要帐号密码的话
            self.client.admin.authenticate(settings.MONGODB_USERNAME, settings.MONGODB_PASSWORD)
            self.db = self.client[settings.MONGODB_DBNANME]  # 获得数据库的句柄
        except Exception as e:
            return e

    def initMysql(self):
        try:
            self.conn = pymysql.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_POST,
                user=settings.MYSQL_USERNAME,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DBNANME,
                charset="utf8mb4")
            # 创建游标，操作设置为字典类型
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            return e

    def process_item(self, item, spider):
        try:
            # self.__addMysql(dict(item), "")
            # self.__addMongodb(dict(item), "")
            pass
        except Exception as e:
            return e
        return item

    def addMongodb(self, data, tbName):
        try:
            self.coll = self.db[tbName]  # 获得collection的句柄
            self.coll.insert(data)  # 向数据库插入一条记录
            self.coll.create_index([("url", 1), ("addDate", 1)], unique=True)
        except Exception as e:
            return e

    def addMysql(self, data, tbName):
        try:
            self.cur.execute("""CREATE TABLE {} (`id` INT UNSIGNED AUTO_INCREMENT,
                 `title` VARCHAR(1000),
                 `enterprise` VARCHAR(1000),
                 `jobAddr` VARCHAR(1000),
                 `pay` VARCHAR(1000),
                 `releaseDate` VARCHAR(1000),
                 `academicRequirement` VARCHAR(1000),
                 `experienceRequirement` VARCHAR(1000),
                 `enterpriseNature` VARCHAR(1000),
                 `enterpriseScale` VARCHAR(1000),
                 `abstract` TEXT(10000),
                 `jobType` VARCHAR(1000),
                 `job` VARCHAR(1000),
                 `city` VARCHAR(1000),
                 `addDate` DATETIME NOT NULL,
                 `url` VARCHAR(100) NOT NULL,
                 PRIMARY KEY (`id`),
                 UNIQUE index index_url(url, addDate));""" .format(tbName))
            # self.cur.execute("CREATE DATABASE tb_A51job;")
        except Exception as e:
            return e
        finally:
            try:
                cmd = """INSERT INTO {} (title, enterprise, jobAddr, pay, releaseDate,
                                         academicRequirement, experienceRequirement, 
                                         enterpriseNature, enterpriseScale, abstract,
                                         jobType, job, city, addDate, url) VALUES (
                                         %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""".format(tbName)
                cmd_values = (data.get("title"),
                              data.get("enterprise"),
                              data.get("jobAddr"),
                              data.get("pay"),
                              data.get("releaseDate"),
                              data.get("academicRequirement"),
                              data.get("experienceRequirement"),
                              data.get("enterpriseNature"),
                              data.get("enterpriseScale"),
                              data.get("abstract"),
                              data.get("jobType"),
                              data.get("job"),
                              data.get("city"),
                              data.get("addDate"),
                              data.get("url"),
                              )
                self.cur.execute(cmd, cmd_values)
            except Exception as e:
                return e


class A51jobPipeline(object):
    def __init__(self):
        self.__initMongodb()
        self.__initMysql()

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def __initMongodb(self):
        try:
            # 链接数据库
            self.client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_POST)
            # 数据库登录需要帐号密码的话
            self.client.admin.authenticate(settings.MONGODB_USERNAME, settings.MONGODB_PASSWORD)
            self.db = self.client[settings.MONGODB_DBNANME]  # 获得数据库的句柄
            self.coll = self.db["tb_A51job"]  # 获得collection的句柄
        except Exception as e:
            return e

    def __initMysql(self):
        try:
            self.conn = pymysql.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_POST,
                user=settings.MYSQL_USERNAME,
                password=settings.MYSQL_PASSWORD,
                database=settings.MYSQL_DBNANME,
                charset="utf8mb4")
            # 创建游标，操作设置为字典类型
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            return e

    def process_item(self, item, spider):
        try:
            self.__addMysql(item["data"])
            self.__addMongodb(item["data"])
        except Exception as e:
            return e
        return item

    def __addMongodb(self, data):
        try:
            self.coll.insert(data)  # 向数据库插入一条记录
        except Exception as e:
            return e

    def __addMysql(self, data):
        try:
            self.cur.execute("""CREATE TABLE tb_A51job (`id` INT UNSIGNED AUTO_INCREMENT,
                                                        `title` VARCHAR(1000),
                                                        `enterprise` VARCHAR(1000),
                                                        `jobAddr` VARCHAR(1000),
                                                        `pay` VARCHAR(1000),
                                                        `releaseDate` VARCHAR(1000),
                                                        `academicRequirement` VARCHAR(1000),
                                                        `experienceRequirement` VARCHAR(1000),
                                                        `enterpriseNature` VARCHAR(1000),
                                                        `enterpriseScale` VARCHAR(1000),
                                                        `abstract` TEXT(10000),
                                                        `jobType` VARCHAR(1000),
                                                        `job` VARCHAR(1000),
                                                        `city` VARCHAR(1000),
                                                        `addDate` DATETIME NOT NULL,
                                                        `url` VARCHAR(1000) NOT NULL,
                                                        PRIMARY KEY (`id`))""")
            # self.cur.execute("CREATE DATABASE tb_A51job;")
        except Exception as e:
            return e
        finally:
            try:
                cmd = """INSERT INTO tb_A51job (title, enterprise, jobAddr, pay, releaseDate,
                                                academicRequirement, experienceRequirement, 
                                                enterpriseNature, enterpriseScale, abstract,
                                                jobType, job, city, addDate, url) VALUES (
                                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cmd_values = (data.get("title"),
                              data.get("enterprise"),
                              data.get("jobAddr"),
                              data.get("pay"),
                              data.get("releaseDate"),
                              data.get("academicRequirement"),
                              data.get("experienceRequirement"),
                              data.get("enterpriseNature"),
                              data.get("enterpriseScale"),
                              data.get("abstract"),
                              data.get("jobType"),
                              data.get("job"),
                              data.get("city"),
                              data.get("addDate"),
                              data.get("url"),
                              )
                self.cur.execute(cmd, cmd_values)
            except Exception as e:
                return e


class BooszhipinPipeline(object):
    """"""
    def process_item(self, item, spider):
        pass


class ZhiLianPipeline(object):
    def __init__(self):
        # 链接数据库
        self.client = pymongo.MongoClient(host=settings.MONGODB_HOST, port=settings.MONGODB_POST)
        # 数据库登录需要帐号密码的话
        self.client.admin.authenticate(settings.MONGODB_USERNAME, settings.MONGODB_PASSWORD)
        self.db = self.client[settings.MONGODB_DBNANME]  # 获得数据库的句柄
        self.coll = self.db["tb_ZhiLian"]  # 获得collection的句柄

    def process_item(self, item, spider):
        try:
            self.coll.insert(item["data"])  # 向数据库插入一条记录
        except Exception as e:
            return e
        return item


class LaGouPipeline(BasePipeline):
    def process_item(self, item, spider):
        try:
            tbName = "tb_LaGou"
            data = dict(item)
            self.addMysql(data, tbName)
            self.addMongodb(data, tbName)
        except Exception as e:
            return e
        return item
