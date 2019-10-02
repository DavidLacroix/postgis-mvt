#!/bin/bash

set -eux

WORKDIR=/
mkdir -p $WORKDIR 

DB_HOST='postgres-master'
DB_PORT='5432'
DB_NAME='postgres'
DB_USER='postgres'
export PGPASSWORD=$POSTGRES_PASSWORD

# Testing database connection
psql -v ON_ERROR_STOP=1 -P pager=off -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -c "SELECT TRUE AS connection"

# Load geojson in postgres
ogr2ogr --config PG_USE_COPY YES \
	-gt 1000 \
	-progress \
	-t_srs EPSG:4326 \
	-f "PostgreSQL" PG:"host=$DB_HOST port=$DB_PORT user=$DB_USER dbname=$DB_NAME password=$PGPASSWORD" \
	-nln public.apur_building_raw \
    -overwrite \
	-nlt MULTIPOLYGON \
	data/apur.geojson OGRGeoJSON

# Initialise a schema to store visualisation tables
psql -v ON_ERROR_STOP=1 -P pager=off -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -c """
    CREATE SCHEMA IF NOT EXISTS mvt;
"""

# Use view to allow a table to be displayed
psql -v ON_ERROR_STOP=1 -P pager=off -h $DB_HOST -p $DB_PORT -d $DB_NAME -U $DB_USER -c """
    DROP VIEW IF EXISTS mvt.apur_building;
    CREATE OR REPLACE VIEW mvt.apur_building AS
    SELECT ogc_fid as id,
        -- totally not accurate (but it'll do)
        (regexp_match(c_perconst, '[0-9]{4}'))[1]::integer AS value,
        h_med::integer AS extrude,
        wkb_geometry as geom
    FROM public.apur_building_raw
    ;
"""
