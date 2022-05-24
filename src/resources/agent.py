import os
import traceback

import config
from app import basic_auth
from common import ValueMissing
from flask import request
from flask_restful import Resource
from models import CustomResponse, Status
from repositories import AgentRepo
from utilities import AgentRunContext

agentRepo = AgentRepo()


def mandatory_param(req):
    e_value = Status.ERR_MISSING_PARAMETERS
    param_list = list()
    for param in config.API_MANDATORY_PARAMS:
        if req.get(param) is None:
            param_list.append(param)
    if len(param_list) > 0:
        return ",".join(param_list), e_value
    else:
        return None, e_value


def check_job_type(req):
    e_value = Status.ERR_INVALID_DATA
    if req.get('type') in config.AGENT_SCRIPT_TYPES.keys():
        return req.get('type'), e_value
    else:
        return None, e_value


class AgentListResource(Resource):
    @basic_auth.required
    def get(self):
        try:
            result = agentRepo.list(os.path.join(
                config.SERVER_STATIC_PATH, config.AGENT_CONFIG_PKL_PATH))
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
            req = request.get_json()
            # check mandatory params
            miss, e_value = mandatory_param(req)
            if miss is not None:
                raise ValueMissing(miss+' - mandatory')

            # check if valid JOB_TYPE
            miss, e_value = check_job_type(req)
            if miss is None:
                raise ValueMissing('invalid type')

            agentRunContext = AgentRunContext(req, miss)
            result = agentRepo.run(agentRunContext, os.path.join(
                config.SERVER_STATIC_PATH, config.AGENT_CONFIG_PKL_PATH))
            if result != None:
                res = CustomResponse(Status.SUCCESS.value, result)
                return res.getres()
            else:
                res = CustomResponse(
                    Status.ERR_GLOBAL_INVALID_DATA.value, "Invalid Agent ID")
                return res.getresjson(), 400
        except Exception as e:
            print(traceback.format_exc())
            res = CustomResponse(e_value.value, str(e))
            return res.getresjson(), 400
