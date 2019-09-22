#!/bin/bash

set -eux

WORKDIR=~
mkdir -p $WORKDIR 

DB_HOST='postgres-master'
DB_PORT='5432'
DB_NAME='postgres'
DB_USER='postgres'
export PGPASSWORD=$POSTGRES_PASSWORD

# Testing database connection
psql -v ON_ERROR_STOP=1 -P pager=off -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -c "SELECT TRUE AS connection"

# Download, unzip insee carreaux 2019
wget "https://www.insee.fr/fr/statistiques/fichier/4176290/Filosofi2015_carreaux_200m_shp.zip" -P $WORKDIR
unzip $WORKDIR/Filosofi2015_carreaux_200m_shp.zip -d $WORKDIR
7z e $WORKDIR/Filosofi2015_carreaux_200m_metropole_shp.7z -o$WORKDIR

ogr2ogr --config PG_USE_COPY YES \
	-gt 1000 \
	-progress \
	-t_srs EPSG:2154 \
	-f "PostgreSQL" PG:"host=$DB_HOST port=$DB_PORT user=$DB_USER dbname=$DB_NAME password=$PGPASSWORD" \
	-nln public.carreaux_raw \
	-nlt MULTIPOLYGON \
	$WORKDIR/Filosofi2015_carreaux_200m_metropole.shp

