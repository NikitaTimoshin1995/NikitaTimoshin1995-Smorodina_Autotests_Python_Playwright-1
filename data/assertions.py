import allure
from playwright.sync_api import Page, expect 

class Assertions:
    def __init__(self, page: Page):
        self.page = page

    @allure.step('Проверка URL')
    def check_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url)

