import unittest
from unittest.mock import patch
from src.weather_client import WeatherClient, WeatherAPIError

class TestWeatherClient(unittest.TestCase):

    @patch("src.weather_client.requests.get")
    def test_current_weather_success(self, mock_get):
        mock_resp = mock_get.return_value
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "name": "TestCity",
            "weather": [{"main": "Clear", "description": "clear sky"}],
            "main": {"temp": 25}
        }
        client = WeatherClient(api_key="fake")
        data = client.current_weather("TestCity")
        self.assertEqual(data["name"], "TestCity")

    @patch("src.weather_client.requests.get")
    def test_non_200_error(self, mock_get):
        mock_resp = mock_get.return_value
        mock_resp.status_code = 401
        mock_resp.json.return_value = {"message": "Invalid API key"}
        client = WeatherClient(api_key="fake")
        with self.assertRaises(WeatherAPIError):
            client.current_weather("TestCity")

if __name__ == "__main__":
    unittest.main()
