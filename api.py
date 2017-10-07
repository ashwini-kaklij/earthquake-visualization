import requests
from multiprocessing.pool import ThreadPool
from flask import Flask, jsonify, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class EarthquakeData(Resource):

    def __init__(self):
        self.request_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
        self.limit = 100
        self.total = 500
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
        for res, error in results:
            if error is None:
                for data in res['features']:
                    lons.append(data['geometry']['coordinates'][0])
                    lats.append(data['geometry']['coordinates'][1])
                    magnitudes.append(data['properties']['mag'])
            else:
                return "error fetching %r: %s" % error
        earth_quake_data.update({'properties': {'lats': lats, 'lons': lons, 'magnitudes': magnitudes}})
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

api.add_resource(EarthquakeData, '/api/v1/earthquake-data/<string:start>/<string:end>')

if __name__ == '__main__':
    app.run(debug=True, port=5002)