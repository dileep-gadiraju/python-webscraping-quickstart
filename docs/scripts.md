
# Scripts

1. Create `python_file` in the respective scriptType folder in `./src/scripts`.

2. Format of the script `my_agent_script.py`.
```
# imports

# create a function
def myAgentScript(agentRunContext):
    log = Log(agentRunContext)
    try:
    
        log.job(config.JOB_RUNNING_STATUS, Job Started')

        # Your script
        # Goes here

        log.job(config.JOB_COMPLETED_SUCCESS_STATUS, Successfully Scraped Dats')

    except Exception as e:
        log.job(config.JOB_COMPLETED_FAILED_STATUS, str(e))
        log.info('exception', traceback.format_exc())

```
3. Add script to `init.py` as 
```
from .my_agent_script import myAgentScript
```


