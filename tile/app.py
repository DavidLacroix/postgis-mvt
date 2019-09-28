import math
import os

import psycopg2
import psycopg2.extras
from flask import Flask, make_response, render_template, request

app = Flask(__name__)

TILE_SCHEMA = 'mvt'
DB_PARAMETERS = {
    'host': 'postgres-master',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': os.environ['POSTGRES_PASSWORD'],
    'cursor_factory': psycopg2.extras.RealDictCursor
}


@app.route("/")
def index():
    return """
        <h1>I shall serve you tiles</h1>
        <img src="https://clevermosaics.com/wp-content/uploads/2018/07/Peel-and-Stick-Tiles-for-Shower-Walls.jpg"/>
    """


@app.route('/<string:layer>/<int:z>/<int:x>/<int:y>', methods=['GET'])
def generic_mvt(layer, z, x, y):
    srid = int(request.args.get('srid', 4326))
    tile = _load_tile(layer, x, y, z, srid=srid)
    response = make_response(tile)
    response.headers.add('Content-Type', 'application/octet-stream')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def _load_tile(layer_name, x, y, z, srid=4326):
    tile = None

    # Generic query to select data from postgres
    query = '''
        SELECT ST_AsMVT(tile, %(layer_name)s, 4096, 'mvt_geom') AS mvt
        FROM (
            SELECT id,
                value,
                ST_AsMVTGeom(
                    -- Geometry from table
                    ST_Transform(t.geom, 3857),
                    -- MVT tile boundary
                    ST_Makebox2d(
                        -- Lower left coordinate
                        ST_Transform(ST_SetSrid(ST_MakePoint(%(xmin)s, %(ymin)s), 4326), 3857),
                        -- Upper right coordinate
                        ST_Transform(ST_SetSrid(ST_MakePoint(%(xmax)s, %(ymax)s), 4326), 3857)
                    ),
                    -- Extent
                    4096,
                    -- Buffer
                    256,
                    -- Clip geom
                    TRUE
                ) AS mvt_geom
            FROM {schema}.{table_name} t
            WHERE
                t.geom
                && ST_Makebox2d(
                    ST_Transform(ST_SetSrid(ST_MakePoint(%(xmin)s, %(ymin)s), 4326), %(srid_bbox)s),
                    ST_Transform(ST_SetSrid(ST_MakePoint(%(xmax)s, %(ymax)s), 4326), %(srid_bbox)s)
                )
        ) AS tile
    '''.format(
        schema=TILE_SCHEMA,
        table_name=layer_name,
    )

    # Transform TMS to BBOX
    xmin, ymin, xmax, ymax = _tms2bbox(x, y, z)

    query_parameters = {
        'layer_name': layer_name,
        'xmin': xmin,
        'ymin': ymin,
        'xmax': xmax,
        'ymax': ymax,
        'srid_bbox': srid,
        'srid_geom': 3857
    }

    with psycopg2.connect(**DB_PARAMETERS) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, query_parameters)
            res = cursor.fetchone()
            if 'mvt' in res and res['mvt'] is not None:
                tile = bytes(res['mvt'])

    return tile


def _tms2bbox(x, y, z):
        '''
            Convert a tile coordinate into a WGS84 bounding box.
            Ex: (0, 1, 1) => (-180.0, 0.0, 0.0, -85.0511287798066)
            :param x: horizontal tile index on the TMS grid
            :param y: vertical tile index on the TMS grid
            :param z: zoom index on the TMS grid
            :return: WGS84 bounding box as a tuple (minlon, minlat, maxlon, maxlat)
        '''
        xmin, ymin = _tms2ll(x, y, z)
        xmax, ymax = _tms2ll(x + 1, y + 1, z)

        return (xmin, ymin, xmax, ymax)


def _tms2ll(x, y, z):
    '''
        Convert a tile coordinate into a WGS84 coordinate.
        Ex: (0, 1, 1) => (-180.0, 0.0)
        :param x: horizontal tile index on the TMS grid
        :param y: vertical tile index on the TMS grid
        :param z: zoom index on the TMS grid
        :return: WGS84 coordinates as a tuple (lon, lat)
    '''
    n = 2.0 ** z
    lon_deg = x / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / n)))
    lat_deg = math.degrees(lat_rad)
    return lon_deg, lat_deg


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
