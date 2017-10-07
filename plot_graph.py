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
        """
        Fetch earthquake data
        :return:
        """
        data = requests.get(self.request_url)
        response = data.json()
        return response

    def get_geo_data(self):
        """
        Format earthquake data
        :return: list1, list2, list3
        """
        data = self.fetch_url()
        lats = []
        lons = []
        mags = []
        for res in data.values():
            lons.extend(res['lons'])
            lats.extend(res['lats'])
            mags.extend(res['magnitudes'])
        return lats, lons, mags

    def plot(self):
        """
        Data plotting
        """
        map = Basemap(
            projection='moll', resolution='l',
            area_thresh=1000.0, lat_0=0, lon_0=-130
        )
        map.drawcoastlines(linewidth=0.25)
        map.drawcountries(linewidth=0.25)
        map.fillcontinents(color='gray')
        map.drawmeridians(np.arange(0, 360, 30))
        map.drawparallels(np.arange(-90, 90, 30))
        min_marker_size = 4
        lats, lons, mags = self.get_geo_data()

        for lon, lat, mag in zip(lons, lats, mags):
            x, y = map(lon, lat)
            if mag is not None:
                msize = mag * min_marker_size
                marker_string = self.set_marker_color(mag)
                map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes of Magnitude 1.0 or Greater \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        plt.title(title_string)
        plt.show()

    @staticmethod
    def set_marker_color(magnitude):
        if magnitude < 3.0:
            return 'go'
        elif magnitude < 5.0:
            return 'yo'
        else:
            return 'ro'


if __name__ == "__main__":
    PARAMS = {
        'start': '2016-01-01',
        'end': '2016-01-30'
    }
    URL = 'http://localhost:5002/api/v1/earthquake-data/' + PARAMS['start'] + '/' + PARAMS['end']
    earthquake = Earthquake(URL, PARAMS)
