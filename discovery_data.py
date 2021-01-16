import pandas as pd
import json_data 
import datetime
from dateutil.relativedelta import *

def by_popularity(df):

    #First we sort by online status then by popularity
    df = df.sort_values(by=['online','popularity'], ascending=False).reset_index()

    return df.head(10)

def by_launch_date(df):

    four_months_ago = datetime.datetime.now() + relativedelta(months=-4)
    dt = pd.to_datetime(four_months_ago)

    #to keep the original datatype we create a mask
    dt_mask = df
    dt_mask['launch_date'] = pd.to_datetime(dt_mask['launch_date'])
    dt_mask = dt_mask['launch_date'] > dt

    df = df[dt_mask]
    df = df.sort_values(by=['online',"launch_date"], ascending=False).reset_index()

    return df.head(10)
def atleast_one(df):
    return None

if __name__ == "__main__":
    df = json_data.as_dataframe()

    df = by_launch_date(df)
    print(df)
