import logging

from django.core.cache import cache
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from study.models import PassAccess, Group, Lesson
from services.groups_rebalance import GroupRebalance


logger = logging.getLogger(__name__)


def get_groups(course):
    groups = Group.objects.filter(course=course).annotate(students_count=Count('student')).select_related('course').prefetch_related('student')
    return list(groups)

@receiver(post_save, sender=PassAccess)
def create_group(sender, instance, created, **kwargs):
    """ 
    При получении доступа к курсу, студент должен быть распределен в группу.
    Если курс ещё не начался. При каждом новом допуске группы должны быть ребалансированы n +-1.
    Ребалансировка групп и побочный функционал реализованы в интерфейсе GroupRebalance в services.groups_rebalance
    """

    logger.info('Запуск сигнала')

    student = instance.student
    course = instance.course 

    group_rebalance = GroupRebalance(student, course, get_groups(course))

    if created:

        if instance.is_valid:
            logger.info('Запуск процесса добавления в группу')
            group_rebalance.add()
            logger.info('Участник добавлен в группу')

        else:
            logger.info('У пользователя не подтвержден PA')
    else:
        
        if not instance.is_valid:
            logger.info('У пользователя отобрали PA')
            group = Group.objects.filter(course=course, student=student).first()
            group.student.remove(student)

            group_rebalance.groups = get_groups(course)
            group_rebalance.rebalance()
            logger.info('Группы ребалансированы')
            
            cache.delete(f'{student}_course_{course.id}')
            logger.info(f'Кеш {student} очищен')
        

@receiver(post_delete, sender=Lesson)
@receiver(post_save, sender=Lesson)
def clear_cache_lessons(sender, instance, **kwargs):
    course_id = instance.course.id
    cache.delete(f'lessons_course_{course_id}')
    logger.info(f'Произошли изменения над объектом Lesson, курса {course_id}. Кеш очищен')