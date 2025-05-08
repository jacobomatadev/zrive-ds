import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

API_URL = "https://archive-api.open-meteo.com/v1/archive?"


class WeatherAPIError(Exception):
    def __init__(self, response: requests.Response):
        reason = response.json().get("reason", "Unknown error")
        super().__init__(f"API Error: {response.status_code} - {reason}")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2),
    retry=retry_if_exception_type(requests.RequestException),
)
def call_api(params: dict) -> dict:
    resp = requests.get(API_URL, params=params, timeout=10)
    content_type = resp.headers.get("Content-Type", "")
    if resp.status_code == 400 and "application/json" in content_type:
        raise WeatherAPIError(resp)
    resp.raise_for_status()
    return resp.json()
