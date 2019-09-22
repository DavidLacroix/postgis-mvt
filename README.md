## Welcome

Find more at https://davidlacroix.github.io/postgis-mvt/


## Prerequisite
* [Docker](https://www.docker.com/get-started)
* [Docker compose](https://docs.docker.com/compose/install/)

## Getting started
Add your database password in the `.env` file, then:

### Starting services
```sh
sudo docker-compose up -b
```

### Processing data
Running the
```sh
sudo docker build -t data-master data-processing
sudo docker run --link=postgres-master --network=postgis-mvt_default --env-file .env -it data-master
```
