import logging

from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from study.models import PassAccess, Group
from services.groups_rebalance import GroupRebalance


logger = logging.getLogger(__name__)


def get_groups(course):
    groups = Group.objects.filter(course=course).annotate(students_count=Count('student')).select_related('course').prefetch_related('student')
    return list(groups)

@receiver(post_save, sender=PassAccess)
def create_group(sender, instance, created, **kwargs):
    """ ..."""
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
        
