from datetime import datetime, timedelta

from rest_framework import serializers

from .models import ForecastOverride


class CurrentWeatherQuerySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)


class ForecastQuerySerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.CharField(required=True)

    def validate_date(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise serializers.ValidationError(
                "Invalid date format, expected dd.MM.yyyy"
            )
        today = datetime.now().date()
        if date < today:
            raise serializers.ValidationError("Date cannot be in the past")
        if date > today + timedelta(days=10):
            raise serializers.ValidationError(
                "Date cannot be more than 10 days in future"
            )
        return date


class ForecastOverrideSerializer(serializers.ModelSerializer):
    date = serializers.CharField()

    class Meta:
        model = ForecastOverride
        fields = "__all__"

    def validate(self, data):
        if data["min_temperature"] > data["max_temperature"]:
            raise serializers.ValidationError(
                "min_temperature cannot be greater than max_temperature"
            )
        return data

    def validate_date(self, value):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise serializers.ValidationError("Invalid date format")
        today = datetime.now().date()
        if date < today or date > today + timedelta(days=10):
            raise serializers.ValidationError("Invalid date range")
        return date
