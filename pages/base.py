import allure
from playwright.sync_api import Page, TimeoutError
from Locators.locator_main_page import LOCATORS

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открытие страницы {url}")
    def open_page(self, url: str):
        self.page.goto(url)
        self.wait_for_full_load()

    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_full_load(self):
        try:
            self.page.wait_for_load_state('networkidle', timeout=30000)
        except TimeoutError:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_on_timeout",
                attachment_type=allure.attachment_type.PNG
            )
            print("Предупреждение: Время ожидания загрузки страницы истекло. Продолжаем выполнение теста.")

    @allure.step("Кликнуть на элемент '{element_name}'")
    def click_element(self, element_name: str):
        xpath = LOCATORS.get(element_name)
        if xpath:
            self.page.locator(f'xpath={xpath}').click()
        else:
            raise ValueError(f"Элемент '{element_name}' не найден.")

    @allure.step("Заполнить элемент '{element_name}' значением '{value}'")
    def fill_element(self, element_name: str, value: str):
        xpath = LOCATORS.get(element_name)
        if xpath:
            self.page.locator(f'xpath={xpath}').fill(value)
        else:
            raise ValueError(f"Элемент '{element_name}' не найден.")