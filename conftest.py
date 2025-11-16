import fakes
import pytest
import requests


from data import ApiUrls, DataForOrder


@pytest.fixture
def register_and_authenticate_courier():
    """
    Фикстура для создания и последующего удаления тестового курьера.
    Возвращает кортеж с данными регистрации и аутентификации.
    """
    courier_login = fakes.generate_user_login()
    courier_password = fakes.generate_random_password()
    courier_name = fakes.generate_first_name()
    
    # Данные для регистрации курьера
    courier_registration_data = {
        'login': courier_login,
        'password': courier_password,
        'first_name': courier_name
    }
    
    # Регистрация курьера
    register_response = send_post_request(ApiUrls.CREATE_COURIER, courier_registration_data)
    
    # Получаем id зарегистрированного курьера
    auth_response = authenticate_courier(courier_login, courier_password)
    courier_id = auth_response.json().get('id')
    
    # Данные для аутентификации курьера
    courier_auth_data = {
        'login': courier_login,
        'password': courier_password
    }
    
    yield [
        courier_registration_data,  # Для проверки создания
        courier_auth_data,          # Для тестирования авторизации
        courier_login,              # Логин для дальнейших проверок
        courier_password,           # Пароль для последующих тестов
        courier_id                  # Идентификатор для удаления
    ]
    
    # Удаляем аккаунт курьера после завершения тестов
    delete_courier(courier_id)


@pytest.fixture
def generate_random_courier():
    """
    Фикстура для генерации случайных данных курьера.
    Используется в тестах создания новых курьеров.
    """
    courier_login = fakes.generate_user_login()
    courier_password = fakes.generate_random_password()
    courier_name = fakes.generate_first_name()
    
    # Данные для регистрации курьера
    courier_registration_data = {
        'login': courier_login,
        'password': courier_password,
        'first_name': courier_name
    }
    
    # Данные для аутентификации курьера
    courier_auth_data = {
        'login': courier_login,
        'password': courier_password
    }
    
    yield [courier_registration_data, courier_auth_data]
    
    # Аутентификация и последующее удаление тестового курьера
    auth_response = authenticate_courier(courier_login, courier_password)
    if auth_response.ok:
        courier_id = auth_response.json().get('id')
        delete_courier(courier_id)


# Вспомогательные методы для обработки HTTP-запросов
def send_post_request(url_path, payload):
    return requests.post(f'{ApiUrls.MAIN_URL}{url_path}', json=payload)


def authenticate_courier(login, password):
    auth_payload = {'login': login, 'password': password}
    return send_post_request(ApiUrls.COURIER_AUTHENTICATE, auth_payload)


def delete_courier(courier_id):
    return requests.delete(f'{ApiUrls.MAIN_URL}{ApiUrls.DELETE_COURIER}{courier_id}')



@pytest.fixture(scope="function")  
def create_and_cancel_order(request):
    """
    Фикстура для создания и последующей отмены заказа.
    Автоматически создает заказ перед каждым тестом и отменяет его после окончания теста.
    """
    # Создание заказа
    order_payload = DataForOrder.order_payload.copy()
    response = requests.post(f"{ApiUrls.MAIN_URL}{ApiUrls.CREATE_ORDER}", json=order_payload)
    
    # Если заказ успешно создан, получаем track-код
    if response.status_code == 201:
        track = response.json()['track']
    else:
        raise Exception(f"Ошибка при создании заказа: {response.text}")
    
    # Передаем track-код в тестовую функцию
    request.cls.track = track
    
    yield track  # Предоставляет track-код тестовым методам
    
    # После выполнения теста отменить заказ
    cancel_response = requests.put(f"{ApiUrls.MAIN_URL}{ApiUrls.CANCEL_ORDER}?track={track}")
    if not cancel_response.ok:
        print(f"Ошибка при отмене заказа: {cancel_response.text}")  # выводим ошибку в консоль, но продолжаем работу
