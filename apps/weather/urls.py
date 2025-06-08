from typing import List

from django.urls import path

from weather_project import SuffixRouter

from . import views

urlpatterns: List[path] = [
    path(SuffixRouter.CURRENT, views.CurrentWeatherView.as_view()),
    path(SuffixRouter.FORCAST, views.ForecastWeatherView.as_view()),
]
