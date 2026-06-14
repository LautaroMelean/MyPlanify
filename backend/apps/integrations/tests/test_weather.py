from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.cache import cache

from apps.integrations.providers.openweather import OpenWeatherProvider


class OpenWeatherProviderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.provider = OpenWeatherProvider()

    def tearDown(self):
        cache.clear()

    def _mock_response(self, condition="Clear", temp=22.0, feels=20.0):
        mock = MagicMock()
        mock.raise_for_status = MagicMock()
        mock.json.return_value = {
            "weather": [{"main": condition, "description": condition.lower()}],
            "main": {"temp": temp, "feels_like": feels, "humidity": 60},
            "wind": {"speed": 5.0},
            "clouds": {"all": 10},
        }
        return mock

    @patch("apps.integrations.providers.openweather.requests.get")
    def test_returns_weather_data(self, mock_get):
        mock_get.return_value = self._mock_response()
        with self.settings(OPENWEATHER_API_KEY="test-key"):
            result = self.provider.get_current_weather(-34.6, -58.4)
        self.assertIsNotNone(result)
        self.assertEqual(result["condition"], "Clear")
        self.assertEqual(result["temperature"], 22.0)
        self.assertTrue(result["is_outdoor_friendly"])

    @patch("apps.integrations.providers.openweather.requests.get")
    def test_caches_result(self, mock_get):
        mock_get.return_value = self._mock_response()
        with self.settings(OPENWEATHER_API_KEY="test-key"):
            self.provider.get_current_weather(-34.60, -58.40)
            self.provider.get_current_weather(-34.60, -58.40)
        self.assertEqual(mock_get.call_count, 1)

    @patch("apps.integrations.providers.openweather.requests.get")
    def test_fallback_on_api_error(self, mock_get):
        mock_get.side_effect = Exception("timeout")
        with self.settings(OPENWEATHER_API_KEY="test-key"):
            result = self.provider.get_current_weather(-34.6, -58.4)
        self.assertIsNone(result)

    def test_returns_none_when_no_api_key(self):
        with self.settings(OPENWEATHER_API_KEY=""):
            result = self.provider.get_current_weather(-34.6, -58.4)
        self.assertIsNone(result)

    @patch("apps.integrations.providers.openweather.requests.get")
    def test_rain_is_not_outdoor_friendly(self, mock_get):
        mock_get.return_value = self._mock_response(condition="Rain", temp=15.0)
        with self.settings(OPENWEATHER_API_KEY="test-key"):
            result = self.provider.get_current_weather(-34.6, -58.4)
        self.assertFalse(result["is_outdoor_friendly"])

    @patch("apps.integrations.providers.openweather.requests.get")
    def test_cold_weather_is_not_outdoor_friendly(self, mock_get):
        mock_get.return_value = self._mock_response(condition="Clear", temp=5.0)
        with self.settings(OPENWEATHER_API_KEY="test-key"):
            result = self.provider.get_current_weather(-34.6, -58.4)
        self.assertFalse(result["is_outdoor_friendly"])
