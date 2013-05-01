import datetime
import pytz
import requests
import time as time_mod


FORECAST_TEMPLATE = 'https://api.forecast.io/forecast/{apikey}/{latitude},{longitude}{time}{si}'


class AttrDict(dict):

    def __init__(self, *args, **kwargs):
        self.timezone = kwargs.pop('timezone', '')
        dict.__init__(self, *args, **kwargs)

    def __getattr__(self, attr):
        #print '+', attr

        #if attr == 'time' or attr.endswith('Time'):
            #print '-', attr
            #if key == 'time' or key.endswith('Time'):
            #    obj[key] = datetime.datetime.fromtimestamp(int(obj[key])).replace(tzinfo=self.timezone)

        #elif attr == 'timezone':
            #print '- timezone'
            #    self.timezone = pytz.timezone(obj[key])

        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


def json_to_python(obj):
    timezone = None
    if isinstance(obj, list):
        return _list_proxy(timezone, obj)
    elif isinstance(obj, dict):
        return _dict_proxy(timezone, obj)
    else:
        return obj


class _list_proxy(object):

    def __init__(self, timezone, proxied_list):
        self.timezone = timezone
        object.__setattr__(self, 'data', proxied_list)

    def __getitem__(self, a):
        return json_to_python(object.__getattribute__(self, 'data').__getitem__(a))

    def __setitem__(self, a, v):
        return object.__getattribute__(self, 'data').__setitem__(a, v)


class _dict_proxy(_list_proxy):

    def __init__(self, timezone, proxied_dict):
        self.timezone = timezone
        _list_proxy.__init__(self, timezone, proxied_dict)

    def __getattribute__(self, a):
        return json_to_python(object.__getattribute__(self, 'data').__getitem__(a))

    #def __setattr__(self, a, v):
    #    return object.__getattribute__(self, 'data').__setitem__(a, v)


class Forecast(object):
    data = None
    timezone = None

    def __init__(self, apikey, latitude=None, longitude=None, time=None,
                 parse_timestamps=True):
        self.apikey = apikey
        self.parse_timestamps = parse_timestamps
        self.latitude = latitude
        self.longitude = longitude
        self.time = time

    def convert_timestamps(self, obj):
        for key in obj.keys():
            if key in ['expires', 'time'] or key.endswith('Time'):
                obj[key] = datetime.datetime.fromtimestamp(int(obj[key])).replace(tzinfo=self.timezone)
            elif key == 'timezone':
                self.timezone = pytz.timezone(obj[key])

        if isinstance(obj, list):
            return _list_proxy(self.timezone, obj)

        elif isinstance(obj, dict):
            return _dict_proxy(self.timezone, obj)

        return obj

    def get(self, latitude=None, longitude=None, time=None, si=False):
        if time:
            time = int(time_mod.mktime(time.timetuple()))

        url = FORECAST_TEMPLATE.format(
            apikey=self.apikey,
            latitude=latitude or self.latitude,
            longitude=longitude or self.longitude,
            time=',{}'.format(time) if time else '',
            si='?{}'.format(si) if si else ''
        )
        request = requests.get(url)

        json_defaults = {}
        if self.parse_timestamps:
            #json_defaults['object_hook'] = json_to_python
            #json_defaults['object_hook'] = self.convert_timestamps
            json_defaults['object_hook'] = AttrDict

        self.data = request.json(**json_defaults)

        return self.data

    @property
    def currently(self):
        return self.data.currently  # ('currently', None)

    @property
    def daily(self):
        return self.data.daily  # get('daily', None)

    @property
    def hourly(self):
        return self.data.hourly  # get('hourly', None)

    @property
    def minutely(self):
        return self.data.minutely  # get('minutely', None)
