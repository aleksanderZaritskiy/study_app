import datetime as dt

from rest_framework import serializers
from django.db.models import Avg, F, Q
from djoser.serializers import UserSerializer

from study.models import Course, PassAccess, Lesson, Group, User


class CourseSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    avg_groups = serializers.SerializerMethodField()
    course_purchase = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'name',
            'author_name',
            'date_time_start',
            'cost',
            'min_group_people',
            'max_group_people',
            'lessons_count',
            'students_count',
            'avg_groups',
            'course_purchase',
        )

    def get_author_name(self, obj):
        return obj.author.username
    
    def get_lessons_count(self, obj):
        return obj.lessons_count

    def get_students_count(self, obj):
        return obj.students_count
    
    def get_avg_groups(self, obj):
        all_groups = Group.objects.filter(course=obj).count()
        if all_groups and obj.students_count:
            return round(
                (all_groups * obj.students_count / all_groups) / obj.max_group_people * 100, 2
            )
        return 0
    
    def get_course_purchase(self, obj):
        all_user = User.objects.all().count()
        if obj.students_count:
            return round(obj.students_count / all_user * 100, 2)
        return 0


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'name',
            'link_to_video',
        )

