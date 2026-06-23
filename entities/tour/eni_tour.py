import allure
import requests
from Constants.client.client_auth.const_client_auth import (
    CLIENT_LOGIN_REQUEST_URL,
    CLIENT_CONFIRM_REQUEST_URL,
    CLIENT_PHONE1,
    CLIENT_CONFIRM_PHONE_CODE 
)
from Constants.const_general import URL


class TourAPI:


    @allure.step('Смена статуса тура')
    def patch_company_start(self, tour_id: int, status: int):
        try:
            # Аутентификация
            auth_url = CLIENT_LOGIN_REQUEST_URL
            auth_payload = {"phone": CLIENT_PHONE1}
            auth_response = requests.post(auth_url, json=auth_payload, timeout=10)          
            if auth_response.status_code != 200:
                error_msg = f"Ошибка аутентификации: {auth_response.status_code} - {auth_response.text}"
                allure.attach(error_msg, name="Auth Error")
                raise ValueError(error_msg)
            # Подтверждение кода
            confirm_url = CLIENT_CONFIRM_REQUEST_URL
            confirm_payload = {
                "phone": CLIENT_PHONE1,
                "confirmation_code": CLIENT_CONFIRM_PHONE_CODE
            }
            confirm_response = requests.post(confirm_url, json=confirm_payload, timeout=10)    
            if confirm_response.status_code != 200:
                error_msg = f"Ошибка подтверждения: {confirm_response.status_code} - {confirm_response.text}"
                allure.attach(error_msg, name="Confirm Error")
                raise ValueError(error_msg)
            # Получаем токен
            try:
                token = confirm_response.json().get('user', {}).get('token')
                if not token:
                    raise ValueError("Токен не найден в ответе")
            except Exception as e:
                error_msg = f"Ошибка получения токена: {str(e)}. Ответ: {confirm_response.text}"
                allure.attach(error_msg, name="Token Error")
                raise ValueError(error_msg)
            # Основной запрос
            update_url = f'{URL.rstrip("/")}/api/admin/tours/{tour_id}/details-params'  
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            payload = {"status_id": status}
            response = requests.patch(update_url, headers=headers, json=payload, timeout=10)
            # Логирование ответа
            print(f"Response status: {response.status_code}")
            try:
                response_json = response.json()
                print(f"Response JSON: {response_json}")
                allure.attach(str(response_json), name="Response JSON", attachment_type=allure.attachment_type.JSON)
            except ValueError:
                print(f"Response text (not JSON): {response.text}")
                allure.attach(response.text, name="Response Text", attachment_type=allure.attachment_type.TEXT)
            if response.status_code != 200:
                error_msg = f"Ошибка запроса: {response.status_code} - {response.text}"
                allure.attach(error_msg, name="Request Error")
                raise ValueError(error_msg) 
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка сети: {str(e)}"
            allure.attach(error_msg, name="Network Error")
            raise
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            allure.attach(error_msg, name="Unexpected Error")
            raise


    @allure.step('Смена статуса продукта')
    def change_product_status(self, product_id: int, status: int):
        try:
            auth_url = CLIENT_LOGIN_REQUEST_URL
            auth_payload = {"phone": CLIENT_PHONE1, "consent_personal_data": 1}
            auth_response = requests.post(auth_url, json=auth_payload, timeout=10)
            if auth_response.status_code != 200:
                error_msg = f"Ошибка аутентификации: {auth_response.status_code} - {auth_response.text}"
                allure.attach(error_msg, name="Auth Error")
                raise ValueError(error_msg)
            confirm_url = CLIENT_CONFIRM_REQUEST_URL
            confirm_payload = {
                "phone": CLIENT_PHONE1,
                "confirmation_code": CLIENT_CONFIRM_PHONE_CODE
            }
            confirm_response = requests.post(confirm_url, json=confirm_payload, timeout=10)
            if confirm_response.status_code != 200:
                error_msg = f"Ошибка подтверждения: {confirm_response.status_code} - {confirm_response.text}"
                allure.attach(error_msg, name="Confirm Error")
                raise ValueError(error_msg)
            try:
                response_json = confirm_response.json()
                token = response_json.get('token')
                if not token:
                    token = (response_json.get('data', {}).get('token') or 
                            response_json.get('user', {}).get('token'))
                if not token:
                    raise ValueError("Токен не найден в ответе")
            except Exception as e:
                error_msg = f"Ошибка получения токена: {str(e)}. Ответ: {confirm_response.text}"
                allure.attach(error_msg, name="Token Error")
                raise ValueError(error_msg)
            status_url = f'{URL.rstrip("/")}/api/admin/product-change-status/{product_id}/{status}'
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            response = requests.get(status_url, headers=headers, timeout=10)
            try:
                response_json = response.json()
                allure.attach(str(response_json), name="Response JSON", attachment_type=allure.attachment_type.JSON)
            except ValueError:
                allure.attach(response.text, name="Response Text", attachment_type=allure.attachment_type.TEXT)
            if response.status_code != 200:
                error_msg = f"Ошибка запроса: {response.status_code} - {response.text}"
                allure.attach(error_msg, name="Request Error")
                raise ValueError(error_msg)
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Ошибка сети: {str(e)}"
            allure.attach(error_msg, name="Network Error")
            raise
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            allure.attach(error_msg, name="Unexpected Error")
            raise

    @allure.step('Включение/выключение предварительного бронирования')
    def change_product_booking(self, db_connection, product_name: str, position: bool):
        try:
            with db_connection.cursor() as cursor:
                update_query = """
                    UPDATE products 
                    SET advance_booking = %s 
                    WHERE name = %s AND advance_booking != %s;
                """
                cursor.execute(update_query, (position, product_name, position))
                db_connection.commit()
                rows_updated = cursor.rowcount
                if rows_updated > 0:
                    message = f"Значение advance_booking установлено в {position} для продукта '{product_name}'"
                else:
                    message = f"Значение advance_booking уже равно {position} для продукта '{product_name}' или продукт не найден"
                allure.attach(message, name="Результат обновления")
                print(f"(ИНФО) {message}")
                return rows_updated > 0
        except Exception as ex:
            db_connection.rollback()
            allure.attach(f"Ошибка при обновлении advance_booking: {ex}", name="Ошибка БД")
            print(f"(ОШИБКА) Проблема при обновлении advance_booking: {ex}")
            raise


