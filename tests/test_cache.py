import pytest

from django.core.cache import cache


@pytest.mark.django_db(transaction=True)
class TestCache:
    URL_LESSON = '/api/course/{course_id}/lessons/'

    def test_cache_lessons_and_pa(self, user, user_client, user_with_pa, create_lessons):
        course_id = create_lessons.course.id
        cache_pa_key = f'{user}_lessons_course_{course_id}'
        cache_lesson_key = f'lessons_course_{course_id}'

        url = self.URL_LESSON.format(course_id=course_id)
        _ = user_client.get(url)

        assert cache.get(
            cache_pa_key
        ), f'При запросе к {url} данные об PA студента не кешируются'
        assert cache.get(
            cache_lesson_key
        ), f'При запросе к {url} данные об уроках студента не кешируются'

        create_lessons.link_to_video = 'https://www.youtube.com/watch?v=mwUWwMFAVwM'
        create_lessons.save()

        assert not cache.get(
            cache_lesson_key
        ), f'После изменений в объекте урока данные кеша должны быть удалены'

        create_lessons.delete()

        assert not cache.get(
            cache_lesson_key
        ), f'После изменений в объекте урока данные кеша должны быть удалены'

        user_with_pa.is_valid = False
        user_with_pa.save()

        assert not cache.get(
            cache_pa_key
        ), f'Если студент теряет PA, данные кеша должны быть удалены'

    # def test_clear_cache_lessons(self, user_client, user_with_pa, create_lessons):
    #     course_id = create_lessons.course.id
    #     cache_lesson_key = f'lessons_course_{course_id}'
    #     url = self.URL_LESSON.format(course_id=course_id)
    #     _ = user_client.get(url)
