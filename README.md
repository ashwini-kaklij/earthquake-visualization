Earthquake visualisation exercise
=================

Quick Installation
------------------

Install below python packages
1. flask
2. matplotlib
3. numpy
4. flask_restful

Install Basemap using Ubuntu’s standard packages

1. sudo apt-get install python-matplotlib
2. sudo apt-get install python-mpltoolkits.basemap

Execute api.py, This will create API that returns the earthquake data for given duration.

Integrated multi threading to send multiple request at the same time followed by parameters offset, limit etc.

API: http://localhost:5002/api/v1/earthquake-data/{start_date}/{end_date}

Now execute plot_map.py which calls the above API and plots the points on maps.
1. Plot the map on basis of particular interval of day
        e.g. Morning, Evening, Afternoon, Night
2. Plot the map on basis of Magnitude values
3. Plot the map on basis of magnitude where status is reviewed
4. Plot the map on basis of Status -reviewed, automatic, deleted
5. Plot the map on basis of alert: green, yellow, orange, red
6. Plot the map on basis of whether it was tsunami or not
7. Plot the map on basis of magnitude and tsunami

There are 7 maps of which screenshots are captured and attached in maps folder.

There are 2 unit tests at the moment.
1. Checks the response of API
2. Validates the slot of the day based on the parameter
