import os
import requests
from typing import Optional, Dict

class WeatherAPIError(Exception):
    """Raised when the weather API returns an error or bad response."""
    pass

class WeatherClient:
    """Client for interacting with the OpenWeatherMap API."""
    def __init__(self, api_key: Optional[str] = None,
                 base_url: str = "https://api.openweathermap.org/data/2.5"):
    
        
        key = api_key or os.getenv("OPENWEATHER_API_KEY")

        if not key:
            raise ValueError(
                "API key not provided. Set OPENWEATHER_API_KEY in your .env file."
            )

        self.api_key = key
        self.base_url = base_url.rstrip("/")

    def _get(self, endpoint: str, params: Dict) -> Dict:
        """Internal helper for making GET requests with error handling."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        params = dict(params)
        params["appid"] = self.api_key

        try:
            resp = requests.get(url, params=params, timeout=10)
        except requests.RequestException as e:
            raise WeatherAPIError(f"Network error: {e}") from e

        if resp.status_code != 200:
            try:
                error_json = resp.json()
                msg = error_json.get("message", resp.text)
            except ValueError:
                msg = resp.text
            raise WeatherAPIError(f"API error ({resp.status_code}): {msg}")

        try:
            return resp.json()
        except ValueError:
            raise WeatherAPIError("Invalid JSON from API")

    def current_weather(self, city: str, country: Optional[str] = None,
                        units: str = "metric") -> Dict:

        q = city if not country else f"{city},{country}"
        params = {"q": q, "units": units}

        return self._get("weather", params)

    def forecast(self, city: str, country: Optional[str] = None,
                 units: str = "metric", cnt: Optional[int] = None) -> Dict:

        q = city if not country else f"{city},{country}"
        params = {"q": q, "units": units}

        if cnt:
            params["cnt"] = cnt

        return self._get("forecast", params)

    def air_quality(self, city: str, country: Optional[str] = None) -> Dict:
        """Fetch AQI data using coordinates from the weather endpoint."""
        q = city if not country else f"{city},{country}"

        weather_data = self._get("weather", {"q": q})
        coord = weather_data.get("coord")

        if not coord or "lat" not in coord or "lon" not in coord:
            raise WeatherAPIError("Could not get coordinates for AQI lookup.")

        lat = coord["lat"]
        lon = coord["lon"]

     
        return self._get("air_pollution", {"lat": lat, "lon": lon})
