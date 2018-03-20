# -*- coding: utf-8 -*-
import pytz
import requests
import time as time_mod

from datetime import datetime


__title__ = 'requests-forecast'
__version__ = '0.6.2'
__author__ = 'Jeff Triplett'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013-2014 Jeff Triplett'


FORECAST_TEMPLATE = 'https://api.darksky.net/forecast/{apikey}/{latitude},{longitude}{time}'
ALERT_FIELDS = ('alerts',)
DATA_FIELDS = ('data',)
DECIMAL_FIELDS = ('cloudCover', 'precipProbability', 'humidity')
TIME_FIELDS = ('expires', 'time')


class DataBlock(dict):

    def __init__(self, data=None, timezone=None):
        self.timezone = str(timezone)
        if data:
            for key in data.keys():
                if key in TIME_FIELDS or key.endswith('Time'):
                    if timezone:
                        tz = pytz.timezone(str(timezone))
                        utc = pytz.utc
                        ts = datetime.utcfromtimestamp(int(data[key])).replace(tzinfo=utc)
                        data[key] = tz.normalize(ts.astimezone(tz))
                    else:
                        data[key] = datetime.fromtimestamp(int(data[key]))

                elif key in DECIMAL_FIELDS:
                    data[key] = float(data[key]) * float('100.0')
                elif key in DATA_FIELDS:
                    self.data = []
                    for datapoint in data[key]:
                        self.data.append(DataBlock(data=datapoint, timezone=timezone))
                elif key in ALERT_FIELDS:
                    self.alerts = []
                    for alert in data[key]:
                        self.alerts.append(DataBlock(data=alert, timezone=timezone))

            super(DataBlock, self).__init__(data)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


class Forecast(object):
    json = None
    timezone = None

    def __init__(self, apikey, latitude=None, longitude=None, time=None):
        self.apikey = apikey
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        #self.units  # TODO Fix units

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
            alerts = []
            for alert in self.json['alerts']:
                alerts.append(DataBlock(alert, self.timezone))
            return alerts
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
