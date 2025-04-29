import pandas as pd
from .models import WeatherResponse

_AGG = {
    "temperature_2m_mean": "mean",
    "precipitation_sum": "sum",
    "wind_speed_10m_max": "max",
}


def response_to_df(resp: WeatherResponse) -> pd.DataFrame:
    df = pd.DataFrame(resp.daily.model_dump())
    df["time"] = pd.to_datetime(df["time"])
    return df.set_index("time")


def monthly_aggregate(df: pd.DataFrame) -> pd.DataFrame:
    return df.resample("ME").agg(_AGG).to_period("M")  # type: ignore
