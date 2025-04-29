from typing import Dict
from pandas import DataFrame
import matplotlib.pyplot as plt

_METRICS = {
    "temperature_2m_mean": "Monthly Mean Temperature (°C)",
    "precipitation_sum": "Monthly Total Precipitation (mm)",
    "wind_speed_10m_max": "Monthly Maximum Wind Speed (m/s)",
}


def plot_metrics_by_city(dfs: Dict[str, DataFrame]):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 15), sharex=True)

    for ax, (col, title) in zip(axes, _METRICS.items()):
        for city, df in dfs.items():
            idx = df.index.to_timestamp()  # type: ignore
            ax.plot(idx, df[col].values, label=city)
        ax.set_title(title)
        ax.legend()

    axes[-1].set_xlabel("Fecha")
    return fig


def save_plot(fig: plt.Figure, filename: str):
    fig.savefig(filename, dpi=300)
