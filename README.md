



# python-webscraping-quickstart

Python based Web-scraping Quick Start Project. 


For Scraping the project uses Selenium & Scrapy framework.


## Setup

* Clone this repositary 
```
 git clone "https://github.com/dileep-gadiraju/python-webscraping-quickstart"
```

* After cloning, Install python packages by running the following command from `./src`.
```
pip install -r "requirements.txt"
```

* Start ElasticSearch,Kibana services as docker-containers.
    
    (refer: https://www.elastic.co/guide/en/kibana/current/docker.html)

* Import API-collections from `./test` for REST client tool.

* Set required global variables

* Run below command from `./src` to start the Server.
```
python app.py
```
Successful local deployment should show Server is up on port 5001.
## Documentation


For Scripting and configuration documentation, refer [Documentation](docs/README.md). 


## API Reference

#### Get all Agents

```
 GET /api/agents
```
_No paramenters Required_

#### Start a Scraping Job

```
  POST /api/run
```
_The following are mandatory Request Body Parameters_
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `agentId` | `string` | `Valid AGENT-ID`                  |
| `type`    | `string` | `Valid Type Of JOB`               |
| `search`  | `string` | `my search query`                 |


#### Get Job Status

```
 GET /api/status
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `JobId`   | `string` | `(required) uuid of a job`        |


### API Authorization

Currently the projects uses basic aurthorization for authentication.

Set the following environment_variable:
| Variables             | Type     | Description                        |
| :--------             | :------- | :--------------------------------  |
| `BASIC_HTTP_USERNAME` | `string` |  username for server               |
| `BASIC_HTTP_PASSWORD` | `string` |  password for server               |



## Authors

- [@dileep-gadiraju](https://github.com/dileep-gadiraju)
- [@Pushkar-Chauhan](https://github.com/Pushkar191098)
- [@dhiru579](https://github.com/dhiru579)
- [@ArchakGAmruth](https://github.com/ArchakGAmruth)

