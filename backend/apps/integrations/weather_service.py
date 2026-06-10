import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

BAD_CONDITIONS = {"Rain", "Drizzle", "Thunderstorm", "Snow", "Fog", "Mist", "Haze"}


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, latitude: float, longitude: float) -> dict:
        api_key = getattr(settings, "OPENWEATHER_API_KEY", "")
        if not api_key:
            return self._neutral()

        try:
            resp = requests.get(
                self.BASE_URL,
                params={"lat": latitude, "lon": longitude, "appid": api_key, "units": "metric"},
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()

            condition = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            is_outdoor_friendly = condition not in BAD_CONDITIONS and temp >= 10

            return {
                "temperature": round(temp, 1),
                "condition": condition,
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "is_outdoor_friendly": is_outdoor_friendly,
            }
        except Exception as exc:
            logger.warning("WeatherService error: %s", exc)
            return self._neutral()

    def _neutral(self) -> dict:
        return {
            "temperature": None,
            "condition": None,
            "description": None,
            "humidity": None,
            "wind_speed": None,
            "is_outdoor_friendly": None,
        }


weather_service = WeatherService()
