import os
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy

import config
from models import AgentUtils
from utilities import AgentContext
from common import TooManyRequest

AGENTS_PKL_PATH = os.path.join(
    config.SERVER_STATIC_PATH, config.AGENT_CONFIG_PKL_PATH)


class AgentRepo:
    def __init__(self):
        self.agentUtils = AgentUtils()
        self.agentUtils.filepath = AGENTS_PKL_PATH
        self.agent_list = self.agentUtils.listAgents()
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_RUNNING_JOBS)

    def get_agent_data(self, agentId):
        data = None
        for agent in self.agent_list:
            if agent['agentId'] == agentId:
                data = agent
                break
        return data

    def list(self):
        result = deepcopy(self.agent_list)
        result = [{k: v for k, v in agent.items() if v is not None}
                  for agent in result]
        for agent in result:
            agent.pop('scripts')
        return result

    def run(self, req_data):
        output = None
        if self.executor._work_queue.qsize() < config.MAX_WAITING_JOBS:
            agent_data = self.get_agent_data(req_data.get('agentId', None))
            if agent_data is not None:
                agentContext = AgentContext(agent_data, req_data)
                self.executor.submit(
                    agent_data['scripts'][config.AGENT_SCRIPT_TYPES[agentContext.jobType]], agentContext)
                output = {'jobId': agentContext.jobId}
            else:
                pass
        else:
            raise TooManyRequest('Already many jobs are in Waiting ... Please retry after some time.')
        return output
