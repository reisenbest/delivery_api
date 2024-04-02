import re
from django.core.exceptions import ValidationError


def validate_car_number(car_number):
    """
     валидатор для проверки валидности номера (4 цифры + буква заглавнаяиз латиницы)
    """
    if not re.match(r'^[1-9]\d{3}[A-Z]$', car_number):
        raise ValidationError('Номер машины должен быть цифрой от 1000 до 9999 + случайная заглавная буква английского алфавита в конце')


def validate_postcode(postcode):
    if not re.match(r'^\d{5}$', postcode):
        raise ValidationError('Почтовый индекс должен состоять из 5 цифр')