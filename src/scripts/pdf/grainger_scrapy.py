import config
import crochet
import scrapy
from common import Log,get_scrapy_settings,CustomScrapyFilesItem
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

crochet.setup()


# search_param=do630 voltage regulator (via category list)
# search_param=do 360 voltage (via product list)
# search_param=61HH68 (via direct product page)

# variables for eval() to parse
null = 'null'
true = 'true'
false = 'false'

# ---------------------SCRAPING-CLASS---------------------

class GriengerPDFScrapy(scrapy.Spider):
    name = 'GriengerPDFScrapy'

    def __init__(self, search_param, eslog):
        self.eslog = eslog
        self.main_url = 'https://www.grainger.com/'
        self.start_urls = [
            "https://www.grainger.com/search?searchQuery="+search_param]
        super().__init__()

    def parse(self, response):
        if 'search?' not in response.url:
            yield scrapy.Request(url=response.url, callback=self.collect_data)
        else:
            if len(response.css('section[aria-label="Category products"]')) > 0:
                script = [i.strip() for i in response.css('script::text').extract(
                ) if i.strip().startswith('window.__PRELOADED_STATE__')][0]
                script = eval(script.split(
                    '=', 1)[-1].split('window.__UI_CONFIG__')[0].strip()[:-1])
                products = list(script['category']['category']
                                ['skuToProductMap'].keys())
                href = '/product/info?productArray='+','.join(products)
                yield scrapy.Request(url=self.main_url+href, callback=self.get_products)
            else:
                # iterate every categories
                for href in response.css('a.route::attr(href)').extract():
                    yield scrapy.Request(url=self.main_url+href, callback=self.parse_category_page)

    def parse_category_page(self, response):
        script = [i.strip() for i in response.css('script::text').extract(
        ) if i.strip().startswith('window.__PRELOADED_STATE__')][0]
        script = eval(script.split('=', 1)
                      [-1].split('window.__UI_CONFIG__')[0].strip()[:-1])
        cat_id = script['category']['category']['id']
        for i in script['category']['collections']:
            coll_id = i['id']
            url1 = self.main_url + \
                '/experience/pub/api/products/collection/{0}?categoryId={1}'
            yield scrapy.Request(url=url1.format(coll_id, cat_id), callback=self.get_products)

    def get_products(self, response):
        data = response.json()
        if 'products' in data.keys():
            for i in data['products']:
                yield scrapy.Request(url=self.main_url+i['productDetailUrl'], callback=self.collect_data)
        else:
            for i in data.values():
                if type(i) == dict and 'productDetailUrl' in i.keys():
                    yield scrapy.Request(url=self.main_url+i['productDetailUrl'], callback=self.collect_data)

    def collect_data(self, response):
        data = dict()
        main_content = response.css('.product-detail__content--large')
        for li in main_content.css('.product-detail__product-identifiers-content'):
            key = li.css(
                '.product-detail__product-identifiers-label::text').get().strip()
            value = li.css(
                '.product-detail__product-identifiers-description::text').extract()
            value = [str(i).strip() for i in value] if len(
                value) > 1 else str(value[0]).strip()
            data[key] = value

        for a_tag in response.css('a.documentation__link'):
            a_href = a_tag.xpath('./@href').get()
            a_name = a_tag.xpath('./@title').get().strip()
            filename = data['Item #']+'-'+a_name+'.'+a_href.split('.')[-1]
            item = CustomScrapyFilesItem()
            item['file_name'] = filename
            item['file_urls'] = ['https:'+a_href]
            self.eslog.data(
                {'file_name': filename, 'file_urls': ['https:'+a_href]})
            yield item

# ---------------------SCRAPING-FUNCTION---------------------


def GraingerScrapy(agentContext):
    log = agentContext.log
    log.job(config.JOB_RUNNING_STATUS, 'Job Started')

    runner = CrawlerRunner(settings=get_scrapy_settings(agentContext.jobId))
    runner.crawl(
        GriengerPDFScrapy, search_param=agentContext.requestBody.get('search'), eslog=log)
    runner.join()
    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Successfully scraped all data')
