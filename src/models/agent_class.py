class Agent(object):
    def __init__(self, agentData):
        self.provider = agentData['provider']
        self.description = agentData['description']
        self.agentId = agentData['agentId']
        self.URL = agentData['URL']
        self.scripts = agentData['scripts']
        self.proxy = agentData.get('proxy', None)

    @property
    def agentId(self):
        return self._agentId

    @agentId.setter
    def agentId(self, value):
        self._agentId = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, value):
        self._provider = value

    @property
    def scripts(self):
        return self._scripts

    @scripts.setter
    def scripts(self, value):
        self._scripts = value

    @property
    def URL(self):
        return self._URL

    @URL.setter
    def URL(self, value):
        self._URL = value

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy = value

    def __str__(self):
        str_1 = 'id: {0} , description: {1} , provider: {2} , scripts: {3} , URL: {4} , Proxy: {5}'
        str_1 = str_1.format(self.agentId, self.description,
                             self.provider, self.scripts, self.URL, self.proxy)
        return str_1
