from datetime import datetime
from typing import Dict

import requests

from django.core.cache import cache
from rest_framework.exceptions import APIException

from weather_project import ENV__BASE_URL, ENV__WEATHER_API_KEY


def get_current_weather(city: str) -> Dict[str, str] | float:
    key = f"current_{city}"
    if cached := cache.get(key):
        return cached

    try:
        response = requests.get(
            f"{ENV__BASE_URL}/weather",
            params={"q": city, "appid": ENV__WEATHER_API_KEY, "units": "metric"},
        )
        data = response.json()
        if response.status_code != 200:
            raise APIException(data.get("message", "City not found"))

        result: Dict[str, str | float] = {
            "temperature": data["main"]["temp"],
            "local_time": datetime.utcfromtimestamp(
                data["dt"] + data["timezone"]
            ).strftime("%H:%M"),
        }
        cache.set(key, result, timeout=60)
        return result
    except Exception as e:
        raise APIException(str(e))


def get_forecast_weather(city: str, date: str) -> Dict[str, float]:
    key = f"forecast_{city}_{date}"
    if cached := cache.get(key):
        return cached

    try:
        response = requests.get(
            f"{ENV__BASE_URL}/forecast",
            params={"q": city, "appid": ENV__WEATHER_API_KEY, "units": "metric"},
        )
        data = response.json()
        if response.status_code != 200:
            raise APIException(data.get("message", "City not found"))

        target = datetime.strptime(date, "%d.%m.%Y").date()
        temps = [
            entry["main"]["temp"]
            for entry in data["list"]
            if datetime.fromtimestamp(entry["dt"]).date() == target
        ]

        if not temps:
            raise APIException("No forecast data available for this date")

        result: Dict[str, float] = {
            "min_temperature": min(temps),
            "max_temperature": max(temps),
        }
        cache.set(key, result, timeout=3600)
        return result
    except Exception as e:
        raise APIException(str(e))
