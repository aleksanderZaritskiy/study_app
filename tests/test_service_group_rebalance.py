from collections import defaultdict

import pytest

from .utils import create_pa, create_users_data
from study.models import Group, GroupStudents


@pytest.mark.django_db(transaction=True)
class TestPassAccessSignalAPI:

    NEED_STUDENTS = 5

    def test_created_group_and_through(self, user_with_pa, user, create_course):

        group = Group.objects.filter(student=user, course=create_course).first()
        through_model = GroupStudents.objects.filter(group=group, student=user)
        assert (
            group
        ), 'Убедитесь, что при необходимости после получения пользователем pa создается объект группы'
        assert (
            through_model.exists()
        ), 'Убедитесь, что при получении пользователем pa создается запись mtm в модели GroupStudents'

    def test_groups_rebalance(self, create_course, django_user_model, user_with_pa):

        create_pa(
            create_users_data(need_users=self.NEED_STUDENTS),
            django_user_model,
            create_course,
        )
        group = Group.objects.filter(course=create_course)
        groups_count = group.count()
        groups_students = GroupStudents.objects.filter(
            group__course=create_course
        ).values('student', 'group')
        students_count = len(groups_students)
        div = (
            students_count % create_course.max_group_people
            if students_count > create_course.max_group_people
            else 0
        )
        need_group = students_count // create_course.max_group_people + (
            True if div else div
        )
        assert (
            groups_count == need_group
        ), f'Колличество групп не соответствуют колличеству студентов {groups_count} != {need_group}'

        students_in_group = defaultdict(int)

        for group_student in groups_students:
            group_id = group_student['group']
            students_in_group[group_id] += 1

        cur, prev = 1, 0
        students = list(students_in_group.values())
        while cur < len(students):

            assert (
                abs(students[cur] - students[prev]) <= 1
            ), f'Нарушен принцип ребалансировки n+-1, {students_in_group[i]} и {students_in_group[i-1]} > 1'
            cur += 1
            prev += 1

        user_with_pa.is_valid = False
        user_with_pa.save()
        groups_count_after_pick_pa = group.count()

        assert (
            groups_count - groups_count_after_pick_pa == 1
        ), f'Группа должна быть удалена, если она не требуется. {groups_count}, {groups_count_after_pick_pa}'
