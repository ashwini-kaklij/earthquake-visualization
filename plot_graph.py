import datetime
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import requests

MARKER_SIZE = 2


class Earthquake(object):

    def __init__(self, url, params={}):
        self.request_url = url
        self.params = params
        self.fetch_url()
        self.plot_time_slot_with_magnitude()
        self.plot_with_magnitude()
        self.plot_with_status_and_magnitude()
        self.plot_with_earthquake_status()
        self.plot_alert()
        self.plot_tsunami()
        self.plot_tsunami_with_magnitude()

    def fetch_url(self):
        """
        Fetch earthquake data
        :return:
        """
        data = requests.get(self.request_url)
        self.response = data.json()
        return self.response

    @staticmethod
    def init_basemap():
        map = Basemap(
            projection='moll', resolution='l',
            area_thresh=1000.0, lat_0=0, lon_0=-130
        )
        map.drawcoastlines(linewidth=0.25)
        map.drawcountries(linewidth=0.25)
        map.fillcontinents(color='gray')
        map.drawmeridians(np.arange(0, 360, 30))
        map.drawparallels(np.arange(-90, 90, 30))
        return map

    def plot_time_slot_with_magnitude(self):
        """
        Plot the map on basis of particular interval of day
        e.g. Morning, Evening, Afternoon, Night
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            mags = res['magnitudes']
            time_slots = res['time_slots']
            for lon, lat, mag, time_slot in zip(lons, lats, mags, time_slots):
                if mag is not None:
                    x, y = map(lon, lat)
                    marker_string, time_value = self.set_slot_marker_color(time_slot)
                    msize = time_value * MARKER_SIZE
                    map.plot(x, y,marker_string, markersize=msize)
        title_string = "Earthquakes on basis of time \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='Night')
        med = mpatches.Patch(color='olive', label='Morning')
        med1 = mpatches.Patch(color='red', label='Afternoon')
        high = mpatches.Patch(color='orange', label='Evening')
        plt.legend(handles=[low, med,med1, high], title='Earthquakes Time')
        plt.title(title_string)
        plt.show()

    def plot_with_magnitude(self):
        """
        Plot the map on basis of Magnitude values
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            mags = res['magnitudes']
            for lon, lat, mag in zip(lons, lats, mags):
                x, y = map(lon, lat)
                if mag is not None:
                    msize = mag * MARKER_SIZE
                    marker_string = self.set_marker_color(mag)
                    map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes of Magnitude 1.0 or Greater \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='< 3')
        med = mpatches.Patch(color='olive', label='< 5')
        high = mpatches.Patch(color='red', label='> 5')
        plt.legend(handles=[low, med, high], title='Earthquakes Magnitude')
        plt.title(title_string)
        plt.show()

    def plot_with_status_and_magnitude(self):
        """
        Plot the map on basis of magnitude where status is reviewed
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            mags = res['magnitudes']
            statuses = res['statuses']
            for lon, lat, mag, status in zip(lons, lats, mags, statuses):
                if mag is not None and status == "reviewed":
                    x, y = map(lon, lat)
                    msize = mag * MARKER_SIZE
                    marker_string = self.set_marker_color(mag)
                    map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes of Magnitude 1.0 or Greater :for Status is 'REVIEWED' \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='< 3')
        med = mpatches.Patch(color='olive', label='< 5')
        high = mpatches.Patch(color='red', label='> 5')
        plt.legend(handles=[low, med, high], title='Earthquakes Magnitude')
        plt.title(title_string)
        plt.show()

    def plot_with_earthquake_status(self):
        """
        Plot the map on basis of Status -reviewed, automatic, deleted
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            statuses = res['statuses']
            for lon, lat, status in zip(lons, lats, statuses):
                x, y = map(lon, lat)
                # if statuses is not None:
                marker_string, status_val = self.set_status_color(status)
                msize = status_val * MARKER_SIZE
                map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes on basis of Status  \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='automatic')
        med = mpatches.Patch(color='olive', label='reviewed')
        high = mpatches.Patch(color='red', label='deleted')
        plt.legend(handles=[low, med, high], title='Earthquakes Status')
        plt.title(title_string)
        plt.show()

    def plot_alert(self):
        """
        Plot the map on basis of alert:green, yellow, orange, red
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            alerts = res['alerts']
            for lon, lat, alert in zip(lons, lats, alerts):
                x, y = map(lon, lat)
                marker_string, alert_val = self.set_alert_color(alert)
                msize = alert_val * MARKER_SIZE
                map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes data on basis of Alerts \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='green')
        med = mpatches.Patch(color='olive', label='yellow')
        med1 = mpatches.Patch(color='orange', label='orange')
        high = mpatches.Patch(color='red', label='red')
        plt.legend(handles=[low, med, med1, high], title='Earthquakes Alerts')
        plt.title(title_string)
        plt.show()

    def plot_tsunami(self):
        """
        Plot the map on basis of whether it was tsunami or not
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            tsunamies = res['tsunamies']
            for lon, lat, tsunami in zip(lons, lats, tsunamies):
                x, y = map(lon, lat)
                marker_string, tsunamies_val = self.set_tsunamies_color(tsunami)
                msize = tsunamies_val * MARKER_SIZE
                map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes data on basis of tsunami values \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='No')
        med = mpatches.Patch(color='red', label='Yes')
        plt.legend(handles=[low, med], title='Earthquakes Tsunami')
        plt.title(title_string)
        plt.show()

    def plot_tsunami_with_magnitude(self):
        """
        Plot the map on basis of magnitude and tsunami
        """
        map = self.init_basemap()
        data = self.response
        for res in data.values():
            lats = res['lats']
            lons = res['lons']
            mags = res['magnitudes']
            tsunamies = res['tsunamies']
            for lon, lat, mag, tsunamies in zip(lons, lats, mags, tsunamies):
                if mag is not None and tsunamies == 1:
                    x, y = map(lon, lat)
                    msize = mag * MARKER_SIZE
                    marker_string = self.set_marker_color_mag(mag)
                    map.plot(x, y, marker_string, markersize=msize)
        title_string = "Earthquakes data for magnitudes for basis of tsunami :Present \n"
        title_string += str(self.params['start']) + ' through ' + str(self.params['end'])
        low = mpatches.Patch(color='green', label='> 3')
        med = mpatches.Patch(color='olive', label='> 4')
        high = mpatches.Patch(color='red', label='> 5')
        plt.legend(handles=[low, med, high], title='Earthquakes Magnitude')
        plt.title(title_string)
        plt.show()

    @staticmethod
    def set_slot_marker_color(time_slot):
        """
        to get marker colour on basis of time_slot
        :param time_slot:
        :return: str, int
        """
        if time_slot == 'Night':
            return 'go', 2
        elif time_slot == 'Morning':
            return 'yo', 3
        elif time_slot == 'Afternoon':
            return 'ro', 3
        else:
            return 'or', 4

    @staticmethod
    def set_marker_color(magnitude):
        """
        to get marker color on basis of magnitude value
        :param magnitude:
        :return: str
        """
        if magnitude < 3.0:
            return 'go'
        elif magnitude < 5.0:
            return 'yo'
        else:
            return 'ro'

    @staticmethod
    def set_status_color(status):
        """
        to get marker color on basis  status
        :param status:
        :return: str, int
        """
        if status == "automatic":
            return 'go',  2
        elif status == "reviewed":
            return 'yo', 3
        else:
            return 'ro', 4

    @staticmethod
    def set_alert_color(alert):
        """
        to get marker color on basis alerts value
        :param alert:
        :return: str, int
        """
        if alert == "green":
            return 'go', 2
        elif alert == "yellow":
            return 'yo', 2
        elif alert == "orange":
            return 'or', 2
        else:
            return 'ro', 2

    @staticmethod
    def set_tsunamies_color(tsunami):
        """
        to get marker color on basis of tsunami value
        :param tsunami:
        :return: str, int
        """
        if tsunami == 1:
            return 'ro', 4
        else:
            return 'go', 2

    @staticmethod
    def set_marker_color_mag(magnitude):
        """
        to get marker color on basis of magnitude value
        :param magnitude:
        :return: str
        """
        if magnitude > 3.0 and magnitude < 4.0 :
            return 'go'
        elif magnitude > 4.0 and magnitude < 5.0 :
            return 'yo'
        elif magnitude > 5.0 :
            return 'ro'


if __name__ == "__main__":
    PARAMS = {
        'start': '2016-01-01',
        'end': '2016-01-10'
    }
    URL = 'http://localhost:5002/api/v1/earthquake-data/' + PARAMS['start'] + '/' + PARAMS['end']
    earthquake = Earthquake(URL, PARAMS)
