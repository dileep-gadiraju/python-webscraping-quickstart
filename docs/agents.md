
# Agent Configurations

To include new agents, add the agent_data to `/static/agents.json`

format: 

```
    {
        "agentId": "MY-AGENT-1",
        "description": "Crawler For my_agent_1",
        "provider": "AGENT-PROVIDER-X",
        "URL": "https://www.my-agent.com",
        "scripts": {
            "scriptType1": "myAgentScript1",
            "scriptType2": "myAgentScript2",
            "scriptType3": "myAgentScript3",
            ...
        }
    }
```

example: 

```
    [
        {
            "agentId": "APPLIED-SELENIUM",
            "description": "Crawler For Applied",
            "provider": "Applied",
            "URL": "https://www.applied.com",
            "scripts": {
                "info": "AppliedSelenium",
                "pdf": "AppliedSelenium"
            }
        },
        {
            "agentId": "GRAINGER-SELENIUM",
            "description": "Crawler For Grainger",
            "provider": "Grainger",
            "URL": "https://www.grainger.com",
            "scripts": {
                "info": "GraingerSelenium",
                "pdf": "GraingerSelenium"
            }
        }
    ]
```