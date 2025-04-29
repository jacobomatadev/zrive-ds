import time

import pytest


@pytest.fixture
def sample_payload():
    return {
        "latitude": 40.4,
        "longitude": -3.7,
        "elevation": 667.0,
        "generationtime_ms": 12.3,
        "utc_offset_seconds": 0,
        "timezone": "Europe/Madrid",
        "timezone_abbreviation": "CET",
        "daily_units": {
            "time": "iso8601",
            "temperature_2m_mean": "°C",
            "precipitation_sum": "mm",
            "wind_speed_10m_max": "m/s",
        },
        "daily": {
            "time": ["2020-01-01", "2020-01-15", "2020-02-03"],
            "temperature_2m_mean": [10, 14, 8],
            "precipitation_sum": [0, 5, 2],
            "wind_speed_10m_max": [3, 4, 6],
        },
    }


@pytest.fixture
def error_payload():
    return {
        "error": "true",
        "reason": "Cannot initialize WeatherVariable from invalid String value",
    }


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    """Evita esperas reales en tenacity (y en cualquier otro sleep)."""
    monkeypatch.setattr(time, "sleep", lambda *_: None)
