from datetime import date

import pytest
from pydantic import ValidationError

from src.module_1.models import Daily, WeatherResponse


def test_weatherresponse_parses(sample_payload):
    weather_response = WeatherResponse(**sample_payload)
    assert isinstance(weather_response, WeatherResponse)


def test_daily_model_parses_dates_and_lists(sample_payload):
    daily = Daily(**sample_payload["daily"])
    assert isinstance(daily.time[0], date)
    assert daily.temperature_2m_mean == sample_payload["daily"]["temperature_2m_mean"]
    assert daily.precipitation_sum == sample_payload["daily"]["precipitation_sum"]
    assert daily.wind_speed_10m_max == sample_payload["daily"]["wind_speed_10m_max"]


def test_weatherresponse_invalid_raises(sample_payload):
    bad = sample_payload.copy()
    bad.pop("daily")
    with pytest.raises(ValidationError):
        WeatherResponse(**bad)
