import os
import sys
TESTFILE = os.path.join(os.path.dirname(__file__), "./static/restaurants.json")
TESTFILE_POPULARITY = os.path.join(os.path.dirname(__file__), "./static/test_popularity.json")
TESTFILE_POPULARITY = os.path.join(os.path.dirname(__file__), "./static/testasdf_popularity.json")
TESTFILE_LAUNCH_DATE = os.path.join(os.path.dirname(__file__), "./static/test_launch_date.json")
TESTFILE_DISTANCE = os.path.join(os.path.dirname(__file__), "./static/test_distance.json")

TOPDIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(TOPDIR)

import unittest
import datatest as dt
import numpy as np
import numpy.testing as npt
import pandas as pd
import pandas.testing as pdt
import random
from backend.discovery_data import *
from backend.json_data import *

def setUpModule():    
    global df_test
    global df_test_popularity
    global df_test_launch_date
    global df_test_distance

    succeeded = np.empty(4,dtype=object)
    df_test, succeeded[0] = load_as_df(file = TESTFILE)
    df_test_popularity, succeeded[1] = load_as_df(file = TESTFILE_POPULARITY)
    df_test_launch_date, succeeded[2] = load_as_df(file = TESTFILE_LAUNCH_DATE)
    df_test_distance, succeeded[3] = load_as_df(file = TESTFILE_DISTANCE)

class DiscoveryTest(unittest.TestCase):

    def test_spherical_dist(self):
        location_1 = np.deg2rad([24.9412,60.1709])
        location_2 = np.deg2rad([24.9432,60.1698])
        correct_dist =   0.165

        result = spherical_dist(location_1,location_2)
        self.assertAlmostEqual(result,correct_dist,places=3)

    def test_arbitrary_vector_input(self):
        n = random.randint(1,100)
        location_1 = np.deg2rad([24.9412,60.1709])
        location_2 = np.deg2rad([24.9432,60.1698])
        location_2 = np.tile(location_2,(n,1))
        correct_dist = np.tile( 0.1649205,(n))

        result = spherical_dist(location_1,location_2)
        self.assertIsNone(npt.assert_almost_equal(result,correct_dist))

    def test_dtype(self):

        if df_test is None:
            falure_string = "{} not found".format(TESTFILE)
            self.fail(falure_string)
            return

        df_popularity = by_popularity(df_test)
        df_launch_date = by_launch_date(df_test)
        df_distance = by_distance(df_test,[24.9412,60.1709])

        self.assertIsNone(pdt.assert_series_equal(df_test.dtypes,df_popularity.dtypes))
        self.assertIsNone(pdt.assert_series_equal(df_test.dtypes,df_launch_date.dtypes))
        self.assertIsNone(pdt.assert_series_equal(df_test.dtypes,df_distance.dtypes))

    def test_by_popularity(self):
        df_popularity = by_popularity(df_test)

        if df_test_popularity is None:
            falure_string = "{} not found".format(TESTFILE_POPULARITY)
            self.fail(falure_string)
            return

        self.assertIsNone(pdt.assert_frame_equal(df_popularity,df_test_popularity))

    def test_by_launch_date(self):
        df_launch_date = by_launch_date(df_test)

        if df_test_launch_date is None:
            falure_string = "{} not found".format(TESTFILE_LAUNCH_DATE)
            self.fail(falure_string)
            return
            
        self.assertIsNone(pdt.assert_frame_equal(df_launch_date,df_test_launch_date))
    
    def test_by_distance(self):
        df_distance = by_distance(df_test,[24.9412,60.1709])

        if df_test_distance is None:
            falure_string = "{} not found".format(TESTFILE_POPULARITY)
            self.fail(falure_string)
            return
            
        self.assertIsNone(pdt.assert_frame_equal(df_distance,df_test_distance))
        
if __name__ == "__main__":
    unittest.main()