from datetime import timedelta

from django.utils import timezone


LENGTH_NAME_OBJ = 150
LENGTH_EMAIL = 254
LENGTH_USERNAME = 100
TTL_CACHE_PA = 86_400
TTL_CACHE_LESSONS = 86_400
TTL_ACCESS_TOKEN = 30
TTL_REFRESH_TOKEN = 30
TTL_CONSTANCE = 60
DATETIME_COURSE_START = timezone.now() + timedelta(days=100)
