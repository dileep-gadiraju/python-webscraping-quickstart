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
                    Status.FAILURE.value, None)
                return res.getresjson(), 400
        except Exception:
            res = CustomResponse(
                Status.FAILURE.value, None)
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
                res = CustomResponse(
                    Status.ERR_INVALID_DATA.value, "Invalid Agent ID")
                return res.getresjson(), 400
        except Exception as e:
            print(traceback.format_exc())
            e_class = str(type(e).__name__)
            res = CustomResponse(get_status(e_class).value, str(e))
            return res.getresjson(), 400
