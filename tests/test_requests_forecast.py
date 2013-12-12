from datetime import datetime
from httpretty import HTTPretty, httprettified

from requests_forecast import Forecast


apikey = '1234'
latitude = 38.9717
longitude = -95.235


@httprettified
def test_forecast_currently():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)
    currently = forecast.get_currently()

    assert 'precipIntensity' in currently.keys()
    assert 'temperature' in currently.keys()
    assert 'icon' in currently.keys()
    assert 'cloudCover' in currently.keys()
    assert 'summary' in currently.keys()
    assert 'pressure' in currently.keys()
    assert 'windSpeed' in currently.keys()
    assert 'visibility' in currently.keys()
    assert 'time' in currently.keys()
    assert 'humidity' in currently.keys()
    assert 'windBearing' in currently.keys()

    assert currently['temperature'] == 58.9
    assert currently.temperature == 58.9
    assert currently['summary'] == u'Mostly Cloudy'
    assert currently['time'] == datetime(2013, 3, 28, 19, 8, 25)


@httprettified
def test_forecast_daily():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)
    daily = forecast.get_daily()

    assert 'data' in daily.keys()
    assert 'icon' in daily.keys()
    assert 'summary' in daily.keys()

    assert daily['icon'] == u'rain'
    assert daily['summary'] == u'Mixed precipitation off-and-on throughout the week; temperatures peaking at 70\xb0 on Sunday.'

    assert len(daily['data']) == 8
    assert 'cloudCover' in daily['data'][0].keys()
    assert 'humidity' in daily['data'][0].keys()
    assert 'icon' in daily['data'][0].keys()
    assert 'precipIntensity' in daily['data'][0].keys()
    assert 'precipType' in daily['data'][0].keys()
    assert 'pressure' in daily['data'][0].keys()
    assert 'summary' in daily['data'][0].keys()
    assert 'sunriseTime' in daily['data'][0].keys()
    assert 'sunsetTime' in daily['data'][0].keys()
    assert 'temperatureMax' in daily['data'][0].keys()
    assert 'temperatureMaxTime' in daily['data'][0].keys()
    assert 'temperatureMin' in daily['data'][0].keys()
    assert 'temperatureMinTime' in daily['data'][0].keys()
    assert 'time' in daily['data'][0].keys()
    assert 'visibility' in daily['data'][0].keys()
    assert 'windBearing' in daily['data'][0].keys()
    assert 'windSpeed' in daily['data'][0].keys()

    assert daily['data'][0]['temperatureMax'] == 63.85
    assert daily['data'][0]['temperatureMin'] == 35.05
    assert daily['data'][0]['time'] == datetime(2013, 3, 28, 0, 0)
    assert daily['data'][0]['sunriseTime'] == datetime(2013, 3, 28, 7, 12, 29)
    assert daily['data'][0]['sunsetTime'] == datetime(2013, 3, 28, 19, 41, 39)
    assert daily['data'][0]['temperatureMaxTime'] == datetime(2013, 3, 28, 16, 0)
    assert daily['data'][0]['temperatureMinTime'] == datetime(2013, 3, 28, 7, 0)


@httprettified
def test_forecast_hourly():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)
    hourly = forecast.get_hourly()
    assert 'data' in hourly.keys()
    assert 'icon' in hourly.keys()
    assert 'summary' in hourly.keys()

    assert hourly['icon'] == u'partly-cloudy-day'
    assert hourly['summary'] == u'Mostly cloudy until tomorrow afternoon.'

    assert 'cloudCover' in hourly['data'][0].keys()
    assert 'humidity' in hourly['data'][0].keys()
    assert 'icon' in hourly['data'][0].keys()
    assert 'precipIntensity' in hourly['data'][0].keys()
    assert 'pressure' in hourly['data'][0].keys()
    assert 'summary' in hourly['data'][0].keys()
    assert 'temperature' in hourly['data'][0].keys()
    assert 'time' in hourly['data'][0].keys()
    assert 'visibility' in hourly['data'][0].keys()
    assert 'windBearing' in hourly['data'][0].keys()
    assert 'windSpeed' in hourly['data'][0].keys()

    assert len(hourly['data']) == 49
    assert hourly['data'][0]['temperature'] == 59.52
    assert hourly['data'][0]['time'] == datetime(2013, 3, 28, 19, 0)


@httprettified
def test_forecast_minutely():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)
    minutely = forecast.get_minutely()

    assert 'data' in minutely.keys()
    assert 'icon' in minutely.keys()
    assert 'summary' in minutely.keys()

    assert minutely['icon'] == u'partly-cloudy-day'
    assert minutely['summary'] == u'Mostly cloudy for the hour.'

    assert len(minutely['data']) == 61
    assert minutely['data'][0].keys() == [u'precipIntensity', u'time']
    assert minutely['data'][0]['time'] == datetime(2013, 3, 28, 19, 8)


@httprettified
def test_forecast_alerts():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/alerts.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)
    alerts = forecast.get_alerts()

    assert len(alerts) == 1
    assert alerts[0]['title'] == u'Freeze Warning for Marin, CA'
    assert alerts[0]['time'] == datetime(2013, 12, 11, 19, 8)
    assert alerts[0]['expires'] == datetime(2013, 12, 12, 11, 0)
