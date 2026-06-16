from django.urls import path
from .views import (
    WeatherCurrentView,
    ExternalPlacesView,
    ExternalPlacesSearchView,
    GeocodingView,
    ReverseGeocodingView,
)

weather_urlpatterns = [
    path("current/", WeatherCurrentView.as_view(), name="weather-current"),
]

external_places_urlpatterns = [
    path("", ExternalPlacesView.as_view(), name="external-places"),
    path("search/", ExternalPlacesSearchView.as_view(), name="external-places-search"),
]

geocoding_urlpatterns = [
    path("", GeocodingView.as_view(), name="geocoding"),
    path("reverse/", ReverseGeocodingView.as_view(), name="reverse-geocoding"),
]
