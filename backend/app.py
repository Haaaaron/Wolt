import os
import sys

from flask import Flask,jsonify,request
from flask_caching import Cache

#Depends if file is being run directly
#Ugly work around
try:
    from .discovery_data import by_popularity,by_launch_date,by_distance
    from .json_data import load_as_df, dataframe_to_json
except:
    from discovery_data import by_popularity,by_launch_date,by_distance
    from json_data import load_as_df, dataframe_to_json
    pass

import json as JSON
import pandas
import os.path

cache_config = {
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 100
}

app = Flask(__name__,instance_relative_config=True)
app.config['JSON_SORT_KEYS'] = False
app.config.from_mapping(cache_config)
cache = Cache(app)
FILENAME = os.path.join(app.static_folder, 'restaurants.json')

@app.route('/discovery')
#@cache.cached(timeout=50)
def generate_endpoint():
    """ Generates restaurant json endpoint based on three criteria.

    1. popularity: discovery_data.by_popylarity
    2. launch date: discover_data.by_launch_date
    3. distance from user: discovery_data.by_distance
    
    Loads based on two query parameters users latitude and longitude [lat,lon] as numbers.
    """
    restaurants, err = load_as_df(file=FILENAME)

    if restaurants is None:
        error = {
            "error": str(err)
        } 
        return jsonify(error), 400

    try:
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        lat = float(lat)
        lon = float(lon)
        user_coordinates = [lon,lat]
    except TypeError as err:
        error = {
            "error": "'lat'=='{0}' and/or 'lon'=='{1}' query parameters unspecified".format(lat,lon)
        }
        return jsonify(error), 400
    except ValueError as err:
        error = {
            "error": "'lat'=='{0}' and/or 'lon'=='{1}' must be number".format(lat,lon)
        }
        return jsonify(error), 400

    result = {
        "sections":[("Popular restaurants",by_popularity(restaurants)),
                    ("New Restaurants",by_launch_date(restaurants)), 
                    ("Nearby Restaurants", by_distance(restaurants, user_coordinates))
        ]
    }

    for i,section in enumerate(result['sections']):
        result['sections'][i] = dataframe_to_json(section)
    
    result['sections'] = [not_null for not_null in result['sections'] if not_null]

    return jsonify(result)


#This chunk is irrelevant since relative imports don't work if app.py is run directly
if __name__ == '__main__':
    port = int(os.environ['PORT']) or 5000   
    host = os.environ['HOST'] or '127.0.0.1'

    app.run(debug=True, use_debugger=True, use_reloader=True, host=host, port=port)
