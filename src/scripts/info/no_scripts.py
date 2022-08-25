import config

def no_scripts(agentcontext):
    agentcontext.log.job(config.JOB_COMPLETED_SUCCESS_STATUS,
                         'Script Not Available')
