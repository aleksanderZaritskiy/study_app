import logging
from datetime import timedelta

import pytest
from django.utils import timezone
from django.core.cache import cache
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

from study.models import Course, PassAccess, Lesson


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='test_user',
        password='test_password22',
    )


@pytest.fixture
def token_user(user):
    token, created = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Token {token_user}',
    )
    return client


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(
        username='test_author',
        password='test_password22',
    )


@pytest.fixture
def create_course(author):
    course_data = {
        'author': author,
        'name': 'TestCourse',
        'date_time_start': timezone.now() + timedelta(days=30),
        'cost': 10000,
        'min_group_people': 2,
        'max_group_people': 5,
    }
    return Course.objects.create(**course_data)


@pytest.fixture
def user_with_pa(user, create_course):
    return PassAccess.objects.create(student=user, course=create_course, is_valid=True)


@pytest.fixture
def create_lessons(create_course):

    lesson_data = {
        'course': create_course,
        'name': 'TestCourse',
        'link_to_video': 'https://www.youtube.com/watch?v=9WPnnn1m4SM',
    }
    return Lesson.objects.create(**lesson_data)


@pytest.fixture(autouse=True)
def clear_cache():
    yield
    cache.clear()


@pytest.fixture(autouse=True)
def no_logging():
    """Отключает логирование для тестов."""
    original_level = logging.getLogger().level
    logging.getLogger().setLevel(logging.CRITICAL)
    yield
    logging.getLogger().setLevel(original_level)
