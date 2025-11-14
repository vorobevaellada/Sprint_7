# Тесты на создание курьера и логин курьера
import allure
import fakes
import pytest
import requests

from data import ApiUrls, DataForRegistration


class TestsCreateNewCourier:

    @allure.title("Тест успешного создания нового курьера")
    def test_create_new_courier(self, generate_random_courier):
        # Отправляем POST-запрос на создание курьера
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.CREATE_COURIER}",
            json=generate_random_courier[0]
        )
        # Проверяем, что курьер успешно создан (статус 201 и ответ {"ok": True})
        assert response.status_code == 201 and response.json() == {"ok": True}

    @allure.title("Ошибка при попытке создать курьера без логина или пароля")
    @pytest.mark.parametrize('data_setup', DataForRegistration.registration_payload)
    def test_cannot_create_courier_without_login_or_password(self, data_setup):
        # Отправляем POST-запрос на создание курьера с неполными данными
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.CREATE_COURIER}",
            json=data_setup
        )
        # Проверяем, что возвращается ошибка 400 и сообщение "Недостаточно данных..."
        assert (
            response.status_code == 400 and 
            response.json()["message"] == "Недостаточно данных для создания учетной записи"
        )

    @allure.title("Ошибка при попытке создать уже существующего курьера")
    def test_cannot_create_duplicate_courier(self, register_and_authenticate_courier):
        # Отправляем POST-запрос на создание курьера с существующими данными
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.CREATE_COURIER}",
            json=register_and_authenticate_courier[0]
        )
        # Проверяем, что возвращается ошибка 409 и сообщение "Этот логин уже используется..."
        assert (
            response.status_code == 409 and 
            response.json()["message"] == "Этот логин уже используется. Попробуйте другой."
        )


class TestLoginCourier:

    @allure.title("Тест успешной авторизации курьера")
    def test_courier_authentication_success(self, register_and_authenticate_courier):
        # Отправляем POST-запрос на авторизацию курьера
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.COURIER_AUTHENTICATE}",
            json=register_and_authenticate_courier[1]
        )
        # Сохраняем полученный ID курьера
        courier_account_id = response.json()
        # Проверяем, что авторизация выполнена успешно (статус 200 и присутствует ID)
        assert response.status_code == 200 and "id" in courier_account_id

    @allure.title("Ошибка при попытке авторизоваться несуществующим курьером")
    def test_failed_courier_authentication(self):
        # Формируем некорректные данные для авторизации
        login_data = {
            "login": fakes.generate_user_login(),
            "password": fakes.generate_random_password()
        }
        # Отправляем POST-запрос на авторизацию несуществующего курьера
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.COURIER_AUTHENTICATE}",
            json=login_data
        )
        # Проверяем, что авторизация невозможна (ошибка 404 и сообщение "Учетная запись не найдена")
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Ошибка при попытке авторизоваться только с логином")
    def test_login_only_with_username(self, register_and_authenticate_courier):
        # Готовим данные для авторизации без пароля
        response_data = {
            "login": register_and_authenticate_courier[2],
            "password": ""
        }
        # Отправляем POST-запрос на авторизацию без пароля
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.COURIER_AUTHENTICATE}",
            json=response_data
        )
        # Проверяем, что авторизация невозможна (ошибка 400 и сообщение "Недостаточно данных...")
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при попытке авторизоваться только с паролем")
    def test_login_only_with_password(self, register_and_authenticate_courier):
        # Готовим данные для авторизации без логина
        response_data = {
            "login": "",
            "password": register_and_authenticate_courier[3]
        }
        # Отправляем POST-запрос на авторизацию без логина
        response = requests.post(
            f"{ApiUrls.MAIN_URL}{ApiUrls.COURIER_AUTHENTICATE}",
            json=response_data
        )
        # Проверяем, что авторизация невозможна (ошибка 400 и сообщение "Недостаточно данных...")
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"