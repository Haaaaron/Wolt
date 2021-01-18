import os
import sys
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

import unittest
from backend import app

class FlaskTest(unittest.TestCase):

    def test_index(self,dummy_route="/discovery?lat=0&lon=0"):
        tester = app.test_client(self)
        response = tester.get(dummy_route)
        self.assertEqual(response.status_code,200)

    def test_response_type(self,dummy_route="/discovery?lat=0&lon=0"):
        tester = app.test_client(self)
        response = tester.get(dummy_route)
        self.assertEqual(response.content_type,"application/json")

    def test_response_data(self,dummy_route="/discovery?lat=0&lon=0"):
        tester = app.test_client(self)
        response = tester.get(dummy_route)
        self.assertTrue(b'sections' in response.data)
        
if __name__ == "__main__":
    unittest.main()
