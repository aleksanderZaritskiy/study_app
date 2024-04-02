import logging
from collections import deque
from typing import Optional

from django.utils import timezone
from django.db import transaction

from study.models import Group, User, Course, GroupStudents


logger = logging.getLogger(__name__)


class GroupRebalance:

    def __init__(self, student: User, course: Course, groups: list[Group]) -> None:
        self.student = student
        self.course = course
        self.groups = groups
        self.__need_to_rebalance = True
        self.min_group_size = self.course.min_group_people
        self.max_group_size = self.course.max_group_people

    def add(self) -> None:
        group = self._get_available_group()
        if not group:
            group = self._create_group()
        GroupStudents.objects.create_group_student(group=group, student=self.student)

        self.rebalance()

    def rebalance(self) -> None:

        if self._is_course_started():
            logger.info('Ребалансировка невыполнена. Курс уже начался')
            return
        
        if self.__need_to_rebalance:
            logger.info('Запуск ребалансировки')
            all_students = [student for group in self.groups for student in group.student.all()]
            GroupStudents.objects.del_groups_related_course(self.course)

            if len(self.groups) * self.max_group_size - len(all_students) >= self.max_group_size:
                self._remove_group()
                
            queue_groups = deque(self.groups)

            with transaction.atomic():
                for student in all_students:
                    group = queue_groups.popleft()
                    group.student.add(student)
                    queue_groups.append(group)
                    logger.info(f'Студен {student} добавлен в {group}')

    def _create_group(self) -> Group:
        new_group = Group.objects.create(course=self.course, name=f"{self.course.name}, group #{len(self.groups) + 1}")
        self.groups.append(new_group)
        logger.info(f'Создание новой группы {new_group}')
        return new_group
    
    def _remove_group(self) -> None:
        logger.info('Удаляем группу')
        removed_group = self.groups.pop()
        removed_group.delete()
    
    def _get_available_group(self) -> Optional[Group]:
        logger.info('Поиск доступных групп')
        group = min(
            filter(lambda group: group.students_count < self.max_group_size, self.groups), 
            key=lambda group: group.students_count, 
            default=None,
        )
        if group:
            self.__need_to_rebalance = False
        return group
    
    def _is_course_started(self) -> bool:
        return self.course.date_time_start <= timezone.now()