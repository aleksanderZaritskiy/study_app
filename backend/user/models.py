from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from study.constants import LENGTH_EMAIL, LENGTH_USERNAME


class CustomUserManager(UserManager):

    def create_user(self, email, password, username='', **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, username='', **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, username, **extra_fields)


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = models.CharField(
        help_text='Укажите ваш псевдоним',
        max_length=LENGTH_USERNAME,
        validators=(UnicodeUsernameValidator(),),
        error_messages={'max_length': "больше 100 символов"},
        blank=True,
        null=True,
    )

    email = models.EmailField(
        'Почта',
        help_text=('Укажите свою электронную почту'),
        max_length=LENGTH_EMAIL,
        error_messages={'max_length': "не валидный имейл больше 254 символов"},
        unique=True,
    )

    objects = CustomUserManager()
