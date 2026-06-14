from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.cache import cache

from apps.integrations.providers.google_places import GooglePlacesProvider


class GooglePlacesProviderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.provider = GooglePlacesProvider()

    def tearDown(self):
        cache.clear()

    def _mock_response(self, results=None):
        mock = MagicMock()
        mock.raise_for_status = MagicMock()
        mock.json.return_value = {"results": results or [
            {
                "place_id": "ChIJ_test_1",
                "name": "Parque Centenario",
                "vicinity": "Buenos Aires",
                "geometry": {"location": {"lat": -34.606, "lng": -58.435}},
                "types": ["park"],
                "price_level": 0,
            }
        ]}
        return mock

    @patch("apps.integrations.providers.google_places.requests.get")
    def test_search_nearby_returns_results(self, mock_get):
        mock_get.return_value = self._mock_response()
        with self.settings(GOOGLE_PLACES_API_KEY="test-key"):
            results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Parque Centenario")
        self.assertEqual(results[0]["source"], "google")
        self.assertEqual(results[0]["category"], "Parque")

    @patch("apps.integrations.providers.google_places.requests.get")
    def test_caches_nearby_results(self, mock_get):
        mock_get.return_value = self._mock_response()
        with self.settings(GOOGLE_PLACES_API_KEY="test-key"):
            self.provider.search_nearby(-34.60, -58.40)
            self.provider.search_nearby(-34.60, -58.40)
        self.assertEqual(mock_get.call_count, 1)

    def test_returns_empty_when_no_api_key(self):
        with self.settings(GOOGLE_PLACES_API_KEY=""):
            results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(results, [])

    @patch("apps.integrations.providers.google_places.requests.get")
    def test_fallback_on_api_error(self, mock_get):
        mock_get.side_effect = Exception("timeout")
        with self.settings(GOOGLE_PLACES_API_KEY="test-key"):
            results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(results, [])

    @patch("apps.integrations.providers.google_places.requests.get")
    def test_text_search_returns_results(self, mock_get):
        mock_get.return_value = self._mock_response()
        with self.settings(GOOGLE_PLACES_API_KEY="test-key"):
            results = self.provider.search_by_query("parque", -34.6, -58.4)
        self.assertEqual(len(results), 1)

    def test_map_type_returns_correct_category(self):
        self.assertEqual(self.provider._map_type(["restaurant", "food"]), "Gastronomía")
        self.assertEqual(self.provider._map_type(["park"]), "Parque")
        self.assertEqual(self.provider._map_type(["unknown_type"]), "Lugar")
