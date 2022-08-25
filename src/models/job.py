from common import Log


class JobModel(object):

    def status(self, job_id):
        '''
            connect to ES DB and get the status of job_id
        '''
        log = Log.from_default()
        return log.get_status(job_id)
