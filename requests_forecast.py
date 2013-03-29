import datetime
import pytz
import requests
import time as time_mod


FORECAST_TEMPLATE = 'https://api.forecast.io/forecast/{apikey}/{latitude},{longitude}{time}{si}'


class Forecast(object):
    data = None
    timezone = None

    def __init__(self, apikey, parse_timestamps=True):
        self.apikey = apikey
        self.parse_timestamps = parse_timestamps

    def convert_timestamps(self, obj):
        for key in obj.keys():
            if key == 'time' or key.endswith('Time'):
                obj[key] = datetime.datetime.fromtimestamp(int(obj[key])).replace(tzinfo=self.timezone)
            elif key == 'timezone':
                self.timezone = pytz.timezone(obj[key])
        return obj

    def get(self, latitude, longitude, time=None, si=False):
        if time:
            time = int(time_mod.mktime(time.timetuple()))

        url = FORECAST_TEMPLATE.format(
            apikey=self.apikey,
            latitude=latitude,
            longitude=longitude,
            time=',{}'.format(time) if time else '',
            si='?{}'.format(si) if si else ''
        )
        request = requests.get(url)

        json_defaults = {}
        if self.parse_timestamps:
            json_defaults['object_hook'] = self.convert_timestamps

        self.data = request.json(**json_defaults)

        return self.data

    @property
    def currently(self):
        return self.data.get('currently', None)

    @property
    def daily(self):
        return self.data.get('daily', None)

    @property
    def hourly(self):
        return self.data.get('hourly', None)

    @property
    def minutely(self):
        return self.data.get('minutely', None)
