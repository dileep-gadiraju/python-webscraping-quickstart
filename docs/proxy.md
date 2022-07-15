## Proxy Setup

#### Requirements: 
[Squid](https://ubuntu.com/server/docs/proxy-servers-squid)

In Linux, enter the following commands to install Squid

```
sudo apt-get update
sudo apt-get install squid
```

#### To create the basic_auth to protect the proxy server

```
sudo touch /etc/squid/passwords
sudo chmod 777 /etc/squid/passwords
sudo htpasswd -c /etc/squid/passwords [USERNAME]
```

Replace [USERNAME] with your username. You will be prompted for entering the password. Enter and confirm it. 

#### To Test the password store 

`/usr/lib/squid3/basic_ncsa_auth /etc/squid/passwords`

After executing this line the console will look like its hung, there is a prompt without any text in it. 

Enter USERNAME PASSWORD (replacing these with your specific username and password) and hit return. 

You should receive the response "OK".

If not, review the error message, your username/password might be incorrect. Its also possible basic_ncsa_auth is located on a different path (e.g. lib64).

#### To configure the Squid configuration file 
The Squid configuration file is found at `/etc/squid/squid.conf`.

Update the file with below configuration

```
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
#auth_param basic realm Squid proxy-caching web server
auth_param basic realm proxy
auth_param basic credentialsttl 2400 hours
auth_param basic casesensitive off
acl authenticated proxy_auth REQUIRED
http_access allow authenticated
dns_v4_first on
forwarded_for delete
via off
http_access deny all
```

Save the file and exit. Once completed restart the squid service

```
sudo systemctl restart squid
```

---

## Proxy VM Requirement


Server Specification

* Instance Type: Standard B2s (2 vcpus, 4 GiB memory)

* Region : as-required* (eg: Sweden-Central)

>>>Note: A proxy VM needs to be created in the geo-region of agent websites as needed.
---

## Crawler Architectural changes for Geo-restricted websites

#### proxy Configuration

Proxy Configuration lies in `/src/proxy_config.yml`

syntax:

```
proxies:

  # proxy with basic_auth (private proxy)
  COUNTRY1:
    URL: "{IP-ADDR}:{PORT}"
    username: "{BASIC_AUTH_USERNAME}"
    password: "{BASIC_AUTH_PASSWORD}"
    
  # proxy with no_auth (public proxy)
  COUNTRY2:
    URL: "{IP-ADDR}:{PORT}"

```
example:

```
proxies:
  SWEDEN:
    URL: "123.12.12.3:8796"
    username: "XXXX"
    password: "YYYY"
  FINLAND:
    URL: "143.62.12.93:8116"
  NORWAY:
    URL: "12.45.6.1:8080"
    username: "XYZ"
    password: "ABC"

```

#### To set proxy to agent

you can set proxy-server to agent in `/src/static/agent_configs/agents.json`

syntax:

```
[
    {
        "agentId": "AGENT-XYX",
        "description": "Crawler For Xyz",
        "provider": "Xyz",
        "URL": "https://xyz.com",
        "proxy": "COUNTRY",
        "scripts": {
            "info": "Xyzcrawler",
            "pdf": "Xyzcrawler"
        }
    }
]
```
example:

```
[
    {
        "agentId": "RS-SCRAPY",
        "description": "Crawler For RS Components",
        "provider": "RS Components",
        "URL": "https://in.rsdelivers.com",
        "proxy": "FINLAND",
        "scripts": {
            "info": "RSScrapy",
            "pdf": "NoScripts"
        }
    }
]
```

From the above example, agent `MESTRO-SKELLEFTEA-KRAFT` will not use any proxy.
