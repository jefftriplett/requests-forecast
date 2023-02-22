import httpretty

# from datetime import datetime
# from dirty_equals import IsPartialDict
from dirty_equals import IsListOrTuple

from requests_forecast import Forecast


API_KEY = "1234"
LATITUDE = 38.9717
LONGITUDE = -95.235
API_URL = "https://weathermachine.io/api/?apiKey={}&lat={}&lon={}".format(
    API_KEY, LATITUDE, LONGITUDE
)


@httpretty.activate
def test_alerts():
    body_fixture = open("test/fixtures/alerts.json").read()
    httpretty.register_uri(
        httpretty.GET, API_URL, body=body_fixture, content_type="text/json"
    )

    forecast = Forecast(API_KEY, latitude=LATITUDE, longitude=LONGITUDE)
    alerts = forecast.alerts()

    assert len(alerts) == 1
    assert alerts[0]["title"] == "Freeze Warning for Marin, CA"
    # assert str(alerts[0]["time"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 12, 12, 1, 8))
    # )
    # assert str(alerts[0]["expires"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 12, 12, 17, 0))
    # )


@httpretty.activate
def test_currently():
    body_fixture = open("test/fixtures/full.json").read()
    httpretty.register_uri(
        httpretty.GET, API_URL, body=body_fixture, content_type="text/json"
    )

    forecast = Forecast(API_KEY, latitude=LATITUDE, longitude=LONGITUDE)

    currently = forecast.currently()

    assert list(currently.keys()) == IsListOrTuple(
        "apparentTemperature",
        "aqi",
        "cloudCover",
        "dewPoint",
        "humidity",
        "icon",
        "pressure",
        "pressureTrend",
        "summary",
        "temperature",
        "uvIndex",
        "visibility",
        "windBearing",
        "windGust",
        "windSpeed",
        check_order=False,
    )

    assert currently["temperature"] == 66.1
    assert currently.temperature == 66.1

    assert currently["summary"] == "Drizzle"
    assert currently.summary == "Drizzle"

    # assert str(currently["time"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 29, 0, 8, 25))
    # )


@httpretty.activate
def test_daily():
    body_fixture = open("test/fixtures/full.json").read()
    httpretty.register_uri(
        httpretty.GET, API_URL, body=body_fixture, content_type="text/json"
    )

    forecast = Forecast(API_KEY, latitude=LATITUDE, longitude=LONGITUDE)
    daily = forecast.daily()

    assert len(daily.keys()) == 2
    assert list(daily.keys()) == IsListOrTuple(
        "data",
        "summary",
        check_order=False,
    )

    assert (
        daily.summary
        == "Mixed precipitation throughout the week, with temperatures falling to 39Â°F on Saturday."
    )
    assert (
        daily["summary"]
        == "Mixed precipitation throughout the week, with temperatures falling to 39Â°F on Saturday."
    )

    assert len(daily["data"][0].keys()) == 27
    assert list(daily["data"][0].keys()) == IsListOrTuple(
        "apparentTemperatureMax",
        "apparentTemperatureMin",
        "aqi",
        "cloudCover",
        "dewPoint",
        "humidity",
        "icon",
        "moonPhase",
        "moonPhaseName",
        "pollenGrass",
        "pollenTree",
        "pollenWeed",
        "precipAccumulation",
        "precipIntensity",
        "precipProbability",
        "precipType",
        "pressure",
        "summary",
        "sunriseTime",
        "sunsetTime",
        "temperatureMax",
        "temperatureMin",
        "time",
        "uvIndex",
        "visibility",
        "windBearing",
        "windSpeed",
        check_order=False,
    )

    assert daily["data"][0]["temperatureMax"] == 66.35
    assert daily["data"][0]["temperatureMin"] == 52.08

    # assert str(daily["data"][0]["time"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 28, 5, 0))
    # )
    # assert str(daily["data"][0]["sunriseTime"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 28, 12, 12, 29))
    # )
    # assert str(daily["data"][0]["sunsetTime"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 29, 00, 41, 39))
    # )

    # assert str(daily["data"][0]["temperatureMaxTime"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 28, 21, 0))
    # )
    # assert str(daily["data"][0]["temperatureMinTime"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 28, 12, 0))
    # )


@httpretty.activate
def test_hourly():
    body_fixture = open("test/fixtures/full.json").read()
    httpretty.register_uri(
        httpretty.GET, API_URL, body=body_fixture, content_type="text/json"
    )

    forecast = Forecast(API_KEY, latitude=LATITUDE, longitude=LONGITUDE)
    hourly = forecast.hourly()

    assert len(hourly.keys()) == 2
    assert list(hourly.keys()) == IsListOrTuple("data", "summary", check_order=False)

    assert (
        hourly["summary"]
        == "Rain starting later this afternoon, continuing until this evening."
    )

    assert len(hourly["data"][0].keys()) == 17
    assert list(hourly["data"][0].keys()) == IsListOrTuple(
        "apparentTemperature",
        "cloudCover",
        "dewPoint",
        "humidity",
        "icon",
        "precipAccumulation",
        "precipIntensity",
        "precipProbability",
        "precipType",
        "pressure",
        "summary",
        "temperature",
        "time",
        "uvIndex",
        "visibility",
        "windBearing",
        "windSpeed",
        check_order=False,
    )

    assert hourly["data"][0]["temperature"] == 66.2
    # assert str(hourly["data"][0]["time"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 29, 0, 0))
    # )


@httpretty.activate
def test_minutely():
    body_fixture = open("test/fixtures/full.json").read()
    httpretty.register_uri(
        httpretty.GET, API_URL, body=body_fixture, content_type="text/json"
    )

    forecast = Forecast(API_KEY, latitude=LATITUDE, longitude=LONGITUDE)
    minutely = forecast.minutely()

    # assert "data" in minutely.keys()
    # assert "icon" in minutely.keys()
    # assert "summary" in minutely.keys()

    assert len(minutely.keys()) == 2
    assert list(minutely.keys()) == IsListOrTuple("data", "summary", check_order=False)

    # assert minutely["icon"] == "partly-cloudy-day"
    assert (
        minutely["summary"]
        == "Light rain stopping in 13 min., starting again 30 min. later."
    )

    assert len(minutely["data"]) == 60
    assert list(minutely["data"][0].keys()) == IsListOrTuple(
        "precipIntensity", "precipType", "time", check_order=False
    )

    # assert str(minutely["data"][0]["time"].astimezone(pytz.utc)) == str(
    #     pytz.utc.localize(datetime(2013, 3, 29, 0, 8))
    # )
