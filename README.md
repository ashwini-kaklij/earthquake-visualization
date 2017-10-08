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

Now execute plot_graph.py which calls the above API and plots the points on graphs.


