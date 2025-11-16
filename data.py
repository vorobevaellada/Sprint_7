import fakes


class ApiUrls:
    MAIN_URL = 'https://qa-scooter.praktikum-services.ru/'  # Основная страница сервиса Яндекса Самокат
    CREATE_COURIER = 'api/v1/courier'              # Ручка для создания нового курьера
    COURIER_AUTHENTICATE = 'api/v1/courier/login'  # Ручка для авторизации курьера
    DELETE_COURIER = 'api/v1/courier/'             # Ручка для удаления аккаунта курьера
    CREATE_ORDER = 'api/v1/orders'                 # Ручка для создания заказа
    GET_ORDERS = 'api/v1/orders'                  # Ручка для получения списка заказов
    TRACK_ORDER_STATUS = '/api/v1/orders/track?t=' # Ручка для отслеживания статуса заказа
    CANCEL_ORDER = 'api/v1/orders/cancel?track='   # Ручка для отмены заказа



class DataForOrder:
    order_payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-06-06",
        "comment": "Saske, come back to Konoha"
        }
    
    color = [['BLACK'], ['GREY'], (['BLACK'], ['GREY']), ['']]

class DataForRegistration:
    # Список наборов данных для регистрации
    registration_payload = [
        # Первый набор: содержит только пароль и имя
        {'password': fakes.generate_random_password(), 'first_name': fakes.generate_first_name()},
        # Второй набор: содержит только логин и имя
        {'login': fakes.generate_user_login(), 'first_name': fakes.generate_first_name()}
    ]