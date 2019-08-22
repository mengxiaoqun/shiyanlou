from sqlalchemy.orm import sessionmaker
from shiyanlougithub.items import RepositoryItem
from shiyanlougithub.models import Repository, engine
import datetime

# -*- coding: utf-8 -*-


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        commits = item['commits'].strip(',')
        item['commits'] = commits
        self.session.add(Repository(**item))
        return item
    
    def open_spider(self,spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self,spider):
        self.session.commit()
        self.session.close()

