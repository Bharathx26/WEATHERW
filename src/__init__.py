import os
from typing import Optional, Dict

def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.openweathermap.org/data/2.5"):
    
    key = api_key or os.getenv("OPENWEATHER_API_KEY")

    if not key:
        raise ValueError("API key not provided. Set OPENWEATHER_API_KEY in your .env file.")

    self.api_key = key
    self.base_url = base_url.rstrip("/")
