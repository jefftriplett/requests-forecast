# -*- coding: utf-8 -*-
import datetime
import pytz
import requests
import time as time_mod


__title__ = 'requests'
__version__ = '0.3.0'
__author__ = 'Jeff Triplett'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 Jeff Triplett'


FORECAST_TEMPLATE = 'https://api.forecast.io/forecast/{apikey}/{latitude},{longitude}{time}'


class DataBlock(dict):

    def __init__(self, data={}, timezone=None):
        self.timezone = timezone
        super(DataBlock, self).__init__(data)
        self.data = []

        if data is not None and 'data' in data:
            for datapoint in data['data']:
                self.data.append(DataBlock(datapoint, timezone=timezone))

    def __getattr__(self, attr):
        try:
            if attr in ['expires', 'time'] or attr.endswith('Time'):
                self[attr] = datetime.datetime.fromtimestamp(int(self[attr])).replace(tzinfo=self.timezone)
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


class DataPoint(dict):

    def __init__(self, data=None, timezone=None):
        self.timezone = timezone
        super(DataPoint, self).__init__(data)

    def __getattr__(self, attr):
        try:
            if attr in ['expires', 'time'] or attr.endswith('Time'):
                self[attr] = datetime.datetime.fromtimestamp(int(self[attr]))  # .replace(tzinfo=self.timezone)
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


class Forecast(object):
    json = None
    timezone = None

    def __init__(self, apikey, latitude=None, longitude=None, time=None,
                 parse_timestamps=True):
        self.apikey = apikey
        self.parse_timestamps = parse_timestamps
        self.latitude = latitude
        self.longitude = longitude
        self.time = time

        self.get(latitude, longitude, time)

        if 'timezone' in self.json:
            self.timezone = pytz.timezone(self.json['timezone'])

    def get(self, latitude=None, longitude=None, time=None):
        if time:
            time = int(time_mod.mktime(time.timetuple()))

        url = FORECAST_TEMPLATE.format(
            apikey=self.apikey,
            latitude=latitude or self.latitude,
            longitude=longitude or self.longitude,
            time=',{}'.format(time) if self.time else ''
        )

        request = requests.get(url, headers={'Accept-Encoding': 'gzip'})
        self.json = request.json()

    def get_alerts(self):
        if 'alerts' in self.json:
            return DataBlock(self.json.alerts, self.timezone)
        return DataBlock()

    def get_currently(self):
        if 'currently' in self.json:
            return DataBlock(self.json['currently'], self.timezone)
        return DataBlock()

    def get_daily(self):
        if 'daily' in self.json:
            return DataBlock(self.json['daily'], self.timezone)
        return DataBlock()

    def get_hourly(self):
        if 'hourly' in self.json:
            return DataBlock(self.json['hourly'], self.timezone)
        return DataBlock()

    def get_minutely(self):
        if 'minutely' in self.json:
            return DataBlock(self.json['minutely'], self.timezone)
        return DataBlock()
