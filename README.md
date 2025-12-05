
## Notes: WeatherW

WeatherW is a Python app that uses the OPENWEATHERMAP REST API to fetch reaal time weather information.
It supports both CLI and GUI(GUI was made by Tkinter)

Usage:
-Command Line Interface(CLI)
-Graphical User Interface(GUI)

To use the CLI:
-It allows you to fetch CURRENT WEATHER and FORECAST directly from the terminal without the use of GUI.
-Environment Variables should be activated and .env file should be available.
-Use the command(in gitbash) -> **python -m src.main current "Name of the city" --country countrycodehere --units metric/imperial/standard** to fetch the currrent weather.
-Use the command(in gitbash) -> **python -m src.main current "Name of the city" --country countrycodehere --limit no.ofdays --units metric/imperial/standard** to fetch the forecast of the upcoming days.

To use the GUI:
-It allows you to fetch CURRENT WEATHER and FORECAST from the GUI initiated from the CLI.
-Initiation of GUI- Use the command(in gitbash) -> **python -m interface**
-A Window appears with a TextField, Enter the asked components and the results will appear in the Result box.


Features are:
-Can fetch Temperature of any city
-The "Feels-like" Temperature can be fetched as well
-Humidity
-Weather conditions
-Wind speed
-Supports metric, imperial, standard units

GUI:
-Asks for City
-Country Code, which is optional
and upon entering the details, results are displayed in the textbox.

Included Error Handling, sush as:
-Invalid Input
-Netwwork Errors
-Non-200 response codes

