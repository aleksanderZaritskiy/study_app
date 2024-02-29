from rest_framework import permissions

from study.models import Pass, EducationCourse


class IsCourseAuthorPermission(permissions.BasePermission):
    """
    Права для управление объектами модели EducationCourse
    Редактировать и удалять может только автор курса
    """

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST'
            and request.user.is_authenticated
            or request.method in ('PATCH', 'DELETE', 'PUT')
            and request.user == obj.author
        )


class LessonPermission(permissions.BasePermission):
    """
    Права для управление объектами модели Lesson
    Редактировать и удалять может только автор курса.
    Чтение доступно только пользователям с подпиской.
    """

    def has_permission(self, request, view):
        if not request.user.id:
            return False
        get_pass = Pass.objects.filter(student=request.user).first()
        get_author = EducationCourse.objects.filter(author=request.user).first()
        return request.method in permissions.SAFE_METHODS and get_pass or get_author

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method in ('PATCH', 'DELETE', 'PUT')
            and obj.course.author == request.user
        )
