from datetime import timedelta

import pytest
from django.test import Client
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse

from study.models import Course, PassAccess

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

# @pytest.fixture
# def user_admin(django_user_model):
#     return django_user_model.objects.create_superuser(
#         username='test_admin',
#         password='test_password22',
#     )

# @pytest.fixture
# def admin_client(user_admin):
#     client = Client()
#     client.login(username=user_admin.username, password=user_admin.password)
#     return client

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
    #return Course.objects.get(name=course_data['name'])

@pytest.fixture
def user_with_pa(user, create_course):
    return PassAccess.objects.create(student=user, course=create_course, is_valid=True)
