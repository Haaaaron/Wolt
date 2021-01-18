import os
import sys
TESTFILE = os.path.join(os.path.dirname(__file__), "./snapshots/simple.json")
TESTFILE_INCORRECT_DATA = os.path.join(os.path.dirname(__file__), "./snapshots/incorrect.json")

TOPDIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(TOPDIR)

import unittest
import pandas as pd
import pandas.testing as pdt
import random
import json as JSON
from backend.json_data import *

def setUpModule():    
    global df_test
    global json_test_in
    global json_test_out

    json_test_in = {
        "restaurants": [
            {
                "blurhash": "UAN=8k?LS~M:ErJFs%t0MDMWRqo@%BxSV{RX",
                "launch_date": "2020-04-20",
                "location": [24.938082, 60.17626],
                "name": "Sea Chain",
                "online": True,
                "popularity": 0.9569904141
            }
        ]
    }

    json_test_out = {
        "title":"Example title",
        "restaurants": [
            {
                "blurhash": "UAN=8k?LS~M:ErJFs%t0MDMWRqo@%BxSV{RX",
                "launch_date": "2020-04-20",
                "location": [24.938082, 60.17626],
                "name": "Sea Chain",
                "online": True,
                "popularity": 0.9569904141
            }
        ]
    }
    
    

    df_test = pd.json_normalize(json_test_in['restaurants'])

class JsonTest(unittest.TestCase):
    """ Test backend.json_data.py """

    def test_load_as_df(self):
        """ Test if json_data.load_as_df loads dataframe correctly """
        df_returned, err = load_as_df(file=TESTFILE)
        self.assertIsNone(pdt.assert_frame_equal(df_test,df_returned))
        self.assertIsNone(err)
    
    def test_none_file(self):
        """ Test that missing file returns df=None and correct error """
        df_returned, err_returned = load_as_df(file="missing.json")
        err_expected = "JSON file {} not found".format("missing.json")
        self.assertIsNone(df_returned)
        self.assertEqual(err_returned,err_expected)

    def test_incorrect_data_format(self):
        """ Test that incorrect JSON data returns df=None and correct error """
        df_returned, err_returned = load_as_df(file=TESTFILE_INCORRECT_DATA)
        err_expected = "Key:'restaurants' not found in JSON file"
        self.assertIsNone(df_returned)
        self.assertEqual(err_returned,err_expected)

    def test_unexpected_error(self):
        """ Test that undexpected error returns df=None """
        df_returned, err_returned = load_as_df(file=None)
        self.assertIsNone(df_returned)

    def test_dataframe_to_json(self):
        """ Test that json_data.dataframe_to_json returns correct JSON """
        example_input = ("Example title",df_test)
        json_returned = dataframe_to_json(example_input)
        result, example = JSON.dumps(json_returned, sort_keys=True), JSON.dumps(json_test_out, sort_keys=True)
        self.assertEqual(result,example)
    
    def test_empty_dataframe_to_json_(self):
        """ Test that empty DataFrame returns None """
        df_empty = pd.DataFrame(columns = ["empty"])
        example_result = ("Example title",df_empty)
        result = dataframe_to_json(example_result)      
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()