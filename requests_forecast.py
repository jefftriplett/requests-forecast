import pytz
import requests
import time as time_mod
import warnings

from datetime import datetime


__author__ = "Jeff Triplett"
__copyright__ = "Copyright 2013-2021 Jeff Triplett"
__license__ = "BSD"
__title__ = "requests-forecast"
__version__ = "1.0.0"


FORECAST_TEMPLATE = "https://api.darksky.net/forecast/{apikey}/{latitude},{longitude}{time}?units={units}"

ALERT_FIELDS = ("alerts",)

DATA_FIELDS = ("data",)

DECIMAL_FIELDS = (
    "cloudCover",
    "precipProbability",
    "humidity",
)

TIME_FIELDS = (
    "expires",
    "time",
)


class DataBlock(dict):
    def __init__(self, data=None, timezone=None):
        self.timezone = str(timezone)
        if data:
            for key in data.keys():
                if key in TIME_FIELDS or key.endswith("Time"):
                    if timezone:
                        tz = pytz.timezone(str(timezone))
                        utc = pytz.utc
                        ts = datetime.utcfromtimestamp(int(data[key])).replace(
                            tzinfo=utc
                        )
                        # data[key] = tz.normalize(ts.astimezone(tz))
                        data[key] = tz.normalize(ts.astimezone(tz))
                    else:
                        data[key] = datetime.fromtimestamp(int(data[key]))

                elif key in DECIMAL_FIELDS:
                    data[key] = float(data[key]) * float("100.0")

                elif key in ALERT_FIELDS:
                    self.alerts = []
                    for alert in data[key]:
                        self.alerts.append(DataBlock(data=alert, timezone=timezone))

            super().__init__(data)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)


class Forecast:
    json = None
    timezone = None

    def __init__(self, apikey, latitude=None, longitude=None, time=None, units=None):
        self.apikey = apikey
        self.latitude = latitude
        self.longitude = longitude
        self.time = time
        self.units = units

        self.get(latitude, longitude, time, units)

        # if 'timezone' in self.json:
        #    self.timezone = pytz.timezone(self.json['timezone'])

    def get(self, latitude=None, longitude=None, time=None, units=None):
        if time:
            time = int(time_mod.mktime(time.timetuple()))

        url = FORECAST_TEMPLATE.format(
            apikey=self.apikey,
            latitude=latitude or self.latitude,
            longitude=longitude or self.longitude,
            time=f",{time}" if self.time else "",
            units=units if units else "auto",
        )
        print(url)

        # TODO: check for 200's and valid apikey...
        request = requests.get(url, headers={"Accept-Encoding": "gzip"})
        print(request.status_code)

        self.json = request.json()

    def alerts(self):
        if "alerts" in self.json:
            alerts = []
            for alert in self.json["alerts"]:
                alerts.append(DataBlock(alert, self.timezone))
            return alerts
        return DataBlock()

    def currently(self):
        if "currently" in self.json:
            return DataBlock(self.json["currently"], self.timezone)
        return DataBlock()

    def daily(self):
        if "daily" in self.json:
            return DataBlock(self.json["daily"], self.timezone)
        return DataBlock()

    def hourly(self):
        if "hourly" in self.json:
            return DataBlock(self.json["hourly"], self.timezone)
        return DataBlock()

    def minutely(self):
        if "minutely" in self.json:
            return DataBlock(self.json["minutely"], self.timezone)
        return DataBlock()

    def offset(self):
        if "offset" in self.json:
            return self.json["offset"]
        return None

    @property
    def timezone(self):
        if "timezone" in self.json:
            return pytz.timezone(self.json["timezone"])
        return None

    def get_alerts(self):
        warnings.warn("deprecated", DeprecationWarning)
        return self.alerts

    def get_currently(self):
        warnings.warn("deprecated", DeprecationWarning)
        return self.currently

    def get_daily(self):
        warnings.warn("deprecated", DeprecationWarning)
        return self.daily

    def get_hourly(self):
        warnings.warn("deprecated", DeprecationWarning)
        return self.hourly

    def get_minutely(self):
        warnings.warn("deprecated", DeprecationWarning)
        return self.minutely
