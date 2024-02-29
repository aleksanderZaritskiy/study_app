from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.decorators import action

from study.models import EducationCourse, Pass, Lesson, Group, GroupStudents
from .permissions import IsCourseAuthorPermission, LessonPermission
from .serializers import (
    EducationCourseSerializer,
    LessonSerializer,
    PassSerializer,
    GroupSerializer,
)


class EducationCourseViewSet(viewsets.ModelViewSet):
    """EducationCourse view"""

    queryset = EducationCourse.objects.all()
    serializer_class = EducationCourseSerializer
    permission_classes = (IsCourseAuthorPermission,)

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
    )
    def lesson(self, request, pk):
        course = Pass.objects.filter(course_id=pk, student=request.user).first()
        if course:
            lessons = Lesson.objects.filter(course_id=course.course_id)
            return Response(
                LessonSerializer(lessons, context={'request': request}, many=True).data,
                status=status.HTTP_200_OK,
            )
        return Response({'response': 'Не найдено'}, status=status.HTTP_404_NOT_FOUND)


class LessonViewSet(viewsets.ModelViewSet):
    """Lesson view"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (LessonPermission,)


class PassVeiewSet(CreateModelMixin, viewsets.GenericViewSet):
    """Pass view. Определяет доступ студентов к курсам"""

    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def _formatted_group(self, request):
        course_id = request.data['course']
        course = EducationCourse.objects.filter(id=course_id).first()
        if (
            course.date_time_start <= timezone.now()
            or Pass.objects.filter(
                course_id=course_id, student_id=request.user.id
            ).exists()
        ):
            return
        students = [{'student': request.user.id}]
        groups = Group.objects.filter(course_id=course_id)
        # В случае, когда на курс ещё не было ни одной записи
        # создаём запись в таблице
        if not groups:
            new_group = Group(course_id=course_id, name=f"Kogorta {course} 1")
            new_group.save()
            GroupStudents(group_id=new_group.id, student_id=request.user.id).save()
            return True
        students.extend(list(groups.values('student')))
        # Очищаем записи в побочной модели MtM
        for group in groups:
            group.student.clear()
        # Добираем новую группу, если количество студентов
        # превышает limit * group_count
        print(len(students), groups.count(), course.max_group_people)
        if len(students) / (groups.count() * course.max_group_people) > 1:
            number_last_group = groups.last().name.split()[-1]
            new_group = Group(
                course_id=course_id, name=f"Kogorta {course} {int(number_last_group) + 1}"
            )
            new_group.save()
        # Наполняем группы сбалансированно
        while students:
            for group in Group.objects.filter(course_id=course_id):
                if not students:
                    break
                tmp_student = students.pop()['student']
                GroupStudents(group_id=group.id, student_id=tmp_student).save()
        return True

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ans = self._formatted_group(request)
        if not ans:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GroupViewSet(ListModelMixin, RetrieveModelMixin, viewsets.GenericViewSet):
    """Group view"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
