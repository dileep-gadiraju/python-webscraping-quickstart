import config
from elasticsearch import Elasticsearch
import json
import time


class Log(object):

    @classmethod
    def from_default(cls):
        return cls(None)

    def __init__(self, agentRunContext):
        self.agentRunContext = agentRunContext
        self.es_client = Elasticsearch([config.ELASTIC_DB_URL],ca_certs=config.ELASTIC_DB_CERT,verify_certs=False, basic_auth=[config.ELASTIC_DB_USERNAME, config.ELASTIC_DB_PASSWORD])

    def __populate_context(self):
        data = {
            'agentId': self.agentRunContext.requestBody['agentId'],
            'jobId': self.agentRunContext.jobId,
            'jobType': self.agentRunContext.jobType,
            'timestamp': int(time.time()*1000),
            'buildNumber': config.BUILD_NUMBER
        }
        return data

    def __index_data_to_es(self, index, data):
        if self.es_client.ping():
            self.es_client.index(index=index, body=json.dumps(data))
        else:
            with open('logger.txt', 'a+') as f:
                f.write(json.dumps(data)+'\n')

    def info(self, info_type, message):
        info_data = self.__populate_context()
        info_data['type'] = info_type
        info_data['message'] = message
        self.__index_data_to_es(config.ES_LOG_INDEX, info_data)

    def data(self, data):
        data.update(self.__populate_context())
        self.__index_data_to_es(config.ES_DATA_INDEX, data)

    def job(self, status, message):
        job_data = self.__populate_context()
        job_data['status'] = status
        job_data['message'] = message
        self.__index_data_to_es(config.ES_JOB_INDEX, job_data)

    def get_status(self, jobId):
        print(jobId)
        if not self.es_client.ping():
            return {'status': 'ES_CONNECTION_FAILED', 'message': "Not able to connect to ES DB"}
        else:
            search_param = {
                "sort": [
                    {
                        "timestamp": {
                            "order": "desc"
                        }
                    }
                ],
                "query": {
                    "bool": {
                        "must": [
                            {"match": {
                                "jobId.keyword": jobId
                            }}
                        ]
                    }
                }
            }
            res = self.es_client.search(
                index=config.ES_JOB_INDEX, body=search_param)

            if len(res['hits']['hits']) > 0:
                source = res['hits']['hits'][0]['_source']
                return {'status': source['status'], 'message': source['message']}
            else:
                return {'status': 'JOBID_NOT_FOUND', 'message': "Please check the given jobId"}
