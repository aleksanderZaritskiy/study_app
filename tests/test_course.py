from datetime import datetime, timedelta
from http import HTTPStatus

from django.utils import timezone
import pytest

#from backend.study.constants import DATETIME_COURSE_START


@pytest.mark.django_db(transaction=True)
class TestCourseAPI:

    URL_COURSES = '/api/course/'
    URL_COURSE = '/api/course/{course_id}/'

    def test_course_endpoint_exists(self, client):
        response = client.get(self.URL_COURSES)

        assert response.status_code != HTTPStatus.NOT_FOUND, (f'Убедитесь, что эндпоинт {self.URL_COURSES} подключен к роутингу')

    def test_not_auth_request(self, client):
        response = client.get(self.URL_COURSES)

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (f'Убедитесь, что анонимный запрос к эндпоинту {self.URL_COURSES} возвращает 401 статус')

    def test_auth_request(self, user_client):
        response = user_client.get(self.URL_COURSES)

        assert response.status_code == HTTPStatus.OK, (f'Убедитесь, что для авторизированного пользователя энпоинт {self.URL_COURSES} доступен со статусом 200')

    def test_course_request_other_then_get(self, create_course, user_client):

        url_cur_course = self.URL_COURSE.format(course_id=create_course.id)

        not_allowed_method = (
            ('post', self.URL_COURSES, 'METHOD_NOT_ALLOWED'), 
            ('put', url_cur_course, 'NOT_FOUND'), 
            ('patch', url_cur_course, 'NOT_FOUND'), 
            ('delete', url_cur_course, 'NOT_FOUND')
        )
        for method, url, status in not_allowed_method:
            response = getattr(user_client, method)(url)
            assert response.status_code == getattr(HTTPStatus, status), (f'Убедитесь метод {method} не поддерижвается для {url}')

    def test_auth_user_can_see_courses_for_purchase(self, author, create_course, user_client):
        response = user_client.get(self.URL_COURSES)
        response_json = response.json()[0]
        assert response_json['name'] == create_course.name, (f'Убедитесь, что пользователю доступны курсы, которые ещё не куплены')

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
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc).replace(microsecond=0)
                course_data[field] = course_data[field].replace(microsecond=0)

            assert field in course_data, (f'Отсутсвуют ожидаемые данные о курсе {field}')
            assert course_data[field] == value, (f'Значение {field} не соответсвуют фактическим данным о курсе {course_data[field]} != {value}')
    
    def test_auth_user_cant_see_course_already_purchase(self, create_course, user_with_pa, user_client):
        response = user_client.get(self.URL_COURSES)
        response_json = response.json()
        assert not response_json, (f'Убедитесь, что пользователю не видны курсы, которые он уже купил')
