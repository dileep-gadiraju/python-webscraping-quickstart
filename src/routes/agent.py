from flask import Blueprint
from flask_restful import Api
from resources import AgentListResource, AgentRunResource

AGENT_BLUEPRINT = Blueprint("agent", __name__)

Api(AGENT_BLUEPRINT).add_resource(
    AgentListResource, "/agents"
)

Api(AGENT_BLUEPRINT).add_resource(
    AgentRunResource, "/run"
)
