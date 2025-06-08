from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import ForecastOverride
from .serializers import (
    CurrentWeatherQuerySerializer,
    ForecastOverrideSerializer,
    ForecastQuerySerializer
)
from .services import get_current_weather, get_forecast_weather


class CurrentWeatherView(APIView):
    """
    Получить список
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Название города для получения текущей погоды",
            )
        ],
        responses={200: openapi.Response(description="Успешный ответ с погодой")},
    )
    def get(self, request: Request) -> Response:
        serializer = CurrentWeatherQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data["city"]
        data = get_current_weather(city)
        return Response(data)


class ForecastWeatherView(APIView):
    """
    Получить список
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="city",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Город",
            ),
            openapi.Parameter(
                name="date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="Дата в формате dd.MM.yyyy",
            ),
        ]
    )
    def get(self, request: Request) -> Response:
        serializer = ForecastQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        city = serializer.validated_data["city"]
        date = serializer.validated_data["date"]

        override = ForecastOverride.objects.filter(city=city, date=date).first()
        if override:
            return Response(
                {
                    "min_temperature": override.min_temperature,
                    "max_temperature": override.max_temperature,
                }
            )

        data = get_forecast_weather(city, request.query_params["date"])
        return Response(data)

    @swagger_auto_schema(
        request_body=ForecastOverrideSerializer,
        responses={201: ForecastOverrideSerializer},
    )
    def post(self, request: Request) -> Response:
        serializer = ForecastOverrideSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        override, _ = ForecastOverride.objects.update_or_create(
            city=validated["city"],
            date=validated["date"],
            defaults={
                "min_temperature": validated["min_temperature"],
                "max_temperature": validated["max_temperature"],
            },
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
