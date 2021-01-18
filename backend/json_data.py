import json as JSON
import pandas as pd
import sys

def load_as_df(file='restaurants.json'):
    """ Loads .json file into pandas DataFrame
    
    Keyword arguments:
    file -- json file
    """
    try:
        with open(file, 'r') as json_file:
            data = JSON.load(json_file)
            df = pd.json_normalize(data['restaurants'])
            return df, None
    except OSError as err:
        return None, "JSON file {} not found".format(file)
    except KeyError as err:
        return None, "Key:{} not found in JSON file".format(err)
    except:
        return None, sys.exc_info()[1]

def dataframe_to_json(section):
    """ Converts tuple to JSON 

    Keyword arguments:
    section -- tuple: ('example title', pandas.DataFrame)
    """
    if (section[1].empty):
        return None
        
    result = {}
    result['title'] = section[0]
    result['restaurants'] = section[1].to_json(orient="records")
    result['restaurants'] = JSON.loads(result['restaurants'])

    return result