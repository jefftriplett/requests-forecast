# requests-forecast

[![](https://badge.fury.io/py/requests-forecast.png "Latest Package Version")](http://badge.fury.io/py/requests-forecast)
[![](https://pypip.in/d/requests-forecast/badge.png "Download Status")](https://pypi.org/project/requests-forecast/)

For complete docs and API options see: https://developer.forecast.io/docs/v2

## Requirements

* Python 3.6+
* requests

## Installation

To install requests-forecast, simply:

```shell
$ pip install requests-forecast
```

## Documentation

- Development version: http://requests-forecast.rtfd.org.

## Quickstart

### Creating a client

```python
from requests_forecast import Forecast
forecast = Forecast(apikey='YOUR-API-KEY')
```

### Getting the current conditions

```python
current = forecast.currently()
print current['temperature']
58.9
```

### Getting minutely conditions

```python
current = forecast.minutely()
current['summary']
u'Mostly cloudy for the hour.'
current['data'][0].keys()
[u'precipIntensity', u'time']
```

### Getting hourly conditions

```python
current = forecast.hourly()
current['temperature']
59.52
forecast.hourly()['summary']
Mostly cloudy until tomorrow afternoon.
forecast.hourly()['data'][0]['temperature']
59.52
```

### Getting daily conditions

```python
forecast.daily()['summary']
u'Mixed precipitation off-and-on throughout the week; temperatures peaking at 70\xb0 on Sunday.'
forecast.daily()['data'][0]['temperatureMax']
63.85
forecast.daily()['data'][0]['temperatureMin']
35.05
```

### Getting alerts

```python
forecast.alerts()
{
  "expires": 1366898400,
  "uri": "http://alerts.weather.gov/cap/wwacapget.php?x=KS124EFAC89CD0.FreezeWarning.124EFAD6F320KS.TOPNPWTOP.8ab7d76a4db42b9136a1a6849a631097",
  "title": "Freeze Warning for Douglas, KS"
}
```

## Example usage

```python
from datetime import datetime
from requests_forecast import Forecast

forecast = Forecast(apikey='YOUR-API-KEY')
data = forecast.get(latitude=38.9717, longitude=-95.235)

forecast.currently()['temperature']
58.9

data = forecast.get(latitude=38.9717, longitude=-95.235,
time=datetime(year=2013, month=12, day=29))

forecast.currently()['temperature']
58.9

forecast.currently()['temperature']
36.75
```

## License

New BSD
