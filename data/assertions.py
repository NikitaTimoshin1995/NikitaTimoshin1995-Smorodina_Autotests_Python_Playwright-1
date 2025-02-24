import allure
from playwright.sync_api import Page, Response

class Assertions:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Проверка, что все запросы с кодом 200")
    def assert_request_statuses(self, requests):
        for request in requests:
            response: Response = request.response()
            assert response and response.status == 200, (
                f"Запрос {request.url} вернул статус {response.status}"
            )