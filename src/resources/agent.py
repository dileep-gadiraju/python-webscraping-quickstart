import os
import traceback

import config
from app import basic_auth
from flask import request
from flask_restful import Resource
from models import CustomResponse, get_status, Status
from repositories import AgentRepo
from common import AgentError

agentRepo = AgentRepo()


class AgentListResource(Resource):
    @basic_auth.required
    def get(self):
        try:
            result = agentRepo.list()
            if result != None:
                res = CustomResponse(Status.SUCCESS.value, result)
                return res.getres()
            else:
                res = CustomResponse(
                    Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
                return res.getresjson(), 400
        except Exception:
            res = CustomResponse(
                Status.ERR_GLOBAL_MISSING_PARAMETERS.value, None)
            return res.getresjson(), 400


class AgentRunResource(Resource):
    @basic_auth.required
    def post(self):
        try:
            req_data = request.get_json()
            result = agentRepo.run(req_data)
            if result != None:
                res = CustomResponse(Status.SUCCESS.value, result)
                return res.getres()
            else:
                raise AgentError("Invalid Agent ID")
        except Exception as e:
            print(traceback.format_exc())
            s_code = 400
            e_class = str(type(e).__name__)
            if e_class == 'TooManyRequest':
                s_code = 429
            res = CustomResponse(get_status(e_class).value, str(e))
            return res.getresjson(), s_code

