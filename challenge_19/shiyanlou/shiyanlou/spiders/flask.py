# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    allowed_domains = ['flask.palletsprojects.com']
    start_urls = ['http://flask.palletsprojects.com/']
    
    rules = ()

    def parse(self, response):
        pass
