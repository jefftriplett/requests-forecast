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
        body=open('tests/test_full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)

    assert forecast.currently.keys() == [u'precipIntensity', u'temperature', u'icon', u'cloudCover', u'summary', u'pressure', u'windSpeed', u'visibility', u'time', u'humidity', u'windBearing']
    assert forecast.currently['temperature'] == 58.9
    assert forecast.currently.temperature == 58.9
    assert forecast.currently['summary'] == u'Mostly Cloudy'

    # test that timestamps are turned into datetime's
    assert forecast.currently['time'] == datetime(2013, 3, 28, 19, 8, 25)
    #assert forecast.currently['time'] == data['currently']['time']


@httprettified
def test_forecast_daily():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/test_full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)

    assert forecast.daily.keys() == [u'summary', u'data', u'icon']
    assert forecast.daily['icon'] == u'rain'
    assert forecast.daily['summary'] == u'Mixed precipitation off-and-on throughout the week; temperatures peaking at 70\xb0 on Sunday.'

    assert len(forecast.daily['data']) == 8
    assert forecast.daily['data'][0].keys() == [u'precipIntensity', u'sunriseTime', u'icon', u'precipType', u'temperatureMax', u'cloudCover', u'summary', u'pressure', u'windSpeed', u'temperatureMin', u'visibility', u'time', u'windBearing', u'humidity', u'temperatureMaxTime', u'sunsetTime', u'temperatureMinTime']
    assert forecast.daily['data'][0]['temperatureMax'] == 63.85
    assert forecast.daily['data'][0]['temperatureMin'] == 35.05

    # test that timestamps are turned into datetime's
    assert forecast.daily['data'][0]['time'] == datetime(2013, 03, 28, 00, 00, 00)
    assert forecast.daily['data'][0]['sunriseTime'] == datetime(2013, 03, 28, 07, 12, 29)
    assert forecast.daily['data'][0]['sunsetTime'] == datetime(2013, 03, 28, 19, 41, 39)
    assert forecast.daily['data'][0]['temperatureMaxTime'] == datetime(2013, 03, 28, 16, 00, 00)
    assert forecast.daily['data'][0]['temperatureMinTime'] == datetime(2013, 03, 28, 07, 00, 00)

    #assert forecast.daily['data'][0]['time'] == data['daily']['data'][0]['time']


@httprettified
def test_forecast_hourly():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/test_full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)

    assert 'data' in forecast.hourly.keys()
    assert 'icon' in forecast.hourly.keys()
    assert 'summary' in forecast.hourly.keys()

    assert forecast.hourly['icon'] == u'partly-cloudy-day'
    assert forecast.hourly['summary'] == u'Mostly cloudy until tomorrow afternoon.'
    assert forecast.hourly['data'][0].keys() == [u'precipIntensity', u'temperature', u'icon', u'cloudCover', u'summary', u'pressure', u'windSpeed', u'visibility', u'time', u'humidity', u'windBearing']

    assert len(forecast.hourly['data']) == 49
    assert forecast.hourly['data'][0]['temperature'] == 59.52
    assert forecast.hourly['data'][0]['time'] == datetime(2013, 3, 28, 19, 0)


@httprettified
def test_forecast_minutely():
    HTTPretty.register_uri(
        HTTPretty.GET,
        'https://api.forecast.io/forecast/1234/38.9717,-95.235',
        body=open('tests/test_full.json', 'r').read(),
        content_type='text/json')

    forecast = Forecast(apikey, latitude=latitude, longitude=longitude)

    assert forecast.minutely.keys() == [u'summary', u'data', u'icon']
    assert forecast.minutely['icon'] == u'partly-cloudy-day'
    assert forecast.minutely['summary'] == u'Mostly cloudy for the hour.'

    assert len(forecast.minutely['data']) == 61
    assert forecast.minutely['data'][0].keys() == [u'precipIntensity', u'time']
    assert forecast.minutely['data'][0]['time'] == datetime(2013, 3, 28, 19, 8)
