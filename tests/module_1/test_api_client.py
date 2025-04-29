import requests
import pytest

from src.module_1.api_client import WeatherAPIError, call_api


class DummyResponse:
    def __init__(self, data, status=200, content_type="application/json"):
        self._data = data
        self.status_code = status
        self.headers = {"Content-Type": content_type}

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code} Error")

    def json(self):
        return self._data


def test_get_meteo_api_raises(monkeypatch, error_payload):
    def fake_error_get(*_, **__):
        return DummyResponse(error_payload, status=400)

    monkeypatch.setattr("src.module_1.api_client.requests.get", fake_error_get)
    with pytest.raises(WeatherAPIError) as e:
        call_api({"latitude": 40.4168, "longitude": -3.7038})
        assert str(e.value) == f"API Error: 400 - {error_payload['reason']}"
