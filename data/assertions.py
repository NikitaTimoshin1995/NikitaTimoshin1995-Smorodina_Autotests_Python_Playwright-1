import allure
from playwright.sync_api import Page, expect 

class Assertions:
    def __init__(self, page: Page):
        self.page = page

    @allure.step('Проверка URL')
    def check_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url)

    @allure.step('Проверка статусов запросов')
    def check_request_statuses(self, requests):
        for request in requests:
            assert request.response.status == 200, f"Запрос {request.url} завершился с кодом {request.response.status}"