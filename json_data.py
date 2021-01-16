import json
import pandas as pd

def load_json(file='restaurants.json'):

    with open(file) as json_file:
        data = json.load(json_file)

    return data

def as_dataframe():
    
    json_data = load_json()
    df = pd.json_normalize(json_data['restaurants'])

    return df






if __name__ == '__main__':
    #data = load(file='not_here.json')
    data = as_dataframe()
    print(data)
    