# Тесты на создание заказа и получение списка заказов
import json
import requests

import allure
import pytest

from data import ApiUrls, DataForOrder



class TestCreateOrder:

    @pytest.mark.usefixtures("create_and_cancel_order")
    @allure.title("Тест успешного создания заказа самоката с разными цветами")
    @pytest.mark.parametrize('color', DataForOrder.color)
    def test_order_creation_with_colors(self, color):
        """Проверка создание заказа с разными цветами"""
        
        with allure.step("Подготавливаю данные заказа с нужным цветом"):
            # Используем тот же самый объект self.track, полученный из фикстуры
            order_payload = DataForOrder.order_payload.copy()
            order_payload['color'] = color
            
        with allure.step("Отправляю POST-запрос на создание заказа"):
            # Повторно отправляем запрос на создание заказа с новым цветом
            response = requests.post(f"{ApiUrls.MAIN_URL}{ApiUrls.CREATE_ORDER}", json=order_payload)
        
        with allure.step("Проверяю успешное создание заказа и наличие трек-кода"):
            # Проверка успешного создания заказа и наличия трека
            assert response.status_code == 201 and 'track' in response.json(), \
                f"Заказ с данным цветом не создан {color}: {response.text}"



class TestOrdersList:

    @allure.title("Тест успешного получения списка заказов")
    def test_getting_orders_list_success(self):
        """Проверяет получение списка заказов через GET-запрос."""
        
        with allure.step("Отправляю GET-запрос на получение списка заказов"):
            # Отправляем запрос на получение списка заказов
            response = requests.get(f'{ApiUrls.MAIN_URL}{ApiUrls.GET_ORDERS}')
        
        with allure.step("Проверяю успешность запроса и наличие массива заказов"):
            # Проверяем успешность запроса и наличие массива заказов
            assert response.status_code == 200 and 'orders' in response.json(), \
                   f"Список заказов не получен. Ответ сервера: {response.text}"