import argparse
import sys
from .weather_client import WeatherAPIError, WeatherClient
from .utils import load_env


def pretty_current(data: dict) -> str:
    """Render current weather details as printable text."""
    name = data.get("name", "")
    sys_info = data.get("sys", {}) or {}
    weather_list = data.get("weather", []) or []
    weather = weather_list[0] if weather_list else {}
    main = data.get("main", {}) or {}
    wind = data.get("wind", {}) or {}

    lines = [
        f"Location: {name}, {sys_info.get('country', '')}",
        f"Weather: {weather.get('main', '')} - {weather.get('description', '')}",
        f"Temperature: {main.get('temp')}°",
        f"Feels like: {main.get('feels_like')}°",
        f"Humidity: {main.get('humidity')}%",
        f"Pressure: {main.get('pressure')} hPa",
        f"Wind: {wind.get('speed')} m/s",
    ]
    return "\n".join(lines)


def pretty_forecast(data: dict, limit: int = 5) -> str:
    """Render forecast list as printable text."""
    city_info = data.get("city", {}) or {}
    city = city_info.get("name", "")
    country = city_info.get("country", "")
    lines = [f"Forecast for {city}, {country}:"]
    count = 0

    for entry in data.get("list", []):
        dt_txt = entry.get("dt_txt")
        weather = entry.get("weather", [{}])[0]
        main = entry.get("main", {})

        lines.append(
            f" - {dt_txt}: {weather.get('main')} ({weather.get('description')}) - {main.get('temp')}°"
        )
        count += 1
        if count >= limit:
            break
    return "\n".join(lines)

def parse_args():
    parser = argparse.ArgumentParser(description="WeatherWatch CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_now = sub.add_parser("current")
    p_now.add_argument("city")
    p_now.add_argument("--country", default=None)
    p_now.add_argument("--units", default="metric", choices=["metric", "imperial","standard"])
    p_fc = sub.add_parser("forecast")
    p_fc.add_argument("city")
    p_fc.add_argument("--country", default=None)
    p_fc.add_argument("--units", default="metric", choices=["metric", "imperial","standard"])
    p_fc.add_argument("--limit", type=int, default=5)

    return parser.parse_args()

def main():
    load_env()
    args = parse_args()
    
    try:
        client = WeatherClient()
    except Exception as e:
        print(f"Configuration error: {e}")
        return 2
    
    try:
        if args.cmd == "current":
            data = client.current_weather(args.city, args.country, args.units)
            print(pretty_current(data))

        elif args.cmd == "forecast":
            data = client.forecast(args.city, args.country, args.units)
            print(pretty_forecast(data, args.limit))
    except WeatherAPIError as e:
        print(f"API Error: {e}")
        return 1
    except ValueError as e:
        print(f"Input Error: {e}")
        return 1
    
if __name__ == "__main__":
    main()
    