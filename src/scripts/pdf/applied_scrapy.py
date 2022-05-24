import config
import scrapy
from common import Log
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


def AppliedScrapy(agentRunContext):
    log = Log(agentRunContext)

    log.job(config.JOB_RUNNING_STATUS, 'Job Started')

    log.job(config.JOB_RUNNING_STATUS, 'Script Under Development')

    log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
            'Successfully scraped all data')
