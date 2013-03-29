requests-forecast
=================




https://developer.darkskyapp.com/



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
