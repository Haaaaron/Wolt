from flask import Flask,render_template,jsonify,request,make_response
import json_data
import discovery_data
import json 
import pandas

app = Flask(__name__)

restaurants_df = json_data.as_dataframe()

@app.route('/discovery')
def hello_world():

    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    
    popular_restaurants = discovery_data.by_popularity(restaurants_df)
    new_restaurants = discovery_data.by_launch_date(restaurants_df)
    return "Hello"

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)