from flask import Flask,jsonify,request
from .discovery_data import by_popularity,by_launch_date,by_distance
from .json_data import load_as_df, dataframe_to_json
import json as JSON
import pandas
import os.path

app = Flask(__name__,instance_relative_config=True)
app.config['JSON_SORT_KEYS'] = False
FILENAME = os.path.join(app.static_folder, 'restaurants.json')

@app.route('/discovery')
def discovery():
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





if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)

