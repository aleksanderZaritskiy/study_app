from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser import views

from .views import CourseViewSet, CreateUserViewSet, LogoutView

router = DefaultRouter()

router.register('course', CourseViewSet, basename='course')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', CreateUserViewSet.as_view({'post': 'create'}), name='user-create'),
    path('me/', views.UserViewSet.as_view({'get': 'me', 'patch': 'me'}), name='user-me'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
]
