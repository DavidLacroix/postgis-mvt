## Welcome

## Prerequisite
* [Docker](https://www.docker.com/get-started)
* [Docker compose](https://docs.docker.com/compose/install/)

## Getting started
Add your variables in the `.env` file:
* postgres password
* mapbox token 

Then:

### Starting services
```sh
sudo docker-compose up -b
```

### Processing insee data
```sh
sudo docker build -t data-master data-processing/
sudo docker run --link=postgres-master --network=global-network --env-file .env -it data-master
```
