import json
import os
import sys

from flask import Flask
from flask.blueprints import Blueprint
from flask_basicauth import BasicAuth
from flask_cors import CORS

# local imports
import config
import routes
from models import AgentUtils

# flask server
server = Flask(__name__)

# server configuration
config.SERVER_STATIC_PATH = server.static_folder
server.config['BASIC_AUTH_USERNAME'] = config.BASIC_HTTP_USERNAME
server.config['BASIC_AUTH_PASSWORD'] = config.BASIC_HTTP_PASSWORD
# basic_auth for server
basic_auth = BasicAuth(server)

# load agents config
with open(os.path.join(config.SERVER_STATIC_PATH, config.AGENT_CONFIG_PATH), 'r') as f:
    agent_list = json.load(f)

__import__("scripts")
my_scripts = sys.modules["scripts"]

# serialize agent config
agent_utils = AgentUtils()
agent_utils.filepath = os.path.join(
    config.SERVER_STATIC_PATH, config.AGENT_CONFIG_PKL_PATH)
pkl_agent_list = agent_utils.list_agents()
len_diff = len(agent_list) - len(pkl_agent_list)
for i in range(len(agent_list)-1, len(agent_list)-len_diff-1, -1):
    agent = agent_list[i]
    agent_script = dict()
    for type in config.AGENT_SCRIPT_TYPES.values():
        agent_script[type] = my_scripts.__dict__[
            type].__dict__[agent['scripts'][type]]
    agent['scripts'] = agent_script
    agent_utils.add_agent(agent)


# server CORS policy
if config.SERVER_CORS:
    cors = CORS(server, resources={r"/api/*": {"origins": "*"}})

# add blueprint routes to server
for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.API_URL_PREFIX)

# sample route


@server.route('/')
def home():
    return "<h1>HI</h1>"


# start server
if __name__ == "__main__":
    print('starting server at {} at port {}'.format(
        config.SERVER_HOST, config.SERVER_PORT))
    server.run(host=config.SERVER_HOST,
               port=config.SERVER_PORT,
               debug=config.SERVER_DEBUG,
               threaded=True)
