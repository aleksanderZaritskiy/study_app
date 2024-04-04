import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


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