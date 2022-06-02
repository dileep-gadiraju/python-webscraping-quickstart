
class AgentRunContext(object):

    def __init__(self, req, jobType):
        self.requestBody = req
        self.jobId = None
        self.URL = None
        self.jobType = jobType

    @property
    def jobId(self):
        return self._jobId

    @jobId.setter
    def jobId(self, value):
        self._jobId = value

    @property
    def requestBody(self):
        return self._requestBody

    @requestBody.setter
    def requestBody(self, value):
        self._requestBody = value

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, value):
        self._URL = value

    @property
    def jobType(self):
        return self._jobType

    @jobType.setter
    def jobType(self, value):
        self._jobType = value
