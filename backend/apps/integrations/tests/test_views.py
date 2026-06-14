from unittest.mock import patch
import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def auth_client(user_factory):
    user = user_factory(email="weather_test@example.com")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
class TestWeatherCurrentView:
    url = "/api/v1/weather/current/"

    def test_requires_authentication(self, api_client):
        resp = api_client.get(self.url, {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_400_when_missing_params(self, auth_client):
        resp = auth_client.get(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_invalid_lat(self, auth_client):
        resp = auth_client.get(self.url, {"lat": "notanumber", "lon": -58.4})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_out_of_range_lat(self, auth_client):
        resp = auth_client.get(self.url, {"lat": 200, "lon": -58.4})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @patch("apps.integrations.providers.openweather.OpenWeatherProvider.get_current_weather")
    def test_returns_weather_data(self, mock_weather, auth_client):
        mock_weather.return_value = {
            "temperature": 18.0,
            "feels_like": 16.0,
            "condition": "Clear",
            "humidity": 50,
            "wind_speed": 3.0,
            "clouds": 10,
            "is_outdoor_friendly": True,
        }
        resp = auth_client.get(self.url, {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["success"] is True
        assert resp.data["data"]["temperature"] == 18.0

    @patch("apps.integrations.providers.openweather.OpenWeatherProvider.get_current_weather")
    def test_returns_null_data_on_fallback(self, mock_weather, auth_client):
        mock_weather.return_value = None
        resp = auth_client.get(self.url, {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["data"] is None


@pytest.mark.django_db
class TestExternalPlacesView:
    url = "/api/v1/external/places/"

    def test_requires_authentication(self, api_client):
        resp = api_client.get(self.url, {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_400_when_missing_params(self, auth_client):
        resp = auth_client.get(self.url)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST

    @patch("apps.integrations.views.get_external_places")
    def test_returns_empty_list_when_no_results(self, mock_places, auth_client):
        mock_places.return_value = []
        resp = auth_client.get(self.url, {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["data"] == []

    def test_search_requires_query(self, auth_client):
        resp = auth_client.get("/api/v1/external/places/search/", {"lat": -34.6, "lon": -58.4})
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
