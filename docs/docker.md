# Docker Deployment

* Stop and remove existing containers with name `web-scraping-project`.
```
docker stop web-scraping-project 
docker rm web-scraping-project
```

* Build Docker image: `web-scraping-project`
```
docker build -t web-scraping-project ./src/
```
_Note: ./src/ contains Dockerfile_


* Spawn: `web-scraping-project`.
```
docker run --name web-scraping-project -p 5001:5001 --env-file ./deploy/dev.env -it web-scraping-project
```

_Note: Here environment file (--env-file) refers from local storage_