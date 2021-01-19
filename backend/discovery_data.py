"""
Sorting and calculation module for discovery data
"""

import datetime
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta


def spherical_distance(coordinate_1, coordinate_2, radius=6371.088):
    """ Generates distance between coordinates based on Great-circle distance:
    https://en.wikipedia.org/wiki/Great-circle_distance

    This formula is computationally accurate at short distances.

    Keyword arguments:

    coordinate_1 -- vector of size n, restaurant coordinates
    coordinate_2 -- vector of size 1, user coordinates
    radius -- mean radius of earth for highest accuracy

    """
    cos_lat1 = np.cos(coordinate_1[..., 1])
    cos_lat2 = np.cos(coordinate_2[1])
    cos_lat_d = np.cos(coordinate_1[..., 1] - coordinate_2[1])
    cos_lon_d = np.cos(coordinate_1[..., 0] - coordinate_2[0])

    return radius * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))


def by_popularity(df_original):
    """Returns max top ten popular restaurants as pandas Dataframe

    Keyword arguments:

    df_original: dataframe of given restaurants
    dataframe is copied so as not to effect the original dtypes
    """
    df = df_original.copy()

    df = df.sort_values(by=['online', 'popularity'],
                        ascending=False).reset_index()
    df.pop('index')

    return df.head(10)


def by_launch_date(df_original):
    """Returns max top ten newest restaurants as pandas Dataframe

    Keyword arguments:

    df_original: dataframe of given restaurants
    dataframe is copied so as not to effect the original dtypes
    """
    df = df_original.copy()

    four_months_ago = datetime.datetime.now() + relativedelta(months=-4)
    dt = pd.to_datetime(four_months_ago)

    mask = df.copy()
    mask['launch_date'] = pd.to_datetime(mask['launch_date'])
    mask = mask['launch_date'] > dt

    df = df[mask]
    df = df.sort_values(by=['online', "launch_date"],
                        ascending=False).reset_index()
    df.pop('index')

    return df.head(10)


def by_distance(df_original, user_coordinates, max_distance=1.5):
    """Returns max top ten nearest restaurants as pandas Dataframe

    Keyword arguments:

    df_original: dataframe of given restaurants
    dataframe is copied so as not to effect the original dtypes
    """
    df = df_original.copy()

    # List object as elements are a little tedious to work with hence apply(pd.Series)
    restaurant_coordinates = np.array(df['location'].apply(pd.Series))
    restaurant_coordinates = np.deg2rad(restaurant_coordinates)
    user_coordinates = np.deg2rad(user_coordinates)

    distance = spherical_distance(restaurant_coordinates, user_coordinates)

    df['distance'] = distance
    df = df.sort_values(by=['online', "distance"], ascending=[
                        False, True]).reset_index()
    df.pop('index')

    mask = df['distance'] < max_distance
    df = df[mask]
    df.pop('distance')

    return df.head(10)
