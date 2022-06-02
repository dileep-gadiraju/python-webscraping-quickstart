
import scrapy
from scrapy.pipelines.files import FilesPipeline

# search_param=do630 voltage regulator (via category list)
# search_param=do 360 voltage (via product list)
# search_param=61HH68 (via direct product page)

# variables for eval() to parse
null = 'null'
true = 'true'
false = 'false'

def GraingerScrapy(agentRunContext):

    class GeneralFilesItem(scrapy.Item):
        file_name = scrapy.Field()
        file_urls = scrapy.Field()
        files = scrapy.Field


    class GenreralFilesPipeline(FilesPipeline):
        def get_media_requests(self, item, info):
            for my_url in item.get('file_urls', []):
                yield scrapy.Request(my_url, meta={'file_name': item.get('file_name')})

        def file_path(self, request, response=None, info=None):
            return request.meta['file_name']


    class GriengerPDFScrapy(scrapy.Spider):
        name = 'GriengerPDFScrapy'
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        main_url = 'https://www.grainger.com/'
        custom_settings = {
            'ITEM_PIPELINES': {'grienger_scrapy_pdf.GenreralFilesPipeline': 1},
            'FILES_STORE': '/home/test/Music/down/'
        }

        def __init__(self, agentRunContext):
            self.start_urls = [
                "https://www.grainger.com/search?searchQuery="+agentRunContext.requestBody['search']]
            super().__init__()
            self

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
                item = GeneralFilesItem()
                item['file_name'] = filename
                item['file_urls'] = ['https:'+a_href]
                yield item
