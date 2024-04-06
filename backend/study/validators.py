from django.utils import timezone


from django.core.validators import RegexValidator, MinValueValidator, URLValidator
from django.core.exceptions import ValidationError


validate_name = RegexValidator(
    r'^[A-Za-zА-Яа-я]+(\s[A-Za-zА-Яа-я]+)*$',
    ('Поле должно содержать только буквы кириллицы/латиницы'),
)

validate_number = MinValueValidator(
    limit_value=1,
    message='Укажите значение 1 и более',
)

validate_url = URLValidator(
    message='Некорректная ссылка',
)


def validate_date_time_start(value):
    if value <= timezone.now():
        raise ValidationError(f'{value} должно быть позже текущего времени.')
