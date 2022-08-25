import uuid

import config
from common import ParamMissing, BlobStorage, Log


class AgentContext(object):

    def __init__(self, agent_data, req_body):
        self.job_id = str(uuid.uuid4())
        self.request_body = req_body
        self.job_type = self.request_body['type']
        self.agent_id = agent_data['agentId']
        self.url = agent_data['URL']
        self.proxy = agent_data.get('proxy', None)
        self.log = Log(self)
        self.blob_storage = None

    @property
    def request_body(self):
        return self._request_body

    @request_body.setter
    def request_body(self, value):
        param_list = list()
        for param in config.API_MANDATORY_PARAMS:
            if value.get(param) is None:
                param_list.append(param)
        if len(param_list) > 0:
            miss = ",".join(param_list)
            raise ParamMissing('mandatory parameters required - '+miss)
        else:
            self._request_body = value

    @property
    def job_type(self):
        return self._job_type

    @job_type.setter
    def job_type(self, value):
        if value in config.AGENT_SCRIPT_TYPES.keys():
            self._job_type = value
        else:
            raise ValueError('Invalid JobType - Valid JobTypes : ' +
                             str(config.AGENT_SCRIPT_TYPES.keys()))

    @property
    def blob_storage(self):
        return self._blob_storage

    @blob_storage.setter
    def blob_storage(self, value):
        if self.job_type != "PDF":
            self._blob_storage = value
        else:
            blob_var = BlobStorage(self.re_blob)
            folder = str(self.agent_id).lower().replace(
                'generic-', '').replace('-', ' ')
            blob_var.set_agent_folder(folder)
            self._blob_storage = blob_var

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        value.job(config.JOB_RUNNING_STATUS, "JOB in waiting state.")
        self._log = value
