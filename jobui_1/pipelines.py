# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class Jobui1Pipeline(object):
    def __init__(self):
        self.cli = pymongo.MongoClient(host='localhost', port=27018)
    def process_item(self, item, spider):
        item = dict(item)
        print(item)
        self.cli['douban_3']['datas'].insert_one(item)
        return item
