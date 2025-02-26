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
            self.page.wait_for_load_state('networkidle', timeout=30000)  # Ожидание загрузки завершено
        except TimeoutError:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_on_timeout",
                attachment_type=allure.attachment_type.PNG
            )
            print("Предупреждение: Время ожидания загрузки страницы истекло. Продолжаем выполнение теста.")
    
    @allure.step("Кликнуть на элемент по XPath {xpath}")
    def click_element_by_xpath(self, xpath: str):
        self.page.locator(f'xpath={xpath}').click()  # Выполняем клик на элемент

    @allure.step("Заполнить элемент по XPath {xpath} значением '{value}'")
    def fill_element_by_xpath(self, xpath: str, value: str):
        self.page.locator(f'xpath={xpath}').fill(value)  # Заполняем элемент указанным значением





