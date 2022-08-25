from app import basic_auth
from flask import request
from flask_restful import Resource
from models import CustomResponse, Status
from repositories import JobRepo

job_repo = JobRepo()


class JobStatusResource(Resource):
    @basic_auth.required
    def get(self):
        try:
            result = job_repo.status(request.args.get('jobId'))
            if result != None:
                res = CustomResponse(Status.SUCCESS.value, result)
                return res.getres()
            else:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400
        except Exception as e:
            print(e)
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400
