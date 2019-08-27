# -*- coding: utf-8 -*-
import json
import redis
import re
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item['summary'] = re.sub('\s+',' ',item['summary'])
        movie_len = self.redis.llen('douban_movie:items')
        if not float(item['score']) >= 8.0:
            raise DropItem('score less than 8.0')
        if movie_len > 32:
            raise DropItem('movie more than 32')
        self.redis.lpush('douban_movie:items',json.dumps(dict(item)))

    def open_spider(self,spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    
