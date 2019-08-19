#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import scrapy
class ShiyanlouGithubScrapy(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        url_list = ['https://github.com/shiyanlou?tab=repositories',
'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwODowNjo1MyswODowMM4FkpKN&tab=repositories',
'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0zMVQyMDoyMDowMiswODowMM4BzHi1&tab=repositories',
'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMi0wNFQwMDoxNzo1MyswODowMM4BpCnu&tab=repositories',
'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0wOS0xNlQxMDowNjowMyswODowMM4Bb3Ud&tab=repositories']
        return url_list

    def parse(self,response):
        for github in response.css('li.col-12'):
            yield{
            'name':github.css('h3 a::text').extract_first().strip(),
            'update-time':github.css('div[class="f6 text-gray mt-2"] relative-time::attr(datetime)').extract_first().strip()
            }
