from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import requests


class Earthquake(object):
    def __init__(self, url, params={}):
        self.request_url = url
        self.params = params
        self.plot()

    def fetch_url(self):
        data = requests.get(self.request_url)
        response = data.json()
        return response

    def get_geo_data(self):
        data = self.fetch_url()
        lats = []
        lons = []
        magnitudes = []
        for res in data.values():
            lons.append(res['lons'])
            lats.append(res['lats'])
            magnitudes.append(res['magnitudes'])
        return lats, lons, magnitudes

    def plot(self):
        """Data plotting"""
        map = Basemap(
            projection='moll', resolution='l',
            area_thresh=1000.0, lat_0=0, lon_0=-130
        )
        map.drawcoastlines(linewidth=0.25)
        map.drawcountries(linewidth=0.25)
        map.fillcontinents(color='coral',lake_color='aqua')
        map.drawmeridians(np.arange(0, 360, 30))
        map.drawparallels(np.arange(-90, 90, 30))
        min_marker_size = 4
        lats, lons, statuses = self.get_geo_data()
        for lon, lat, status in zip(lons, lats, statuses):
            x, y = map(lon, lat)
            if status is not None:
                marker_string, size = self.set_marker_color(status)
                msize = size * min_marker_size
                map.plot(x, y, marker_string, markersize=msize)

        title_string = "Earthquakes of Magnitude 1.0 or Greater \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        plt.title(title_string)
        plt.show()

    def set_marker_color(self, magnitude):
        if magnitude == "automatic":
            # Green
            return 'go', 2
        elif magnitude == "reviewed":
            # Yellow
            return 'yo', 3
        else:
            # Red
            return 'ro', 4


if __name__ == "__main__":
    PARAMS = {
        'start': '2016-01-01',
        'end': '2016-01-30'
    }
    URL = 'http://localhost:5002/api/v1/earthquake-data/' + PARAMS['start'] + '/' + PARAMS['end']
    earthquake = Earthquake(URL, PARAMS)
