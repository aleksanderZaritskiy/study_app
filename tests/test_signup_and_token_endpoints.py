from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class TestUserRegistation:
    URL_SIGNUP = '/api/users/'
    URL_TOKEN = '/api/auth/token/login/'
    URL_LOGOUT = '/api/auth/token/logout/'

    def test_nodata_signup(self, client):
        response = client.post(self.URL_SIGNUP)
        assert response.status_code != HTTPStatus.FORBIDDEN, (
            f'endpoint {self.URL_SIGNUP} должен быть доступен анонимному юзеру'
        )
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'endpoint {self.URL_SIGNUP} не найден'
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            'не содержит необходимых данных, должен вернуться ответ со '
            'статусом 400.'
        )
        
        response_json = response.json()
        empty_fields = ['password', 'username']
        for field in empty_fields:
            
            assert (field in response_json and isinstance(response_json.get(field), list)), (
                f'Если в POST-запросе к `{self.URL_SIGNUP}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях.'
            )

    def test_singup_access(self, client):
        valid_user_data = {
            'username': 'test_user',
            'password': 'test_password22',
        }
        
        response = client.post(self.URL_SIGNUP, data=valid_user_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (f'Проверьте {self.URL_SIGNUP} в urls.py, т.к. запрос возвращает 404')
        assert response.status_code != HTTPStatus.FORBIDDEN, (f'Убедитесь, что доступ эндпоинту {self.URL_SIGNUP} имеют все пользователи с валидными данными')
        assert response.status_code == HTTPStatus.CREATED, (f'Убедитесь что запрос к эндпоинту {self.URL_SIGNUP} с валидными данными возвращает статус 200')

    def test_login_access(self, client):
        valid_user_data = {
            'username': 'test_user',
            'password': 'test_password22',
        }
        response = client.post(self.URL_SIGNUP, data=valid_user_data)
        response = client.post(self.URL_TOKEN, data=valid_user_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (f'Проверьте {self.URL_TOKEN} в urls.py, т.к. запрос возвращает 404')
        assert response.status_code != HTTPStatus.FORBIDDEN, (f'Убедитесь, что доступ эндпоинту {self.URL_TOKEN} имеют все пользователи с валидными данными')
        assert response.status_code == HTTPStatus.OK, (f'Убедитесь что запрос к эндпоинту {self.URL_TOKEN} с валидными данными возвращает статус 200')

    def test_logout_access(self, user_client):
        response = user_client.post(self.URL_LOGOUT)
        
        assert response.status_code != HTTPStatus.NOT_FOUND, (f'Проверьте {self.URL_LOGOUT} в urls.py, т.к. запрос возвращает 404')
        assert response.status_code != HTTPStatus.FORBIDDEN, (f'Убедитесь, что доступ эндпоинту {self.URL_LOGOUT} имеют авторизированные пользователи')
        assert response.status_code == HTTPStatus.NO_CONTENT, (f'Убедитесь что запрос к эндпоинту {self.URL_TOKEN} возвращает статус 204')
