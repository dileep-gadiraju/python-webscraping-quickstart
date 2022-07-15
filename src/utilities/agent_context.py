import os
import uuid
from datetime import datetime as dt

import config
from common import ParamMissing, FormatError, BlobStorage, Log


class AgentContext(object):

    def __init__(self, agent_data, req_body):
        self.jobId = str(uuid.uuid4())
        self.requestBody = req_body
        self.jobType = self.requestBody['type']
        self.agentId = agent_data['agentId']
        self.URL = agent_data['URL']
        self.proxy = agent_data.get('proxy', None)
        self.log = Log(self)
        self.blobStorage = None

    @property
    def requestBody(self):
        return self._requestBody

    @requestBody.setter
    def requestBody(self, value):
        param_list = list()
        for param in config.API_MANDATORY_PARAMS:
            if value.get(param) is None:
                param_list.append(param)
        if len(param_list) > 0:
            miss = ",".join(param_list)
            raise ParamMissing('mandatory parameters required - '+miss)
        else:
            self._requestBody = value

    @property
    def jobType(self):
        return self._jobType

    @jobType.setter
    def jobType(self, value):
        if value in config.AGENT_SCRIPT_TYPES.keys():
            self._jobType = value
        else:
            raise ValueError('Invalid JobType - Valid JobTypes : ' +
                             str(config.AGENT_SCRIPT_TYPES.keys()))

    @property
    def blobStorage(self):
        return self._blobStorage

    @blobStorage.setter
    def blobStorage(self, value):
        if self.jobType != "PDF":
            self._blobStorage = value
        else:
            blob_var = BlobStorage(self.reBlob)
            folder = str(self.agentId).lower().replace(
                'generic-', '').replace('-', ' ')
            blob_var.set_agent_folder(folder)
            self._blobStorage = blob_var

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        value.job(config.JOB_RUNNING_STATUS, "JOB in waiting state.")
        self._log = value
