from .plotting import plot_metrics_by_city, save_plot
from .processing import monthly_aggregate, response_to_df
from .services import get_data_meteo_api


def main():
    city_frames = {}

    for city in ["Madrid", "London", "Rio"]:
        wr = get_data_meteo_api(city)
        df_mensual = monthly_aggregate(response_to_df(wr))
        city_frames[city] = df_mensual

    fig = plot_metrics_by_city(city_frames)
    save_plot(fig, "weather_metrics_by_city.png")


if __name__ == "__main__":
    main()
