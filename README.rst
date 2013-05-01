=================
requests-forecast
=================

For complete docs and API options see: https://developer.forecast.io/docs/v2


Requirements
============

* Python 2.5+
* requests 1.2.0+


Installation
============

To install requests-forecast, simply:

.. code-block:: bash

    $ pip install requests-forecast


Quickstart
==========


Creating a client
-----------------

::

    >>> from requests_forecast import Forecast
    >>> forecast = Forecast(apikey='FORECAST_API_KEY', latitude=38.9717, longitude=-95.235)


Getting the current conditions
------------------------------

::

    >>> current = forecast.currently()
    >>> print current['temperature']
    58.9


Getting minutely conditions
---------------------------

::

    >>> current = forecast.minutely()
    >>> current['summary']
    u'Mostly cloudy for the hour.'
    >>> current['data'][0].keys()
    [u'precipIntensity', u'time']



Getting hourly conditions
-------------------------

::

    >>> current = forecast.hourly
    >>> current['temperature']
    59.52


    >>> forecast.hourly['summary']
    Mostly cloudy until tomorrow afternoon.

    >>> forecast.hourly['data'][0]['temperature']
    >>> 59.52


Getting daily conditions
------------------------

::

    >>> forecast.daily['summary']
    u'Mixed precipitation off-and-on throughout the week; temperatures peaking at 70\xb0 on Sunday.'
    >>> forecast.daily['data'][0]['temperatureMax']
    63.85
    >>> forecast.daily['data'][0]['temperatureMin']
    35.05


Getting alerts
--------------

::

    >>> forecast.alerts()
    {
      "expires": 1366898400,
      "uri": "http://alerts.weather.gov/cap/wwacapget.php?x=KS124EFAC89CD0.FreezeWarning.124EFAD6F320KS.TOPNPWTOP.8ab7d76a4db42b9136a1a6849a631097",
      "title": "Freeze Warning for Douglas, KS"
    }


Example usage
~~~~~~~~~~~~~

::

    from datetime import datetime
    from requests_forecast import Forecast

    forecast = Forecast(apikey='YOUR-API-KEY')
    data = forecast.get(latitude=38.9717, longitude=-95.235)

    >>> forecast.currently['temperature']
    58.9

    data = forecast.get(latitude=38.9717, longitude=-95.235,
        time=datetime(year=2013, month=12, day=29))

    >>> forecast.currently['temperature']
    58.9

    >>> forecast.currently['temperature']
    36.75


License
=======

New BSD
