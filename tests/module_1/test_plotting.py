import matplotlib
import matplotlib.pyplot as plt

from src.module_1.plotting import plot_metrics_by_city
from src.module_1.processing import monthly_aggregate, response_to_df
from src.module_1.models import WeatherResponse

matplotlib.use("Agg")


def test_returns_figure_with_three_axes(sample_payload):
    city_frames = {
        "Madrid": monthly_aggregate(response_to_df(WeatherResponse(**sample_payload))),
        "London": monthly_aggregate(response_to_df(WeatherResponse(**sample_payload))),
        "Rio": monthly_aggregate(response_to_df(WeatherResponse(**sample_payload))),
    }
    fig = plot_metrics_by_city(city_frames)
    assert isinstance(fig, matplotlib.figure.Figure)
    assert len(fig.axes) == 3

    plt.close(fig)
