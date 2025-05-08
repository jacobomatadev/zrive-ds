from datetime import date
from typing import Dict, List

from pydantic import BaseModel


class Daily(BaseModel):
    time: List[date]
    temperature_2m_mean: List[float]
    precipitation_sum: List[float]
    wind_speed_10m_max: List[float]


class WeatherResponse(BaseModel):
    latitude: float
    longitude: float
    elevation: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    daily_units: Dict[str, str]
    daily: Daily
