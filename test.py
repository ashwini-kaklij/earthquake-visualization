import unittest
import requests

from utils import get_day_slot


class TestEarthquakeApp(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5002/api/v1/earthquake-data/2016-01-01/2016-01-31'

    def test_hello_world(self):
        response = requests.get(self.url)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['properties'])

    def test_day_interval_calculation(self):
        morning = get_day_slot(11)
        afternoon = get_day_slot(15)
        evening = get_day_slot(21)
        self.assertEqual(morning, 'morning')
        self.assertEqual(afternoon, 'afternoon')
        self.assertEqual(evening, 'evening')


if __name__ == '__main__':
    unittest.main()