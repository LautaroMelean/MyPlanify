import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

BAD_CONDITIONS = {"Rain", "Drizzle", "Thunderstorm", "Snow", "Fog", "Mist", "Haze"}
CACHE_TTL = 900  # 15 minutes


class OpenWeatherProvider:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    TIMEOUT = 3

    def get_current_weather(self, latitude: float, longitude: float) -> dict | None:
        lat_r = round(latitude, 2)
        lon_r = round(longitude, 2)
        cache_key = f"weather:{lat_r}:{lon_r}"

        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        api_key = getattr(settings, "OPENWEATHER_API_KEY", "")
        if not api_key:
            return None

        try:
            resp = requests.get(
                self.BASE_URL,
                params={"lat": lat_r, "lon": lon_r, "appid": api_key, "units": "metric"},
                timeout=self.TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()

            condition = data["weather"][0]["main"]
            temp = data["main"]["temp"]
            result = {
                "temperature": round(temp, 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "condition": condition,
                "humidity": data["main"]["humidity"],
                "wind_speed": round(data["wind"]["speed"], 1),
                "clouds": data.get("clouds", {}).get("all", 0),
                "is_outdoor_friendly": condition not in BAD_CONDITIONS and temp >= 10,
            }
            cache.set(cache_key, result, CACHE_TTL)
            return result

        except Exception as exc:
            logger.warning("OpenWeatherProvider error [%s,%s]: %s", lat_r, lon_r, exc)
            return None


openweather_provider = OpenWeatherProvider()
