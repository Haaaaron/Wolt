""" Test ./backend/app.py module """

import sys
import os
import unittest

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from backend.app import app


def setUpModule():
    """ unittest default setup """
    global DUMMY_ROUTE
    global DUMMY_ROUTE_INCORRECT
    global DUMMY_ROUTE_MISSING
    DUMMY_ROUTE = "/discovery?lat=0&lon=0"
    DUMMY_ROUTE_INCORRECT = "/discovery?lat=a&lon=b"
    DUMMY_ROUTE_MISSING = "/discovery?lat=None&lon=None"


class FlaskTest(unittest.TestCase):
    """ Unittest test class """

    def test_index(self):
        """ Test that Flask returns endpoint """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertEqual(response.status_code, 200)

    def test_response_type(self):
        """ Test response type is JSON """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertEqual(response.content_type, "application/json")

    def test_response_data(self):
        """ Test response data contains sections i.e format is correct """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE)
        self.assertTrue(b'sections' in response.data)

    def test_incorrect_query_params(self):
        """ Test incorrect query params returns error and error message """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE_INCORRECT)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'error' in response.data)

    def test_missing_query_params(self):
        """ Test missing query params returns error and error message """
        tester = app.test_client(self)
        response = tester.get(DUMMY_ROUTE_MISSING)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(b'error' in response.data)


if __name__ == "__main__":
    unittest.main()
