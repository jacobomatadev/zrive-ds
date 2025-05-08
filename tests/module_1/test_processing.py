from src.module_1.processing import response_to_df, monthly_aggregate
from src.module_1.models import WeatherResponse


def test_response_to_df(sample_payload):
    resp = WeatherResponse(**sample_payload)
    df = response_to_df(resp)
    assert list(df.columns) == [
        "temperature_2m_mean",
        "precipitation_sum",
        "wind_speed_10m_max",
    ]
    # índice debe ser datetime y con 3 filas
    assert df.index.dtype.kind == "M"
    assert len(df) == 3


def test_monthly_aggregate(sample_payload):
    resp = WeatherResponse(**sample_payload)
    df_daily = response_to_df(resp)
    df_month = monthly_aggregate(df_daily)

    # January: (10+14)/2 = 12   | 0+5 = 5 | max(3,4)=4
    jan = df_month.loc["2020-01"]
    assert jan["temperature_2m_mean"] == 12
    assert jan["precipitation_sum"] == 5
    assert jan["wind_speed_10m_max"] == 4

    # Febrero: valores únicos
    feb = df_month.loc["2020-02"]
    assert feb["temperature_2m_mean"] == 8
    assert feb["precipitation_sum"] == 2
    assert feb["wind_speed_10m_max"] == 6
