
import json
import time

from elasticsearch import Elasticsearch

import scrapy
from scrapy import Request

class AppliedSpider(scrapy.Spider):
    name = 'applied'
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    def __init__(self, search_param=''):
        self.api_url = 'https://www.applied.com'
        self.start_urls = [
            'https://www.applied.com/search?page=0&search-category=all&override=true&isLevelUp=false&q='+search_param]
        super().__init__()

    def collect_data(self, response):
        # product url parsing

        # specification data
        spec = dict()
        for trs in response.xpath('//*[@id="specifications"]//table//tr'):
            key = trs.xpath('./td[1]/text()').get().strip()
            value = trs.xpath('./td[2]/text()').get().strip()
            spec[key] = value

        # final data
        data = {
            'company': response.xpath('//h1[@itemprop="brand"]/a/text()').get().strip(),
            'product': response.xpath('//span[@itemprop="mpn name"]/text()').get().strip(),
            'details': response.xpath('//div[@class="details"]//text()').get().strip(),
            'item': response.xpath('//div[@class="customer-part-number"]/text()').get().strip(),
            'description': [x.strip() for x in response.xpath('//div[@class="short-description"]/ul/li/text()').extract()],
            'specification': spec,
            'url': response.url.strip(),
            'timestamp': int(time.time()*1000)
        }
        yield data

    def parse(self, response):
        # search url parsing
        for scrape_url in response.xpath('//a[@class="hide-for-print more-detail"]/@href').extract():
            # extract product url
            yield Request(self.api_url+scrape_url, self.collect_data)

        # extract next page url and re-run function
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            yield Request(self.api_url+next_page, self.parse)
