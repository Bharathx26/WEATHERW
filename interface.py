import tkinter as tk
from tkinter import messagebox
from src.weather_client import WeatherClient, WeatherAPIError
from src.utils import load_env

load_env()


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


root = tk.Tk()
root.title("WeatherW")
root.geometry("400x350")

tk.Label(root, text="City:").pack()
city_entry = tk.Entry(root, width=30)
city_entry.pack()

tk.Label(root, text="Country Code (optional):").pack()
country_entry = tk.Entry(root, width=30)
country_entry.pack()

get_btn = tk.Button(root, text="Get Weather", command=get_weather)
get_btn.pack(pady=10)

output_text = tk.Text(root, height=10, width=45)
output_text.pack()

root.mainloop()
