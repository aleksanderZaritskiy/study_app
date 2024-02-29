from django.db import models
from django.contrib.auth import get_user_model

from .constants import LENGTH_NAME_OBJ
from .validators import validate_name, validate_number

User = get_user_model()


class EducationCourse(models.Model):
    """Модель продукта"""

    author = models.ForeignKey(
        User,
        verbose_name='Автор курса',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Название',
        help_text='Укажите название курса',
        validators=(validate_name,),
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )
    date_time_start = models.DateTimeField(
        verbose_name='Дата начала',
    )
    cost = models.PositiveSmallIntegerField(
        'Стоимость курса',
        help_text='Укажите стоимость курса',
        validators=(validate_number,),
    )
    min_group_people = models.PositiveSmallIntegerField(
        'Минимальное количество человек в группе',
        help_text='Укажите минимальное число студентов для набора',
        validators=(validate_number,),
    )
    max_group_people = models.PositiveSmallIntegerField(
        'Максимальное количество человек в группе',
        help_text='Укажите минимальное число студентов для набора',
        validators=(validate_number,),
    )

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return self.name


class Pass(models.Model):
    """Модель связи студента и курса"""

    student = models.ForeignKey(User, on_delete=models.PROTECT, related_name='course')
    course = models.ForeignKey(
        EducationCourse, on_delete=models.CASCADE, related_name='student'
    )

    class Meta:
        verbose_name_plural = 'Pass'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course',
            )
        ]


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(
        EducationCourse, on_delete=models.CASCADE, related_name='lesson'
    )
    name = models.CharField(
        'Название урока',
        help_text='Укажите название урока',
        validators=(validate_name,),
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )
    link_to_video = models.URLField(
        'Cсылка на видео урок',
        help_text='Укажите ссылку на видео',
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )


class Group(models.Model):
    """Модель группы"""

    student = models.ManyToManyField(
        User,
        through='GroupStudents',
    )
    course = models.ForeignKey(
        EducationCourse, on_delete=models.CASCADE, related_name='group'
    )
    name = models.CharField(
        'Название группы',
        help_text='Укажите название группы',
        max_length=LENGTH_NAME_OBJ,
    )


class GroupStudents(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
