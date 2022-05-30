
# ElasticSearch Log

* Initialize Log object.
```
log = Log(agentRunContext)
```

* Types of logs:
    
    1. log.job : it shows the job status, logs are shown in `general-job-stats`
        
        Syntax:
        ```
        log.job(status, message)
        ```
        
        Examples:
        ```
        log.job(config.JOB_RUNNING_STATUS, 'job Started')
        # your code goes here
        try:
            log.job(config.JOB_COMPLETED_SUCCESS_STATUS, 'Job Completed')
        except:
            log.job(config.JOB_COMPLETED_FAILED_STATUS, 'Job Failed')
        ```

    2. log.info : it shows the job info, logs are shown in `general-app-logs`

        Syntax:
        ```
        log.info(info_type, message)
        ```
        Examples:
        ```
        log.info('info', 'This is generalization project')
        log.info('warning', 'Script is taking more than usual time')
        log.info('exception', 'No Products Available')
        ```
    3. log.data : it shows the job data, logs are shown in `general-acrawled-data`
        
        Syntax:
        ```
        log.data(data)
        ```
        Example:
        ```
        data = {
            "A" : "123",
            "B" : "Generic Project"
        }
        log.data(data)
        ```
