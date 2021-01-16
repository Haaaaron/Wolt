import pandas as pd
import numpy as np
import json_data 
import datetime
from dateutil.relativedelta import *

#Was going to use vectorize but found this better method that handles any length vectors
#r: nominal earth equatorial radius
def spherical_dist(coordinate_1,coordinate_2,r = 3598.75):

    cos_lat1 = np.cos(coordinate_1[..., 0])
    cos_lat2 = np.cos(coordinate_2[..., 0])
    cos_lat_d = np.cos(coordinate_1[..., 0] - coordinate_2[..., 0])
    cos_lon_d = np.cos(coordinate_1[..., 1] - coordinate_2[..., 1])
    
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))


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

def by_distance(df, user_coordinates):
    
    #List object as elements are a little tedious to work with
    #conversion to radians
    restaurant_coordinates = np.deg2rad(np.array(df['location'].apply(pd.Series)))
    user_coordinates = np.deg2rad(user_coordinates)
    print(user_coordinates[...,0])
    distance = spherical_dist(restaurant_coordinates[1],user_coordinates)
    print(distance)






if __name__ == "__main__":
    df = json_data.as_dataframe()

    #df = by_launch_date(df)

    df = by_distance(df,[60.1709,24.941])
    print(df)
