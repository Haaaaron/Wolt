import json as JSON
import pandas as pd

def load_json(file='restaurants.json'):

    try:
        with open(file, 'r') as json_file:
            data = JSON.load(json_file)
            df = pd.json_normalize(data['restaurants'])
            return df, True, None
    except OSError as err:
        return None, False, "JSON file not found"
    except:
        return None, False, "Error in file format {0}".format(file)



def to_dataframe():
    
    df = pd.json_normalize(json_data['restaurants'])

    return df

def dataframe_to_json(section):

    if (section[1].empty):
        return None

    result = {}
    result['title'] = section[0]
    result['restaurants'] = section[1].to_json(orient="records")
    result['restaurants'] = JSON.loads(result['restaurants'])

    return result