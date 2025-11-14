# Тесты на создание заказа и получение списка заказов
import json
import requests

import allure
import pytest

from data import ApiUrls, DataForOrder


class TestCreateOrder:

    @allure.title("Тест успешного создания заказа самоката с разными цветами")
    @pytest.mark.parametrize('color', DataForOrder.color, )
    def test_order_creation_with_colors(self, color):
        """Проверка создание заказа с разными цветами"""
        
        # Необходимые данные заказа + нужный цвет
        order_payload = DataForOrder.order_payload.copy()
        order_payload['color'] = color
        
        # Отправка POST-запроса на создание заказа
        response = requests.post(f'{ApiUrls.MAIN_URL}{ApiUrls.CREATE_ORDER}', json=order_payload)
        
        # Проверка успешного создания заказа и наличия трека
        assert response.status_code == 201 and 'track' in response.json(), \
            f"Заказ с данным цветом не создан {color}: {response.text}"
            
        # Отмена созданного заказа
        requests.put(f'{ApiUrls.MAIN_URL}{ApiUrls.CANCEL_ORDER}{response.json()["track"]}')



class TestOrdersList:

    @allure.title("Тест успешного получения списка заказов")
    def test_getting_orders_list_success(self):
        """Проверяет получение списка заказов через GET-запрос."""
        
        # Отправляем запрос на получение списка заказов
        response = requests.get(f'{ApiUrls.MAIN_URL}{ApiUrls.GET_ORDERS}')
        
        # Проверяем успешность запроса и наличие массива заказов
        assert response.status_code == 200 and 'orders' in response.json(), \
               f"Список заказов не получен. Ответ сервера: {response.text}"