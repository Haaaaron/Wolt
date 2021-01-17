import pandas as pd
import numpy as np
import json_data 
import datetime
from dateutil.relativedelta import *

#r: Mean radius of earth (km). This allows for the smallest error margin. Best would be an area specific radius, but that would be quite hardcore
def spherical_dist(coordinate_1,coordinate_2,r = 6371.0088):

    cos_lat1 = np.cos(coordinate_1[..., 1])
    cos_lat2 = np.cos(coordinate_2[1])
    cos_lat_d = np.cos(coordinate_1[..., 1] - coordinate_2[1])
    cos_lon_d = np.cos(coordinate_1[..., 0] - coordinate_2[0])
    
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))


def by_popularity(df):

    df = df.sort_values(by=['online','popularity'], ascending=False).reset_index()
    df.pop('index')

    return df.head(10)

def by_launch_date(df):

    four_months_ago = datetime.datetime.now() + relativedelta(months=-4)
    dt = pd.to_datetime(four_months_ago)

    #to keep the original datatype we create a mask and a deep copy to not effect the dtypes of the original dataframe
    mask = df.copy()
    mask['launch_date'] = pd.to_datetime(mask['launch_date'])
    mask = mask['launch_date'] > dt

    df = df[mask]
    df = df.sort_values(by=['online',"launch_date"], ascending=False).reset_index()
    df.pop('index')

    return df.head(10)

def by_distance(df, user_coordinates, max_distance=1.5):
    
    #List object as elements are a little tedious to work with hence apply(pd.Series)
    restaurant_coordinates = np.deg2rad(np.array(df['location'].apply(pd.Series)))
    user_coordinates = np.deg2rad(user_coordinates)

    distance = spherical_dist(restaurant_coordinates,user_coordinates)

    df['distance'] = distance
    df = df.sort_values(by=['online',"distance"], ascending=[False,True]).reset_index()
    df.pop('index')

    mask = df['distance'] < max_distance
    df = df[mask]
    df.pop('distance')

    return df.head(10)
