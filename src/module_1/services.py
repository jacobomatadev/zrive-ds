from .models import WeatherResponse
from .api_client import call_api


COORDINATES = {
    "Madrid": {"latitude": 40.416775, "longitude": -3.703790},
    "London": {"latitude": 51.507351, "longitude": -0.127758},
    "Rio": {"latitude": -22.906847, "longitude": -43.172896},
}
VARIABLES = ["temperature_2m_mean", "precipitation_sum", "wind_speed_10m_max"]
START_DATE = "2010-01-01"
END_DATE = "2020-01-01"


def get_data_meteo_api(city: str) -> WeatherResponse:
    coords = COORDINATES.get(city)
    if not coords:
        raise KeyError(f"City '{city}' not found in coordinates dictionary.")

    params = {
        "latitude": coords["latitude"],
        "longitude": coords["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": VARIABLES,
        "timezone": "Europe/Madrid",
    }
    raw = call_api(params)
    return WeatherResponse(**raw)
