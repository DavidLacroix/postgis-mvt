## Postgis-mvt
Presenting the stack Postgis/Flask/Mapboxgl to display geographic data using vector tiles.

Presentation is hosted here: https://davidlacroix.github.io/postgis-mvt/slide/index.html. The presentation won't be complete without the small infrastructure that comes with it. Follow the instructions to get the whole thing working properly.

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
sudo docker-compose up -d
```
Sudoing docker is not secure but is faster. To setup your docker properly read [this](https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user)

#### Postgres
```sh
# Connect to database
psql -h localhost -p 5555 -d postgres -U postgres
# Access container
sudo docker exec -it postgres-master /bin/bash
```

#### Webapp
```sh
http://localhost:8001
# Access container
sudo docker exec -it webapp-master /bin/bash
```

#### Slides
```sh
http://localhost:8000
# Access container
sudo docker exec -it slide-master /bin/bash
```

### Processing insee data
```sh
sudo docker build -t data-master data-processing/
sudo docker run --link=postgres-master --network=global-network --env-file .env -it data-master
```
