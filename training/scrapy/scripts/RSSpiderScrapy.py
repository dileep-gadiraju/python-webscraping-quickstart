import scrapy

class RSSpider(scrapy.Spider):
    crawler = 'RSSpider'
    name = 'RSSpider'
    main_domain = 'https://in.rsdelivers.com'
    start_urls = ['https://in.rsdelivers.com/productlist/search?query=749']

    def parse(self,response):
        for ele in response.css('a.snippet'):
            my_href = ele.xpath('./@href').get()
            yield scrapy.Request(url=self.main_domain+my_href,callback=self.collect_data)

    def collect_data(self,response):
        data = dict()
        meta_data = response.css('div.row-inline::text').extract()
        for i in range(0,100,3):
            try:
                data[meta_data[i]] = meta_data[i+2]
            except Exception:
                break
        data['title'] = str(response.css('h1.title::text').get()).strip()
        data['url'] = response.url
        yield data
