import logging
from collections import deque
from typing import Optional, Union

from django.utils import timezone
from django.db import transaction

from study.models import PassAccess, Group, User, Course, GroupStudents


logger = logging.getLogger(__name__)


class GroupRebalance:

    def __init__(self, student: User, course: Course, groups: list[Group]) -> None:
        self.student = student
        self.course = course
        self.groups = groups
        self.__need_to_rebalance = True
        self.min_group_size = self.course.min_group_people
        self.max_group_size = self.course.max_group_people

    def add_to_group(self) -> None:
        group = self._get_available_group()
        if not group:
            group = self._create_group()
        group.create_groups_student_through(self.student)

        self.rebalance()

    def rebalance(self):

        if self._is_course_started():
            logger.info('Ребалансировка невыполнена. Курс уже начался')
            return
        
        if self.__need_to_rebalance:
            logger.info('Запуск ребалансировки')
            self._delete_group_student_through()
            all_students = [student for group in self.groups for student in group.student.all()]

            if self.max_group_size * len(self.groups) > len(all_students):
                self._remove_group()
                
            queue_groups = deque(self.groups)
            
            with transaction.atomic():
                for student in all_students:
                    group = queue_groups.pop()
                    # пишут что при использовании .add в побочке автоматом создается запись.
                    group.student.add(student)
                    queue_groups.append(group)
                    logger.info(f'Студен {student} добавлен в {group}')
            return 
        return 


    def _create_group(self) -> Group:
        logger.info('Создание новой группы')
        new_group = Group.objects.create(course=self.course, name=f"{self.course.name}, group #{len(self.groups) + 1}")
        self.groups.append(new_group)
        return new_group
    
    def _remove_group(self) -> None:
        logger.info('Удаляем группу')
        removed_group = self.groups.pop()
        removed_group.delete()
    
    def _delete_group_student_through(self) -> None:
        logger.info('Удаляем запись в побочной группе')
        GroupStudents.objects.filter(group__course=self.course).delete()

    def _get_available_group(self) -> Optional[Group]:
        logger.info('Поиск доступных групп')
        group = min(
            filter(lambda group: group.student_count < self.max_group_size, self.groups), 
            key=lambda group: group.students_count, 
            default=None,
        )
        if group:
            self.__need_to_rebalance = False
        return group
    
    def _is_course_started(self):
        return self.course.date_time_start >= timezone.now()