import re
from datetime import datetime, timedelta

from rest_framework.exceptions import ValidationError


class Validator:
    @staticmethod
    def validate_city(city: str) -> str:
        if not re.fullmatch(r"[A-Za-z\s\-]+", city):
            raise ValidationError(
                "Название города должно содержать только английские буквы, пробелы и дефисы."
            )
        return city

    @staticmethod
    def validate_forecast_date(date_str: str) -> datetime.date:
        try:
            date: datetime.date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            raise ValidationError(
                "Неверный формат даты, ожидается дд.мм.гггг"
            )
        return date

    @staticmethod
    def validate_temperature_range(data: dict) -> dict[str, int | float]:
        min_temp: str = data.get("min_temperature")
        max_temp: str = data.get("max_temperature")

        if min_temp is None or max_temp is None:
            raise ValidationError("Поля min_temperature и max_temperature обязательны.")

        if min_temp > max_temp:
            raise ValidationError(
                "Значение min_temperature не может быть больше значения max_temperature"
            )
        return data

    @staticmethod
    def validate_date_range(date: datetime.date) -> None:
        today: datetime.date = datetime.now().date()

        if date < today:
            raise ValidationError(
                "Дата не может быть в прошлом"
            )
        if date > today + timedelta(days=10):
            raise ValidationError(
                "Дата не может быть позже чем через 10 дней"
            )
