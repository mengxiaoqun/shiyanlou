# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem
from shiyanlougithub.models import Repository, engine

class RepositoriesSpider(scrapy.Spider):
    name = 'repositories'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']
    
    @property
    def start_urls(self):
        url_list = ['https://github.com/shiyanlou?tab=repositories']
        return url_list

    def parse(self, response):
        for github in response.css('li.col-12'):
            item = RepositoryItem({
                'name': github.css('h3 a::text').extract_first().strip(),
                'update_time':github.css('div[class="f6 text-gray mt-2"] relative-time::attr(datetime)').extract_first().strip()
            })

            github_url = github.css('h3 a::attr(href)').extract_first()
            full_github_url = response.urljoin(github_url)
            #full_github_url = "https://github.com/shiyanlou/flask"

            request = scrapy.Request(full_github_url, callback=self.parse_details)
            request.meta['item'] = item
            yield request

        if (response.css('div.BtnGroup button') == []):
            url = response.css('div.BtnGroup a::attr(href)')[1]
        else:
            url = response.css('div.BtnGroup a::attr(href)')[0]
        
        yield response.follow(url, callback=self.parse)

    def parse_details(self, response):
        item = response.meta['item']
        item['commits'] = response.css('ul.numbers-summary li.commits a span::text').extract_first().strip()
        item['branches'] = response.xpath("//ul[@class='numbers-summary']/li[2]/a/span/text()").extract_first().strip()
        item['releases'] = response.xpath("//ul[@class='numbers-summary']/li[3]/a/span/text()").extract_first().strip()
        yield item
