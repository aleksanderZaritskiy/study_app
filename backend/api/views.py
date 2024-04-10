import logging

from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, status, views
from django.core.cache import cache
from django.db.models import Count, Prefetch, Exists, OuterRef, Q
from rest_framework import viewsets, permissions, status, views
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from constance import config

from study.models import Course, PassAccess, Lesson, User

from .serializers import (
    CourseSerializer,
    LessonSerializer,
)


logger = logging.getLogger(__name__)


class CourseViewSet(ListModelMixin, viewsets.GenericViewSet):

    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):

        user = self.request.user
        author_prefetch = Prefetch('author', queryset=User.objects.only('username'))
        queryset = Course.objects.filter(
            ~Exists(
                PassAccess.objects.filter(
                    course=OuterRef('pk'), student=user, is_valid=True
                )
            )
        ).prefetch_related(author_prefetch)
        queryset = queryset.annotate(
            lessons_count=Count('lesson', distinct=True),
            students_count=Count(
                'pass_access', filter=Q(pass_access__is_valid=True), distinct=True
            ),
        )

        return queryset

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def lessons(self, request, pk):
        cache_pa_key = f'{request.user}_lessons_course_{pk}'
        cache_lesson_key = f'lessons_course_{pk}'
        pa = cache.get(cache_pa_key)
        if not pa:
            pa = PassAccess.objects.filter(
                student=request.user, course=pk, is_valid=True
            ).exists()
            cache.set(cache_pa_key, pa, config.TTL_CACHE_PA)
            logger.info(f'PA студента {request.user} закеширован')

        if pa:

            lessons_data = cache.get(cache_lesson_key)

            if not lessons_data:
                lessons_from_db = Lesson.objects.filter(course=pk)
                lessons_data = LessonSerializer(
                    lessons_from_db, context={'request': request}, many=True
                ).data
                cache.set(cache_lesson_key, lessons_data, config.TTL_CACHE_LESSONS)
                logger.info(f'Данные уроков закешированы {lessons_data}')

            return Response(
                lessons_data,
                status=status.HTTP_200_OK,
            )
        return Response({'response': 'Не найдено'}, status=status.HTTP_403_FORBIDDEN)


class CreateUserViewSet(UserViewSet):

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LogoutView(views.APIView):

    def post(self, request):

        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=400)

        try:
            decode_token = RefreshToken(refresh_token)
            decode_token.blacklist()
            return Response({'success': "User logged out."}, status=200)
        except (TokenError, InvalidToken) as error:
            return ResourceWarning({'error': error.default_detail}, status=400)
