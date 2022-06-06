import config
import crochet
import scrapy
from common import Log,get_scrapy_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

crochet.setup()

# ---------------------SCRAPING-CLASS---------------------

class AppliedSpider(scrapy.Spider):
    name = 'applied'
    
    def __init__(self, search_param,eslog):
        self.eslog = eslog
        self.api_url = 'https://www.applied.com'
        self.start_urls = [
            'https://www.applied.com/search?page=0&search-category=all&override=true&isLevelUp=false&q='+search_param]
        super().__init__()

    def parse(self, response):
        # search url parsing
        for scrape_url in response.xpath('//a[@class="hide-for-print more-detail"]/@href').extract():
            # extract product url
            yield scrapy.Request(self.api_url+scrape_url, self.collect_data)

        # extract next page url and re-run function
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page is not None:
            yield scrapy.Request(self.api_url+next_page, self.parse)

    # product url parsing
    def collect_data(self, response):

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
        }
        self.eslog.data(data)

# ---------------------SCRAPING-FUNCTION---------------------

def AppliedScrapy(agentRunContext):
    log = Log(agentRunContext)
    log.job(config.JOB_RUNNING_STATUS, 'Job Started')

    runner = CrawlerRunner(settings=get_scrapy_settings(agentRunContext.jobId))
    runner.crawl(
        AppliedSpider, search_param=agentRunContext.requestBody.get('search'), eslog=log)
    reactor.run()
    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Successfully scraped all data')