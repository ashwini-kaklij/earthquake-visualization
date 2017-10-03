import requests
from multiprocessing.pool import ThreadPool
from flask import Flask, jsonify, request


app = Flask(__name__)

# Constants
URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
LIMIT = 100
TOTAL = 500
PARAMS = {
    'format': 'geojson',
    'limit': LIMIT
}


@app.route('/api/v1/earthquake-data', methods=['GET'])
def index():
    arguments = request.args
    PARAMS.update({
        'starttime': arguments.get('start'),
        'endtime': arguments.get('end')
    })
    threads = int(round(TOTAL / LIMIT))
    results = ThreadPool(threads).imap_unordered(fetch_url, range(1, TOTAL, LIMIT))
    earth_quake_data = {}
    lats = []
    lons = []
    mag  = []
    for res, error in results:
        if error is None:
            for data in res['features']:
                lons.append(data['geometry']['coordinates'][0])
                lats.append(data['geometry']['coordinates'][1])
                mag.append(data['properties']['mag'])
        else:
            return "error fetching %r: %s" % error
    earth_quake_data.update({'properties': {'lats': lats, 'lons': lons, 'mag': mag}})
    return jsonify(earth_quake_data)


def fetch_url(offset):
    try:
        PARAMS.update({'offset': offset})
        res = requests.get(
            URL, params=PARAMS
        )
        return res.json(), None
    except Exception as e:
        return None, e

if __name__ == '__main__':
    app.run(debug=True, port=5002)