import threading
import time
import uuid

import config
from common.elastic_wrapper import Log
from models import AgentUtils


class AgentRepo:
    def __init__(self):
        self.agentUtils = AgentUtils()
        self.activeThreads = []
        self.waitThreads = []

    def list(self, filepath):
        self.agentUtils.filepath = filepath
        result = self.agentUtils.listAgents()
        for agent in result:
            agent.pop('scripts')
        return result

    def waitAndStart(self, agentRunContext, target_script):
        # log waiting state
        log = Log(agentRunContext)
        log.job(config.JOB_RUNNING_STATUS, "JOB in waiting state.")
        del log
        # code to check and run if activeThreads is empty
        while True:
            if len(self.activeThreads) < config.MAX_RUNNING_JOBS:
                self.activeThreads.append(agentRunContext.jobId)
                self.waitThreads.remove(agentRunContext.jobId)
                thread = threading.Thread(target=target_script, args=(
                    agentRunContext,), name=agentRunContext.jobId)
                thread.start()
                # check if thread alive
                while thread.is_alive():
                    time.sleep(10)
                # remove thread after completion
                self.activeThreads.remove(agentRunContext.jobId)
                break
            else:
                time.sleep(10)
        return None

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
                if len(self.waitThreads) < config.MAX_WAITING_JOBS:
                    self.waitThreads.append(agentRunContext.jobId)
                    thread = threading.Thread(target=self.waitAndStart, args=(
                        agentRunContext, agent['scripts'][config.AGENT_SCRIPT_TYPES[agentRunContext.jobType]]), name=str('wait-'+agentRunContext.jobId))
                    thread.start()
                else:
                    return {'message': 'Already many jobs are in Waiting ... Please retry after some time.'}
        if threadStarted:
            return {'jobId': agentRunContext.jobId}
        else:
            return None
