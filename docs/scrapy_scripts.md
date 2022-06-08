
# Scrapy Scripts

A Scrapy Script must contain Scrapy.Spider class and a SpiderRunning Function

script_format:

```
# mandatory import 
import crochet
crochet.setup()
# crochet runs scrapy.twistor inside flask (without this errors!)

# imports
import scrapy

Class Myspider(scrapySpider):
    # scraping code goes here

def MySpiderFunc(agentRunContext):
    log = Log(agentRunContext)
    log.job(config.JOB_RUNNING_STATUS, 'Job Started')

    # start a CrawlerRunner instance
    runner = CrawlerRunner(my_settings)
    
    # start crawling
    runner.crawl(
        Myspider, *args, eslog=log)
    
    # wait until scraping finished
    reactor.run()
    
    # log for finished job
    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Successfully scraped all data')
```

agents_format:
```
[
    {
        "agentId": "SAMPLE-AGENT",
        "description": "scrapy crawler for sample-agent website",
        "provider": "sample agent",
        "URL": "https://www.sample-agent.com",
        "scripts": {
            "info": "MySpiderFunc",
            "PDF": "NoPDFScript"
        }
    }
]
```

## NOTE

1. import of crochet and setup is mandatory while writing scrapy Scripts.
2. for storing files , use settings and classes available in src/common/scrapy_utils.py