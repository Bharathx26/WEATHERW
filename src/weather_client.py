import os
from typing import Dict, Optional

import requests


class WeatherAPIError(Exception):
    """Raised when the weather API returns an error or bad response."""


class WeatherClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.openweathermap.org/data/2.5",
    ):
        """
        Simple client for OpenWeatherMap API.

        api_key: API key string; falls back to OPENWEATHER_API_KEY env var.
        base_url: Base API URL; defaults to OpenWeatherMap v2.5 base.
        """
        if api_key is None:
            api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is not provided. Set OPENWEATHER_API_KEY in environment variables."
            )

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _get(self, endpoint: str, params: Dict) -> Dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        params = dict(params)
        params["appid"] = self.api_key

        try:
            resp = requests.get(url, params=params, timeout=10)
        except requests.RequestException as e:
            raise WeatherAPIError(f"Network error: {e}") from e

        if resp.status_code != 200:
            try:
                err_json = resp.json()
                msg = err_json.get("message") or resp.text
            except ValueError:
                msg = resp.text
            raise WeatherAPIError(f"API error ({resp.status_code}): {msg}")

        try:
            return resp.json()
        except ValueError:
            raise WeatherAPIError("Invalid JSON response")

    def current_weather(
        self, city: str, country: Optional[str] = None, units: str = "metric"
    ) -> Dict:
        if not city:
            raise ValueError("City name is required.")

        q = city if not country else f"{city},{country}"
        params = {"q": q, "units": units}

        return self._get("weather", params)

    def forecast(
        self,
        city: str,
        country: Optional[str] = None,
        units: str = "metric",
        cnt: Optional[int] = None,
    ) -> Dict:
        if not city:
            raise ValueError("City name is required.")

        q = city if not country else f"{city},{country}"
        params = {"q": q, "units": units}

        if cnt:
            params["cnt"] = cnt

        return self._get("forecast", params)
