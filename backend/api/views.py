from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Prefetch, Exists, OuterRef, Subquery, Q, Avg
from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action

from study.models import Course, PassAccess, Lesson, Group, GroupStudents, User
#from .permissions import IsCourseAuthorPermission, LessonPermission
from .serializers import (
    CourseSerializer,
    LessonSerializer,
)


class CourseViewSet(ListModelMixin, viewsets.GenericViewSet):
    
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        author_prefetch = Prefetch('author', queryset=User.objects.only('username'))
        queryset = Course.objects.filter(
            ~Exists(
                PassAccess.objects.filter(course=OuterRef('pk'), student=user, is_valid=True)
            )
        ).prefetch_related(author_prefetch)
        queryset = queryset.annotate(
            lessons_count=Count('lesson', distinct=True),
            students_count=Count('pass_access', filter=Q(pass_access__is_valid=True)),

        )
        return queryset

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,),
    )
    def lessons(self, request, pk):
        pa = PassAccess.objects.filter(student=request.user, course=pk, is_valid=True)
        if pa.exists():
            lessons = Lesson.objects.filter(course=pk)
            return Response(
                LessonSerializer(lessons, context={'request': request}, many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response({'response': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)


