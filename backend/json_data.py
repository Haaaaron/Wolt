import json as JSON
import pandas as pd

def load_as_df(file='restaurants.json'):
    try:
        with open(file, 'r') as json_file:
            data = JSON.load(json_file)
            df = pd.json_normalize(data['restaurants'])
            return df, None
    except OSError as err:
        return None, "JSON file {} not found".format(file)
    except:
        return None, "Error in file format {}".format(file)

def dataframe_to_json(section):
    if (section[1].empty):
        return None

    result = {}
    result['title'] = section[0]
    result['restaurants'] = section[1].to_json(orient="records")
    result['restaurants'] = JSON.loads(result['restaurants'])

    return result