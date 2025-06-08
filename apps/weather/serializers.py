from rest_framework import serializers

from .models import ForecastOverride
from .utils import Validator


class CurrentWeatherQuerySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)

    def validate_city(self, city):
        return Validator.validate_city(city)


class ForecastQuerySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.CharField(required=True)

    def validate_city(self, city):
        return Validator.validate_city(city)

    def validate_date(self, date):
        return Validator.validate_forecast_date(date)


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.CharField()

    class Meta:
        model = ForecastOverride
        fields = "__all__"

    def validate_date(self, date):
        return Validator.validate_forecast_date(date)

    def validate_city(self, city):
        return Validator.validate_city(city)

    def validate(self, data: dict) -> dict:
        Validator.validate_date_range(data["date"])
        Validator.validate_temperature_range(data)
        return data
