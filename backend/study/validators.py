from django.core.validators import RegexValidator, MinValueValidator


validate_name = RegexValidator(
    r'^[A-Za-zА-Яа-я]+(\s[A-Za-zА-Яа-я]+)*$',
    ('Поле должно содержать только буквы кириллицы/латиницы'),
)

validate_number = MinValueValidator(
    limit_value=1,
    message='Укажите значение 1 и более',
)
