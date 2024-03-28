from django.contrib import admin

from study.models import Course, PassAccess, Lesson, Group, GroupStudents, User


class AdminCourse(admin.ModelAdmin):
    pass


class AdminPassAccess(admin.ModelAdmin):
    pass


class AdminLesson(admin.ModelAdmin):
    pass


class AdminGroup(admin.ModelAdmin):
    pass


admin.site.register(Course, AdminCourse)
admin.site.register(PassAccess, AdminPassAccess)
admin.site.register(Lesson, AdminLesson)
admin.site.register(Group, AdminGroup)