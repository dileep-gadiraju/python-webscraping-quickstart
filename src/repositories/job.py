from models import JobModel


class JobRepo:
    def __init__(self):
        self.job_model = JobModel()

    def status(self, job_id):
        return self.job_model.status(job_id)
