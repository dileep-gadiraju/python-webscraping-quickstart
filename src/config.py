import os

# ------------------server configuration--------------------------

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
SERVER_DEBUG = True
SERVER_CORS = False
SERVER_STATIC_PATH = ''

# API configuration
API_URL_PREFIX = "/api"
BUILD_NUMBER = 'BUILD_NUMBER_001'
API_MANDATORY_PARAMS = ['agentId', 'search', 'type']

# Application configuration
BASIC_HTTP_USERNAME = os.environ.get('BASIC_HTTP_USERNAME')
BASIC_HTTP_PASSWORD = os.environ.get('BASIC_HTTP_PASSWORD')


# ------------------agent configuration---------------------------
# AGENT_SCRIPT_TYPES = { 'JOB_TYPE_1' : 'JOB_TYPE_1_FOLDER', 'JOB_TYPE_2' : 'JOB_TYPE_2_FOLDER' }
AGENT_SCRIPT_TYPES = {
    'INFORMATION': 'info',
    'PDF': 'pdf'
}
# agent configuration file
AGENT_CONFIG_PATH = 'agent_configs/agents.json'
AGENT_CONFIG_PKL_PATH = 'agent_configs/agents.pkl'

# ------------------AzureBlob Variable----------------------------

# AzureBlob variable
BLOB_INTIGRATION = False
BLOB_SAS_TOKEN = os.environ.get('BLOB_SAS_TOKEN')
BLOB_ACCOUNT_URL = os.environ.get('BLOB_ACCOUNT_URL')
BLOB_CONTAINER_NAME = os.environ.get('CONTAINER_NAME')

# ------------------Queuing variables-----------------------------

# Queuing variables
MAX_RUNNING_JOBS = int(os.environ.get('MAX_RUNNING_JOBS', 4))
MAX_WAITING_JOBS = int(os.environ.get('MAX_WAITING_JOBS', 10))

# ------------------ElasticSearch DB variables--------------------

ELASTIC_DB_URL = os.environ.get('ELASTIC_DB_URL')

# ES index variables
ES_LOG_INDEX = 'general-app-logs'
ES_JOB_INDEX = 'general-job-stats'
ES_DATA_INDEX = 'general-crawled-data'

# ------------------Logging variables-----------------------------

JOB_OUTPUT_PATH = "output"
JOB_OUTPUT_PATH = '/'.join(os.getcwd().split('/')[:-1]) + '/' + JOB_OUTPUT_PATH

# JobStatus variables
JOB_RUNNING_STATUS = 'RUNNING'
JOB_COMPLETED_SUCCESS_STATUS = 'COMPLETED_SUCCESS'
JOB_COMPLETED_FAILED_STATUS = 'COMPLETED_FAILED'

# ------------------Driver Variables-------------------------------

CHROMEDRIVER_PATH = 'C:\\Drivers\\chromedriver_win32\\chromedriver.exe'

# -----------------------------------------------------------------
