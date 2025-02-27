import allure
from playwright.sync_api import Page, expect
import re

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
        # Локатор для поиска div с классом "text" и указанным текстом
        locator = self.page.locator(f"div.text:has-text('{text}')")
        # Проверяем, что элемент видим на странице
        expect(locator).to_be_visible()

    @allure.step('Проверка выделения красным поля "{xpath}"')
    def check_border_style_by_xpath(self, xpath: str):
        # Локатор для поиска элемента по XPath
        locator = self.page.locator(f"xpath={xpath}")
        # Проверяем, что у элемента есть класс "invalid" (игнорируя лишние пробелы)
        expect(locator).to_have_class(re.compile(r".*\binvalid\b.*"))