import allure
from playwright.sync_api import Page, TimeoutError  # Импортируем TimeoutError из playwright.sync_api

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открытие страницы {url}")
    def open_page(self, url: str):
        self.page.goto(url)
        self.wait_for_full_load()  # Ожидаем загрузки страницы

    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_full_load(self):
        try:
            self.page.wait_for_load_state('networkidle')  # Ожидание загрузки завершено
        except TimeoutError:
            print("Время ожидания загрузки страницы истекло.")



