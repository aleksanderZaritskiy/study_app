from datetime import timedelta

from django.utils import timezone


LENGTH_NAME_OBJ = 150
TTL_CACHE_PA = 86_400
TTL_CACHE_LESSONS = 86_400
DATETIME_COURSE_START = timezone.now() + timedelta(days=100)
