import config
import crochet
import scrapy
from common import Log,get_scrapy_settings
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

crochet.setup()

# ---------------------SCRAPING-CLASS---------------------

class RSSpider(scrapy.Spider):
    name = 'RSSpider'

    def __init__(self,search_param, eslog):
        self.eslog = eslog
        self.main_domain = 'https://in.rsdelivers.com'
        self.start_urls = ['https://in.rsdelivers.com/productlist/search?query='+search_param]

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
            except:
                break
        data['title'] = str(response.css('h1.title::text').get()).strip()
        data['url'] = response.url
        self.eslog.data(data)

# ---------------------SCRAPING-FUNCTION---------------------

def RSScrapy(agentRunContext):
    log = Log(agentRunContext)
    log.job(config.JOB_RUNNING_STATUS, 'Job Started')

    runner = CrawlerRunner(settings=get_scrapy_settings(agentRunContext.jobId))
    runner.crawl(
        RSSpider, search_param=agentRunContext.requestBody.get('search'), eslog=log)

    runner.join()
    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Successfully scraped all data')