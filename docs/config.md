
# Configure config.py

* [Server configuration](#Server-configuration)
* [Agent configuration](#Agent-configuration)
* [AzureBlob configuration](#AzureBlob-configuration)
* [ElasticSearch variables](#ElasticSearch-DB-variables)
* [Logging configuration](#Logging-configuration)

## Server configuration

| Variables             | Type      | Description                       |
| :--------             | :-------  | :-------------------------        |
| `SERVER_HOST`         | `string`  |  host for Server                  |
| `SERVER_PORT`         | `string`  |  port for Server                  |
| `SERVER_DEBUG`        | `bool`    |  debugging for Server             |
| `SERVER_CORS`         | `bool`    |  CORS policy for Server           |
| `SERVER_STATIC_PATH`  | `string`  |  static folder path for Server    |
| `API_URL_PREFIX`      | `string`  |  url prefix for Server            |
| `API_MANDATORY_PARAMS`| `list`    |  mandatory parameters for request |
| `BASIC_HTTP_USERNAME` | `string`  |  username to access Server        |
| `BASIC_HTTP_PASSWORD` | `string`  |  password to access Server        |

## Agent configuration

| Variables              | Type      | Description                                     |
| :--------              | :-------  | :-------------------------                      |
| `AGENT_SCRIPT_TYPES`   | `dict`    |  types of scraping_scripts                      |
| `AGENT_CONFIG_PATH`    | `string`  |  file_path for agent_configuration(json file)   |
| `AGENT_CONFIG_PKL_PATH`| `string`  |  file_path for agent_configuration(pickle file) |

## AzureBlob configuration

| Variables             | Type     | Description                       |
| :--------             | :------- | :-------------------------        |
| `BLOB_INTIGRATION`    | `bool`   |  enable/disable AzureBlob Storage |
| `BLOB_SAS_TOKEN`      | `string` |  SAS Token for AzureBlob Storage  |
| `BLOB_ACCOUNT_URL`    | `string` |  Account URL for AzureBlob Storage|
| `BLOB_CONTAINER_NAME` | `string` |  Container for AzureBlob Storage  |

## ElasticSearch DB variables

| Variables        | Type     | Description                          |
| :--------        | :------- | :-------------------------           |
| `ELASTIC_DB_URL` | `string` |  URL of ElasticSearch Server         |
| `ES_LOG_INDEX`   | `string` |  Info Logging Index in ElasticSearch |
| `ES_JOB_INDEX`   | `string` |  Job  Logging Index in ElasticSearch |
| `ES_DATA_INDEX`  | `string` |  Data Logging Index in ElasticSearch |

## Logging configuration

| Variables                     | Type     | Description                    |
| :--------                     | :------- | :-------------------------     |
| `JOB_OUTPUT_PATH`             | `string` |  folder_path for JOB output    |
| `MAX_RUNNING_JOBS`            | `int`    |  Max No. of Running Jobs       |
| `MAX_WAITING_JOBS`            | `int`    |  Max No. of Waiting Jobs       |
| `JOB_RUNNING_STATUS`          | `string` |  Status for Running Jobs       |
| `JOB_COMPLETED_SUCCESS_STATUS`| `string` |  Status for Successfull Jobs   |
| `JOB_COMPLETED_FAILED_STATUS` | `string` |  Status for Failed Jobs        |
