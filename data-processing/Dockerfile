FROM geodata/gdal:latest

RUN apt-get update \
    && apt-get install -y postgresql-client zip p7zip-full \
    && apt-get autoremove -y \
    && apt-get clean all

ADD . .

ENTRYPOINT ./load_insee.sh
