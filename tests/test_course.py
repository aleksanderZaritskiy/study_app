from datetime import datetime, timedelta
from http import HTTPStatus

from django.utils import timezone
import pytest

from .utils import create_lesson, create_pa, create_users_data
from study.models import Group


@pytest.mark.django_db(transaction=True)
class TestCourseAPI:

    URL_COURSES = '/api/course/'
    URL_COURSE = '/api/course/{course_id}/'
    URL_LESSONS = '/api/course/{course_id}/lessons/'

    def test_course_endpoint_exists(self, client):
        response = client.get(self.URL_COURSES)

        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), f'Убедитесь, что эндпоинт {self.URL_COURSES} подключен к роутингу'

    def test_not_auth_request(self, client):
        response = client.get(self.URL_COURSES)

        assert (
            response.status_code == HTTPStatus.UNAUTHORIZED
        ), f'Убедитесь, что анонимный запрос к эндпоинту {self.URL_COURSES} возвращает 401 статус'

    def test_auth_request(self, user_client):
        response = user_client.get(self.URL_COURSES)

        assert (
            response.status_code == HTTPStatus.OK
        ), f'Убедитесь, что для авторизированного пользователя энпоинт {self.URL_COURSES} доступен со статусом 200'

    def test_course_request_other_then_get(self, create_course, user_client):

        url_cur_course = self.URL_COURSE.format(course_id=create_course.id)

        not_allowed_method = (
            ('post', self.URL_COURSES, 'METHOD_NOT_ALLOWED'),
            ('put', url_cur_course, 'NOT_FOUND'),
            ('patch', url_cur_course, 'NOT_FOUND'),
            ('delete', url_cur_course, 'NOT_FOUND'),
        )
        for method, url, status in not_allowed_method:
            response = getattr(user_client, method)(url)
            assert response.status_code == getattr(
                HTTPStatus, status
            ), f'Убедитесь метод {method} не поддерижвается для {url}'

    def test_auth_user_can_see_courses_for_purchase(
        self, author, create_course, user_client
    ):
        response = user_client.get(self.URL_COURSES)
        response_json = response.json()[0]
        assert (
            response_json['name'] == create_course.name
        ), f'Убедитесь, что пользователю доступны курсы, которые ещё не куплены'

        course_data = {
            'author_name': author.username,
            'name': 'TestCourse',
            'date_time_start': timezone.now() + timedelta(days=30),
            'cost': 10000,
            'min_group_people': 2,
            'max_group_people': 5,
            'lessons_count': 0,
            'students_count': 0,
            'avg_groups': 0,
            'course_purchase': 0,
        }
        for field, value in response_json.items():

            if field == 'date_time_start':
                value = (
                    datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
                    .replace(tzinfo=timezone.utc)
                    .replace(microsecond=0, second=0)
                )
                course_data[field] = course_data[field].replace(microsecond=0, second=0)

            assert field in course_data, f'Отсутсвуют ожидаемые данные о курсе {field}'
            assert (
                course_data[field] == value
            ), f'Значение {field} не соответсвуют фактическим данным о курсе {course_data[field]} != {value}'

    def test_not_auth_user_lessons_request(self, create_course, client):
        url_course_lessons = self.URL_LESSONS.format(course_id=create_course.id)
        response = client.get(url_course_lessons)
        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), f'Убедитесь, что эндпоинт {url_course_lessons} добавлен в urls.py'
        assert (
            response.status_code == HTTPStatus.UNAUTHORIZED
        ), f'Для не авторизованного пользователя {url_course_lessons} должен возвращать 401 статус'

    def test_auth_user_cant_see_course_already_purchase(
        self, create_course, user_with_pa, user_client
    ):
        response = user_client.get(self.URL_COURSES)
        response_json = response.json()
        assert (
            not response_json
        ), f'Убедитесь, что пользователю не видны курсы, которые он уже купил'

    def test_with_pa_can_see_lessons(self, create_lessons, user_with_pa, user_client):
        url_course_lessons = self.URL_LESSONS.format(course_id=create_lessons.course.id)
        response = user_client.get(url_course_lessons)

        assert (
            response.status_code == HTTPStatus.OK
        ), f'Убедитесь, что {url_course_lessons} доступен для пользователя с PA'
        response_json = response.json()[0]
        assert (
            response_json['name'] == create_lessons.name
        ), 'Убедитесь, что пользователю доступны уроки при имеющейся подписке на курс'
        expected_lesson_fields = ('name', 'link_to_video')
        for exp_field in expected_lesson_fields:
            assert (
                exp_field in response_json
            ), f'Отсутсвует обязательное поле для уроков {exp_field}'

    def test_wihtout_pa_cant_see_lessons(self, create_lessons, user_client):
        url_course_lessons = self.URL_LESSONS.format(course_id=create_lessons.course.id)
        response = user_client.get(url_course_lessons)

        assert (
            response.status_code == HTTPStatus.FORBIDDEN
        ), f'Убедитесь, что пользователю без PA не доступны уроки'

    def test_course_statistics_fields(
        self, create_course, user_client, django_user_model
    ):
        lessons_count = create_lesson(create_course)
        students_count = create_pa(create_users_data(), django_user_model, create_course)
        groups_count = Group.objects.filter(course=create_course).count()
        users_count = django_user_model.objects.all().count()

        response = user_client.get(self.URL_COURSES)
        response_json = response.json()[0]
        statistics_fields = (
            ('lessons_count', lessons_count),
            ('students_count', students_count),
            (
                'avg_groups',
                round(
                    (groups_count * students_count / groups_count)
                    / create_course.max_group_people
                    * 100,
                    2,
                ),
            ),
            ('course_purchase', round(students_count / users_count * 100, 2)),
        )
        for field, value in statistics_fields:
            assert (
                response_json[field] == value
            ), f'Статические данные {field} для курса вычисляются неверно. Результат {response_json[field]} != {value}'
