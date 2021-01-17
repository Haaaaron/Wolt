from flask import Flask,jsonify,request
from discovery_data import by_popularity,by_launch_date,by_distance
import json_data
import json as JSON
import pandas

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/discovery')
def hello_world():

    restaurants, succeeded, err = json_data.load_json()

    if not succeeded:

        error = {
            "error": str(err)
        } 

        return jsonify(error), 400

    try:

        lat = request.args.get('lat')
        lon = request.args.get('lon')
        lat = float(lat)
        lon = float(lon)

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

    #deep copy since the structure of the df is changed
    nearby_restaurants = by_distance(restaurants.copy(), [lon,lat])
    popular_restaurants = by_popularity(restaurants)
    new_restaurants = by_launch_date(restaurants)

    result = {}
    result['sections'] = [("Popular restaurants",popular_restaurants),("New Restaurants",new_restaurants), ("Nearby Restaurants",nearby_restaurants)]

    for i,section in enumerate(result['sections']):
        result['sections'][i] = json_data.dataframe_to_json(section)
    
    result['sections'] = [not_null for not_null in result['sections'] if not_null]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)

