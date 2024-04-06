from django.db import models
from django.contrib.auth import get_user_model

from .constants import LENGTH_NAME_OBJ
from .validators import (
    validate_name,
    validate_number,
    validate_date_time_start,
    validate_url,
)


User = get_user_model()


class Course(models.Model):
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
        validators=(validate_date_time_start,),
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
        verbose_name_plural = 'Courses'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'], name='unique_author_course'
            ),
            models.CheckConstraint(
                check=models.Q(min_group_people__lte=models.F('max_group_people')),
                name='Минимальное количество участников не должно быть больше максимального',
            ),
        ]

    def __str__(self):
        return self.name


class PassAccess(models.Model):
    """Модель связи студента и курса"""

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='pass_access'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='pass_access'
    )
    is_valid = models.BooleanField('Выдан/Отнят доступ к курсу', default=False)

    class Meta:
        verbose_name_plural = 'PassAccess'
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course',
            )
        ]

    def __str__(self):
        return f'{self.student.username}'


class Lesson(models.Model):
    """Модель урока"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lesson')
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
        validators=(validate_url,),
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )

    class Meta:
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f'Курс: {self.course}, Урок: {self.name}'


class Group(models.Model):
    """Модель группы"""

    student = models.ManyToManyField(
        User,
        through='GroupStudents',
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='group')
    name = models.CharField(
        'Название группы',
        help_text='Укажите название группы',
        max_length=LENGTH_NAME_OBJ,
        unique=True,
    )

    class Meta:
        verbose_name_plural = 'Groups'

    def __str__(self):
        return f'{self.name}'


class GroupStudentsManager(models.Manager):

    def create_group_student(self, group, student):
        GroupStudents.objects.create(group=group, student=student)

    def del_groups_related_course(self, course):
        GroupStudents.objects.filter(group__course=course).delete()


class GroupStudents(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = GroupStudentsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'group'],
                name='unique_student_group',
            )
        ]
