import argparse
from .weather_client import WeatherClient, WeatherAPIError
from .utils import load_env

AQI_LABELS = {
    1: "Good",
    2: "Fair",
    3: "Moderate",
    4: "Poor",
    5: "Very Poor",
}

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


def pretty_aqi(data: dict, city: str, country) -> str:
    """Render Air Quality Index details as printable text."""
    city_display = city if not country else f"{city}, {country}"

    items = data.get("list", [])
    if not items:
        return f"No AQI data available for {city_display}"

    entry = items[0]
    main = entry.get("main", {})
    components = entry.get("components", {})

    aqi_value = main.get("aqi")
    label = AQI_LABELS.get(aqi_value, "Unknown")

    lines = [
        f"AQI for {city_display}: {aqi_value} ({label})",
        "",
        "Pollutant concentrations (µg/m³):",
        f"  PM2.5: {components.get('pm2_5')}",
        f"  PM10:  {components.get('pm10')}",
        f"  O₃:    {components.get('o3')}",
        f"  NO₂:   {components.get('no2')}",
        f"  SO₂:   {components.get('so2')}",
        f"  CO:    {components.get('co')}",
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
    p_now = sub.add_parser("current", help="Get current weather for a city")
    p_now.add_argument("city", help="City name (e.g. Hyderabad)")
    p_now.add_argument("--country", help="Country code (e.g. IN)", default=None)
    p_now.add_argument(
        "--units",
        default="metric",
        choices=["metric", "imperial", "standard"],
        help="Units system",
    )

    p_fc = sub.add_parser("forecast", help="Get forecast for a city")
    p_fc.add_argument("city", help="City name (e.g. Hyderabad)")
    p_fc.add_argument("--country", help="Country code (e.g. IN)", default=None)
    p_fc.add_argument(
        "--units",
        default="metric",
        choices=["metric", "imperial", "standard"],
        help="Units system",
    )
    p_fc.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of forecast entries to display",
    )

    p_aqi = sub.add_parser("aqi", help="Get Air Quality Index for a city")
    p_aqi.add_argument("city", help="City name (e.g. Hyderabad)")
    p_aqi.add_argument("--country", help="Country code (e.g. IN)", default=None)

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
            data = client.forecast(args.city, args.country, args.units, cnt=args.limit)
            print(pretty_forecast(data, args.limit))

        elif args.cmd == "aqi":
            data = client.air_quality(args.city, args.country)
            print(pretty_aqi(data, args.city, args.country))

    except WeatherAPIError as e:
        print(f"API Error: {e}")
        return 1
    except ValueError as e:
        print(f"Input Error: {e}")
        return 1


if __name__ == "__main__":
    main()
