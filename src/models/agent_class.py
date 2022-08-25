class Agent(object):
    def __init__(self, agent_data):
        self.provider = agent_data['provider']
        self.description = agent_data['description']
        self.agent_id = agent_data['agentId']
        self.url = agent_data['URL']
        self.scripts = agent_data['scripts']
        self.proxy = agent_data.get('proxy', None)

    @property
    def agent_id(self):
        return self._agent_id

    @agent_id.setter
    def agent_id(self, value):
        self._agent_id = value

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
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy = value

    def __str__(self):
        str_1 = 'id: {0} , description: {1} , provider: {2} , scripts: {3} , URL: {4} , Proxy: {5}'
        str_1 = str_1.format(self.agent_id, self.description,
                             self.provider, self.scripts, self.url, self.proxy)
        return str_1
