import os
import pickle

from .agent_class import Agent


class AgentUtils:

    def __init__(self):
        self.filepath = None

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

    def __readpklfile(self):
        if os.path.exists(self.filepath):
            file_pi = open(self.filepath, 'rb')
            agent_list = pickle.load(file_pi)
            return agent_list
        else:
            return []

    def __writepklfile(self, agent_list):
        file_pi = open(self.filepath, 'wb')
        pickle.dump(agent_list, file_pi)

    def add_agent(self, agent_data):
        agent = Agent(agent_data)
        agent_list = self.__readpklfile()
        for old_agent in agent_list:
            if old_agent.agent_id == agent.agent_id:
                print('The agent already exists', agent)
                return
        agent_list.append(agent)
        self.__writepklfile(agent_list)

    def list_agents(self):
        return_list = []
        agent_list = self.__readpklfile()
        for old_agent in agent_list:
            agent = {}
            agent['agentId'] = old_agent.agent_id
            agent['description'] = old_agent.description
            agent['provider'] = old_agent.provider
            agent['scripts'] = old_agent.scripts
            agent['URL'] = old_agent.url
            agent['proxy'] = old_agent.proxy
            return_list.append(agent)
        return return_list
