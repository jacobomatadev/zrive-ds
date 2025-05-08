import pytest
import requests

from src.module_1.models import WeatherResponse
from src.module_1.services import VARIABLES, get_data_meteo_api


def test_get_data_meteo_api_parses(monkeypatch, sample_payload):
    def fake_call(params):
        assert params["daily"] == VARIABLES
        return sample_payload

    monkeypatch.setattr("src.module_1.services.call_api", fake_call)
    wr = get_data_meteo_api("Madrid")
    assert isinstance(wr, WeatherResponse)
    assert wr.latitude == sample_payload["latitude"]


def test_get_data_meteo_api_raises(monkeypatch):
    def fake_call(params):
        raise requests.exceptions.HTTPError("API Error")

    monkeypatch.setattr("src.module_1.services.call_api", fake_call)
    with pytest.raises(requests.exceptions.HTTPError):
        get_data_meteo_api("Madrid")


def test_get_data_meteo_api_bad_city():
    with pytest.raises(KeyError):
        get_data_meteo_api("Atlantis")
