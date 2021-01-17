import json as JSON
import pandas as pd

def load_json(file='restaurants.json'):

    with open(file) as json_file:
        data = JSON.load(json_file)

    return data

def as_dataframe():
    
    json_data = load_json()
    df = pd.json_normalize(json_data['restaurants'])

    return df

def dataframe_to_json(df):

    if (df.empty):
        return None
    result = df.to_json(orient="records")
    parsed = JSON.loads(result)
    
    return JSON.dumps(parsed, indent=4)  



if __name__ == '__main__':
    #data = load(file='not_here.json')
    data = as_dataframe()
    print(data)
    