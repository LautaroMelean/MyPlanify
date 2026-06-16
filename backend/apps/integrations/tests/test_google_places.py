from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.cache import cache

from apps.integrations.providers.overpass import OverpassProvider


OSM_ELEMENT = {
    "type": "node",
    "id": 12345,
    "lat": -34.606,
    "lon": -58.435,
    "tags": {
        "name": "Parque Centenario",
        "amenity": "park",
        "addr:city": "Buenos Aires",
    },
}

OSM_WAY_ELEMENT = {
    "type": "way",
    "id": 99999,
    "center": {"lat": -34.61, "lon": -58.44},
    "tags": {
        "name": "Bar San Telmo",
        "amenity": "bar",
        "addr:street": "Defensa",
        "addr:housenumber": "123",
        "addr:city": "Buenos Aires",
        "phone": "+54 11 1234-5678",
        "website": "https://example.com",
    },
}


def _mock_response(elements=None):
    mock = MagicMock()
    mock.raise_for_status = MagicMock()
    mock.json.return_value = {"elements": elements if elements is not None else [OSM_ELEMENT]}
    return mock


class OverpassProviderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.provider = OverpassProvider()

    def tearDown(self):
        cache.clear()

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_search_nearby_returns_results(self, mock_post):
        mock_post.return_value = _mock_response()
        results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Parque Centenario")
        self.assertEqual(results[0]["source"], "osm")
        self.assertIn("osm:node:12345", results[0]["external_id"])

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_caches_results(self, mock_post):
        mock_post.return_value = _mock_response()
        self.provider.search_nearby(-34.60, -58.40)
        self.provider.search_nearby(-34.60, -58.40)
        self.assertEqual(mock_post.call_count, 1)

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_fallback_on_api_error(self, mock_post):
        mock_post.side_effect = Exception("timeout")
        results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(results, [])

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_skips_elements_without_name(self, mock_post):
        mock_post.return_value = _mock_response([
            {"type": "node", "id": 1, "lat": -34.6, "lon": -58.4, "tags": {}},
        ])
        results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(results, [])

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_parses_way_element_with_center(self, mock_post):
        mock_post.return_value = _mock_response([OSM_WAY_ELEMENT])
        results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Bar San Telmo")
        self.assertEqual(results[0]["phone"], "+54 11 1234-5678")
        self.assertEqual(results[0]["website"], "https://example.com")
        self.assertAlmostEqual(results[0]["latitude"], -34.61)

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_deduplicates_elements(self, mock_post):
        mock_post.return_value = _mock_response([OSM_ELEMENT, OSM_ELEMENT])
        results = self.provider.search_nearby(-34.6, -58.4)
        self.assertEqual(len(results), 1)

    def test_resolve_category_amenity(self):
        self.assertEqual(self.provider._resolve_category({"amenity": "restaurant"}), "Gastronomía")
        self.assertEqual(self.provider._resolve_category({"amenity": "bar"}), "Bar")
        self.assertEqual(self.provider._resolve_category({"amenity": "museum"}), "Museo")

    def test_resolve_category_leisure(self):
        self.assertEqual(self.provider._resolve_category({"leisure": "park"}), "Parque")
        self.assertEqual(self.provider._resolve_category({"leisure": "fitness_centre"}), "Deporte")

    def test_resolve_category_unknown(self):
        self.assertEqual(self.provider._resolve_category({"amenity": "unknown_xyz"}), "Lugar")

    def test_build_address_with_street_and_number(self):
        tags = {"addr:street": "Corrientes", "addr:housenumber": "1234", "addr:city": "Buenos Aires"}
        address = self.provider._build_address(tags)
        self.assertIn("Corrientes 1234", address)
        self.assertIn("Buenos Aires", address)

    def test_build_address_empty_when_no_data(self):
        self.assertEqual(self.provider._build_address({}), "")

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_search_by_query_falls_back_to_nearby(self, mock_post):
        mock_post.return_value = _mock_response()
        results = self.provider.search_by_query("bar", -34.6, -58.4)
        self.assertTrue(mock_post.called)
        self.assertEqual(len(results), 1)

    @patch("apps.integrations.providers.overpass.requests.post")
    def test_type_filter_uses_specific_tag(self, mock_post):
        mock_post.return_value = _mock_response([])
        self.provider.search_nearby(-34.6, -58.4, place_type="restaurant")
        # call_args is (args, kwargs); data= is passed as kwarg
        call_kwargs = mock_post.call_args[1]
        query_sent = call_kwargs.get("data", {}).get("data", "")
        self.assertIn("restaurant", query_sent)
