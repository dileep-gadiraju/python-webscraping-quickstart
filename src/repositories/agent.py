import uuid
from concurrent.futures import ThreadPoolExecutor

import config
from common.elastic_wrapper import Log
from models import AgentUtils


class AgentRepo:
    def __init__(self):
        self.agentUtils = AgentUtils()
        self.executor = ThreadPoolExecutor(max_workers=config.MAX_RUNNING_JOBS)

    def list(self, filepath):
        self.agentUtils.filepath = filepath
        result = self.agentUtils.listAgents()
        for agent in result:
            agent.pop('scripts')
        return result

    def run(self, agentRunContext, filepath):
        threadStarted = False
        agentRunContext.jobId = str(uuid.uuid4())
        self.agentUtils.filepath = filepath
        agents_list = self.agentUtils.listAgents()
        threadStarted = False
        for agent in agents_list:
            if agent['agentId'] == agentRunContext.requestBody['agentId']:
                agentRunContext.URL = agent['URL']
                threadStarted = True
                if self.executor._work_queue.qsize() < config.MAX_WAITING_JOBS:
                    log = Log(agentRunContext)
                    log.job(config.JOB_RUNNING_STATUS, "JOB in waiting state.")
                    del log
                    self.executor.submit(
                        agent['scripts'][config.AGENT_SCRIPT_TYPES[agentRunContext.jobType]], agentRunContext)
                else:
                    return {'message': 'Already many jobs are in Waiting ... Please retry after some time.'}
        if threadStarted:
            return {'jobId': agentRunContext.jobId}
        else:
            return None
