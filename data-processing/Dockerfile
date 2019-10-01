FROM mdillon/postgis:latest

RUN apt-get update \
    && apt-get install -y gdal-bin wget zip p7zip-full \
    && apt-get autoremove -y \
    && apt-get clean all

ADD . .

ENTRYPOINT ./run.sh
