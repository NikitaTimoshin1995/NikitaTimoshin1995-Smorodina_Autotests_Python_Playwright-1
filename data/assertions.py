import allure
from playwright.sync_api import Page, expect
import re
import psycopg2

class Assertions:
    def __init__(self, page: Page):
        self.page = page

    @allure.step('Проверка URL')
    def check_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url)

    @allure.step('Проверка статусов запросов. Что все с кодом 200')
    def check_request_statuses(self, requests):
        for request in requests:
            response = request.response()  # Получаем ответ
            assert response is not None, f"Запрос {request.url} не получил ответа"
            assert response.status in (200, 302), f"Запрос {request.url} завершился с кодом {response.status}"

    @allure.step('Проверка наличия ошибки "{text}"')
    def check_div_with_text(self, text: str):
        locator = self.page.locator(f"div.text:has-text('{text}')")
        expect(locator).to_be_visible()

    @allure.step('Проверка выделения красным поля "{xpath}"')
    def check_border_style_by_xpath(self, xpath: str):
        locator = self.page.locator(f"xpath={xpath}")
        expect(locator).to_have_class(re.compile(r".*\binvalid\b.*"))

    @allure.step('Проверка успешного создания пользователя в базе данных')
    def check_user_in_db(self, db_connection, email: str, phone: str, active: int, consent_advertising: int):
        cursor = db_connection.cursor()
        query = "SELECT login, active, email, phone, consent_advertising FROM users WHERE email = %s"
        cursor.execute(query, (email,))  # Используем параметризированный запрос для предотвращения SQL инъекций

        user = cursor.fetchone()
        cursor.close()

        assert user is not None, f"Пользователь с email: {email} не найден в базе данных."

        login, user_active, user_email, user_phone, user_consent_advertising = user

        assert login == email, f"Email не совпадает. Ожидалось: {email}, но получено: {login}"
        assert user_active == active, f"Active статус не совпадает. Ожидалось: {active}, но получено: {user_active}"
        assert user_email == email, f"Email не совпадает. Ожидалось: {email}, но получено: {user_email}"
        assert user_phone == phone, f"Телефон не совпадает. Ожидалось: {phone}, но получено: {user_phone}"
        assert user_consent_advertising == consent_advertising, f"Согласие на рекламу не совпадает. Ожидалось: {consent_advertising}, но получено: {user_consent_advertising}"