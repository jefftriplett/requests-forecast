import pytz
import requests

from datetime import datetime

# from pydantic import BaseModel


__author__ = "Jeff Triplett"
__copyright__ = "Copyright 2013-2021 Jeff Triplett"
__license__ = "BSD"
__title__ = "requests-forecast"
__version__ = "1.0.0"


FORECAST_TEMPLATE = (
    "https://weathermachine.io/api/"
    "?apiKey={apikey}"
    "&lat={latitude}"
    "&lon={longitude}"
    "&output={output}"
    "&source={source}"
    "&units={units}"
)

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

# TODO: Refactor to use BaseModel
# class DataPoint(BaseModel):
#     apparentTemperature: float
#     apparentTemperatureMax: float
#     apparentTemperatureMin: float
#     aqi: int
#     cloudCover: float
#     dewPoint: float
#     humidity: float
#     icon: str
#     moonPhase: float
#     moonPhaseName: str
#     pollenGrass: int
#     pollenTree: int
#     pollenWeed: int
#     precipAccumulation: float
#     precipIntensity: float
#     precipProbability: float
#     precipType: str
#     pressure: float
#     pressureTrend: str
#     summary: str
#     sunriseTime: datetime
#     sunsetTime: datetime
#     temperature: float
#     temperatureMax: float
#     temperatureMin: float
#     time: datetime
#     uvIndex: int
#     visibility: float
#     windBearing: int
#     windGust: float
#     windSpeed: float


# class DataBlock(BaseModel):
#     data: list[DataPoint]
#     summary: str


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

    def __init__(
        self,
        apikey: str,
        latitude: float = None,
        longitude: float = None,
        output: str = None,
        source: str = None,
        units: str = None,
    ):
        self.apikey = apikey
        self.latitude = latitude
        self.longitude = longitude
        self.output = output
        self.source = source
        self.units = units

        self.get(latitude=latitude, longitude=longitude, units=units)

        # if 'timezone' in self.json:
        #    self.timezone = pytz.timezone(self.json['timezone'])

    def get(
        self,
        *,
        latitude: float = None,
        longitude: float = None,
        output: str = None,
        source: str = None,
        units: str = None,
    ):
        url = FORECAST_TEMPLATE.format(
            apikey=self.apikey,
            latitude=latitude or self.latitude,
            longitude=longitude or self.longitude,
            output=output if output else "base",
            source=source if source else "mock",
            units=units if units else "us",
        )

        request = requests.get(url, headers={"Accept-Encoding": "gzip"})
        request.raise_for_status()

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
