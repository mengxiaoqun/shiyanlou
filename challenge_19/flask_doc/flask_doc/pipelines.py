# -*- coding: utf-8 -*-
import re
import redis
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        item['text'] = re.sub('\s+',' ',item['text'])
        self.redis.lpush('flask_doc:items',json.dumps(dict(item)))
        return item
    
    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
