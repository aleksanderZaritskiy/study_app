# Generated by Django 4.2.10 on 2024-02-28 17:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EducationCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название курса",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[а-яА-ЯёЁa-zA-Z]*$",
                                "Поле должно содержать только буквы кириллицы/латиницы",
                            )
                        ],
                        verbose_name="Название",
                    ),
                ),
                ("date_time_start", models.DateTimeField(verbose_name="Дата начала")),
                (
                    "cost",
                    models.PositiveSmallIntegerField(
                        help_text="Укажите стоимость курса",
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1, message="Укажите значение 1 и более"
                            )
                        ],
                        verbose_name="Стоимость курса",
                    ),
                ),
                (
                    "min_group_people",
                    models.PositiveSmallIntegerField(
                        help_text="Укажите минимальное число студентов для набора",
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1, message="Укажите значение 1 и более"
                            )
                        ],
                        verbose_name="Минимальное количество человек в группе",
                    ),
                ),
                (
                    "max_group_people",
                    models.PositiveSmallIntegerField(
                        help_text="Укажите минимальное число студентов для набора",
                        validators=[
                            django.core.validators.MinValueValidator(
                                limit_value=1, message="Укажите значение 1 и более"
                            )
                        ],
                        verbose_name="Максимальное количество человек в группе",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор курса",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Product",
            },
        ),
        migrations.CreateModel(
            name="Pass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="student",
                        to="study.educationcourse",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="course",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название урока",
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[а-яА-ЯёЁa-zA-Z]*$",
                                "Поле должно содержать только буквы кириллицы/латиницы",
                            )
                        ],
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "link_to_video",
                    models.SlugField(
                        help_text="Укажите ссылку на видео",
                        max_length=150,
                        unique=True,
                        verbose_name="Cсылка на видео урок",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lesson",
                        to="study.educationcourse",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Укажите название группы",
                        max_length=150,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^[а-яА-ЯёЁa-zA-Z]*$",
                                "Поле должно содержать только буквы кириллицы/латиницы",
                            )
                        ],
                        verbose_name="Название группы",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="group",
                        to="study.educationcourse",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="group",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]