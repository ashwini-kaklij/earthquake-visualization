from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import requests

URL = 'http://localhost:5002/api/v1/earthquake-data'
PARAMS = {
    'start': '2016-01-01',
    'end': '2016-01-30'
}
response = requests.get(URL, params=PARAMS)

data = response.json()
lats = []
lons = []
magnitudes = []
for res in data.values():
    lons = res['lons']
    lats = res['lats']
    magnitudes = res['mag']

map = Basemap(
    projection='moll', resolution='l',
    area_thresh=1000.0, lat_0=0, lon_0=-130
)
map.drawcoastlines()
map.drawcountries()
map.drawlsmask()
map.drawrivers()
map.fillcontinents()
map.bluemarble()
map.drawmapboundary()
map.fillcontinents(color='gray')
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))


def set_marker_color(magnitude):
    if magnitude < 3.0:
        return 'go'
    elif magnitude < 5.0:
        return 'yo'
    else:
        return 'ro'


min_marker_size = 2.5
for lon, lat, mag in zip(lons, lats, magnitudes):
    x, y = map(lon, lat)
    if mag is not None:
        msize = mag * min_marker_size
        marker_string = set_marker_color(mag)
        map.plot(x, y, marker_string, markersize=msize)

title_string = "Earthquakes of Magnitude 1.0 or Greater \n"
title_string += str(PARAMS['start']) + ' through ' + str(PARAMS['end'])
plt.title(title_string)
plt.show()
