import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

import unittest
from backend import app

def setUpModule():
    global dummy_route
    global dummy_route_incorrect
    global dummy_route_missing
    dummy_route="/discovery?lat=0&lon=0"
    dummy_route_incorrect="/discovery?lat=a&lon=b"
    dummy_route_missing="/discovery?lat=None&lon=None"

class FlaskTest(unittest.TestCase):

    def test_index(self):
        """ Test that Flask returns endpoint """
        tester = app.app.test_client(self)
        response = tester.get(dummy_route)
        self.assertEqual(response.status_code,200)

    def test_response_type(self):
        """ Test response type is JSON """
        tester = app.app.test_client(self)
        response = tester.get(dummy_route)
        self.assertEqual(response.content_type,"application/json")

    def test_response_data(self):
        """ Test response data contains sections i.e format is correct """
        tester = app.app.test_client(self)
        response = tester.get(dummy_route)
        self.assertTrue(b'sections' in response.data)

    def test_incorrect_query_params(self):
        """ Test incorrect query params returns error and error message """
        tester = app.app.test_client(self)
        response = tester.get(dummy_route_incorrect)
        self.assertEqual(response.status_code,400)
        self.assertTrue(b'error' in response.data)

    def test_missing_query_params(self):
        """ Test missing query params returns error and error message """
        tester = app.app.test_client(self)
        response = tester.get(dummy_route_missing)
        self.assertEqual(response.status_code,400)
        self.assertTrue(b'error' in response.data)
        
if __name__ == "__main__":
    unittest.main()
