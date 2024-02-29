import datetime as dt

from rest_framework import serializers
from djoser.serializers import UserSerializer

from study.models import EducationCourse, Pass, Lesson, Group, User


class EducationCourseSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    lesson_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    avg_puck_groups = serializers.SerializerMethodField()
    course_purchase = serializers.SerializerMethodField()

    class Meta:
        model = EducationCourse
        fields = (
            'id',
            'author',
            'name',
            'date_time_start',
            'cost',
            'min_group_people',
            'max_group_people',
            'lesson_count',
            'students_count',
            'avg_puck_groups',
            'course_purchase',
        )
        read_only_fields = (
            'lesson_count',
            'students_count',
            'avg_puck_groups',
            'course_purchase',
        )

    def get_lesson_count(self, obj):
        return obj.lesson.count()

    def get_students_count(self, obj):
        return obj.student.count()

    def get_avg_puck_groups(self, obj):
        all_groups = Group.objects.filter(course_id=obj.id)
        students_in_groups = all_groups.values('student').count()
        groups_count = all_groups.count()
        if not students_in_groups or not groups_count:
            return 0
        return round(students_in_groups / groups_count / obj.max_group_people * 100, 2)

    def get_course_purchase(self, obj):
        return round(
            Pass.objects.filter(course_id=obj.id).count()
            / User.objects.all().count() * 100, 2
        )

    def validate(self, data):
        if any(
            [
                'name' not in self.initial_data,
                'date_time_start' not in self.initial_data,
                'cost' not in self.initial_data,
                'min_group_people' not in self.initial_data,
                'max_group_people' not in self.initial_data,
            ]
        ):
            raise serializers.ValidationError({'detail': 'Заполните все поля'})
        input_time = self.initial_data.get('date_time_start')
        if dt.datetime.now() >= dt.datetime.strptime(input_time, '%Y-%m-%d %H:%M'):
            raise serializers.ValidationError(
                {'detail': 'Слишком ранняя дата начала курса'}
            )
        return data

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        course_obj = EducationCourse.objects.create(**validated_data)
        return course_obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date_time_start = validated_data.get('date_time_start', instance.name)
        instance.cost = validated_data.get('cost', instance.name)
        instance.min_group_people = validated_data.get('min_group_people', instance.name)
        instance.max_group_people = validated_data.get('max_group_people', instance.name)
        instance.save()
        return instance


class LessonSerializer(serializers.ModelSerializer):

    course = serializers.PrimaryKeyRelatedField(queryset=EducationCourse.objects.all())

    class Meta:
        model = Lesson
        fields = (
            'course',
            'name',
            'link_to_video',
        )

    def create(self, validated_data):
        lesson_obj = Lesson.objects.create(**validated_data)
        return lesson_obj


class PassSerializer(serializers.ModelSerializer):

    course = serializers.PrimaryKeyRelatedField(queryset=EducationCourse.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Pass
        fields = (
            'course',
            'student',
        )


class GetStudentSerializer(serializers.ModelSerializer):

    username = serializers.PrimaryKeyRelatedField(
        source='student.username', queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ('username',)


class GroupSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=EducationCourse.objects.all())
    student = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'course',
            'student',
        )

    def get_student(self, obj):
        students = obj.groupstudents_set.all()
        return GetStudentSerializer(students, many=True).data
