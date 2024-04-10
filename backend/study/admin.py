from django.contrib import admin
from constance.admin import ConstanceAdmin, Config

from study.models import Course, PassAccess, Lesson, Group, GroupStudents, User


class AdminCourse(admin.ModelAdmin):
    pass


class AdminPassAccess(admin.ModelAdmin):
    pass


class AdminLesson(admin.ModelAdmin):
    pass


class AdminGroup(admin.ModelAdmin):
    pass


class GroupStudentsAdmin(admin.ModelAdmin):
    pass


class ConfigAdmin(ConstanceAdmin):
    pass


admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
admin.site.register(GroupStudents, GroupStudentsAdmin)
admin.site.register(Course, AdminCourse)
admin.site.register(PassAccess, AdminPassAccess)
admin.site.register(Lesson, AdminLesson)
admin.site.register(Group, AdminGroup)
