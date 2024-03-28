from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from djoser import views

from .views import CourseViewSet


router = DefaultRouter()

router.register('users', views.UserViewSet)
router.register('course', CourseViewSet, basename='course')
# router.register('lesson', LessonViewSet)
# router.register('get_pass', PassVeiewSet)
# router.register('group', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
