import tkinter as tk
from tkinter import messagebox
from src.weather_client import WeatherClient, WeatherAPIError
from src.utils import load_env

load_env()
client = WeatherClient()

def get_weather():
    city = city_entry.get().strip()
    country = country_entry.get().strip()

    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return

    try:
        client = WeatherClient()
        data = client.current_weather(city, country if country else None)
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        return

   
    result = []
    result.append(f"Location: {data.get('name')}, {data.get('sys', {}).get('country', '')}")
    result.append(f"Weather: {data['weather'][0]['description']}")
    result.append(f"Temperature: {data['main']['temp']}°C")
    result.append(f"Feels like: {data['main']['feels_like']}°C")
    result.append(f"Humidity: {data['main']['humidity']}%")
    result.append(f"Wind: {data['wind']['speed']} m/s")

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(result))

    
def get_aqi():
    city = city_entry.get()
    country = country_entry.get()

    if not city:
        messagebox.showwarning("Input Error", "City name is required.")
        return

    try:
        data = client.air_quality(city, country)
    except WeatherAPIError as e:
        messagebox.showerror("API Error", str(e))
        return

    item = data["list"][0]
    main = item["main"]
    comp = item["components"]

    AQI_LABELS = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    aqi_val = main["aqi"]
    label = AQI_LABELS.get(aqi_val, "Unknown")

    result = (
        f"AQI for {city}, {country or ''}: {aqi_val} ({label})\n\n"
        f"PM2.5: {comp['pm2_5']}\n"
        f"PM10: {comp['pm10']}\n"
        f"O₃: {comp['o3']}\n"
        f"NO₂: {comp['no2']}\n"
        f"SO₂: {comp['so2']}\n"
        f"CO: {comp['co']}\n"
    )

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

    
def get_forecast():
    city = city_entry.get()
    country = country_entry.get()

    if not city:
        messagebox.showwarning("Input Error", "City name is required.")
        return

    try:
        data = client.forecast(city, country or None, units="metric", cnt=5)
    except WeatherAPIError as e:
        messagebox.showerror("API Error", str(e))
        return

    city_info = data.get("city", {})
    name = city_info.get("name", "")
    c_code = city_info.get("country", "")

    lines = [f"Forecast for {name}, {c_code} (next 5 entries):\n"]

    for entry in data.get("list", [])[:5]:
        dt_txt = entry.get("dt_txt", "")
        main = entry.get("main", {})
        weather = entry.get("weather", [{}])[0]
        lines.append(
            f"{dt_txt}: {weather.get('main', '')} "
            f"({weather.get('description', '')}) — {main.get('temp', '')}°C"
        )

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(lines))


    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "\n".join(lines))


root = tk.Tk()
root.title("WeatherW")
root.geometry("550x500")

tk.Label(root, text="City:").pack()
city_entry = tk.Entry(root, width=40)
city_entry.pack()

tk.Label(root, text="Country Code (optional):").pack()
country_entry = tk.Entry(root, width=40)
country_entry.pack()

get_btn = tk.Button(root, text="Get Weather", command=get_weather)
get_btn.pack(pady=10)

get_btn = tk.Button(root, text="Get AQI", command=get_aqi)
get_btn.pack(pady=5)

get_btn = tk.Button(root, text="Get Forecast", command=get_forecast)
get_btn.pack(pady=5)


output_text = tk.Text(root, height=12, width=60)
output_text.pack()

root.mainloop()
