import datetime
import requests
from multiprocessing.pool import ThreadPool
from flask import Flask, jsonify, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class EarthquakeData(Resource):

    def __init__(self):
        self.request_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.limit = 1000
        self.total = 10000
        self.param = {
            'format': 'geojson',
            'limit': self.limit
        }

    def get(self, start, end):
        self.param.update({
            'starttime': start,
            'endtime': end
        })
        threads = int(round(self.total / self.limit))
        results = ThreadPool(threads).imap_unordered(
            self.fetch_url, range(1, self.total, self.limit)
        )
        earth_quake_data = {}
        lats = []
        lons = []
        magnitudes = []
        statuses = []
        alerts = []
        tsunamies = []
        time_slots = []
        for res, error in results:
            if error is None:
                for data in res['features']:
                    lons.append(data['geometry']['coordinates'][0])
                    lats.append(data['geometry']['coordinates'][1])
                    magnitudes.append(data['properties']['mag'])
                    statuses.append(data['properties']['status'])
                    slot = self.get_day_slot(data['properties']['time'])
                    time_slots.append(slot)
                    alerts.append(data['properties']['alert'])
                    tsunamies.append(data['properties']['tsunami'])
            else:
                return "error fetching %r: %s" % error
        earth_quake_data.update({'properties': {
            'lats': lats,
            'lons': lons,
            'magnitudes': magnitudes,
            'statuses': statuses,
            'alerts': alerts,
            'tsunamies': tsunamies,
            'time_slots': time_slots
            },
        })
        return jsonify(earth_quake_data)

    def fetch_url(self, offset):
        try:
            self.param.update({'offset': offset})
            res = requests.get(
                self.request_url, params=self.param
            )
            return res.json(), None
        except Exception as e:
            return None, e

    @staticmethod
    def get_day_slot(time):
        hour = int(datetime.datetime.fromtimestamp(int(time) / 1000.0).strftime('%H'))
        if hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'afternoon'
        else:
            return 'evening'


api.add_resource(EarthquakeData, '/api/v1/earthquake-data/<string:start>/<string:end>')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
