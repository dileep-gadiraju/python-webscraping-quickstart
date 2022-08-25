import scrapy
from config import JOB_OUTPUT_PATH
from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings


# getting settings for scrapy crawlers
def get_scrapy_settings(job_id):
    settings = {
        **get_project_settings(),
        'ITEM_PIPELINES': {'common.scrapy_utils.CustomFilesPipeline': 1},
        'FILES_STORE': str(JOB_OUTPUT_PATH + '/{0}/'.format(job_id)),
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    return settings


# custom itemClass for files purpose only
class CustomScrapyFilesItem(scrapy.Item):
    file_name = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field

# custom file pipeline


class CustomFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for my_url in item.get('file_urls', []):
            yield scrapy.Request(my_url, meta={'file_name': item.get('file_name')})

    def file_path(self, request, response=None, info=None):
        return request.meta['file_name']
