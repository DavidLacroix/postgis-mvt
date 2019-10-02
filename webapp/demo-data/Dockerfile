FROM mdillon/postgis:latest

RUN apt-get update \
    && apt-get install -y gdal-bin wget zip p7zip-full \
    && apt-get autoremove -y \
    && apt-get clean all

ADD . .

# Waits for (see WAITS_FOR in docker-compose.yml)
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

ENTRYPOINT /wait && ./run.sh
