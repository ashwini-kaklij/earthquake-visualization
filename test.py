import unittest
import requests


class TestEarthquakeApp(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5002/api/v1/earthquake-data/2016-01-01/2016-01-31'

    def test_hello_world(self):
        response = requests.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['properties'])


if __name__ == '__main__':
    unittest.main()