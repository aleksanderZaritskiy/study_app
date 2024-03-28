import datetime as dt

from rest_framework import serializers
from djoser.serializers import UserSerializer

from study.models import Course, PassAccess, Lesson, Group, User


class CourseSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    # avg_puck_groups = serializers.SerializerMethodField()
    # course_purchase = serializers.SerializerMethodField()

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
            #'avg_puck_groups',
            #'course_purchase',
        )

    def get_author_name(self, obj):
        return obj.author.username
    
    def get_lessons_count(self, obj):
        return obj.lessons_count

    def get_students_count(self, obj):
        return obj.students_count

class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'name',
            'link_to_video',
        )



class PassSerializer(serializers.ModelSerializer):
    pass
    # course = serializers.PrimaryKeyRelatedField(queryset=EducationCourse.objects.all())
    # student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    # class Meta:
    #     model = Pass
    #     fields = (
    #         'course',
    #         'student',
    #     )


class GetStudentSerializer(serializers.ModelSerializer):
    pass
    # username = serializers.PrimaryKeyRelatedField(
    #     source='student.username', queryset=User.objects.all()
    # )

    # class Meta:
    #     model = User
    #     fields = ('username',)


class GroupSerializer(serializers.ModelSerializer):
    pass
    # course = serializers.PrimaryKeyRelatedField(queryset=EducationCourse.objects.all())
    # student = serializers.SerializerMethodField()

    # class Meta:
    #     model = Group
    #     fields = (
    #         'id',
    #         'name',
    #         'course',
    #         'student',
    #     )

    # def get_student(self, obj):
    #     students = obj.groupstudents_set.all()
    #     return GetStudentSerializer(students, many=True).data
