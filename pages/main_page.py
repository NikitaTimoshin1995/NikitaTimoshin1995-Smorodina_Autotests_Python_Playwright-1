import allure
from pages.base import BasePage
from Locators.locator_main_page import (
    BUTTON_ENTER,
    BUTTON_TOUR_SELLER,
    BUTTON_SEARCH_TOURS,
    INPUT_LOGIN_SELLER,
    INPUT_PASSWORD_SELLER,
    BUTTON_ENTER_SELLER
)
from data.constants import URL

class MainPage(BasePage):
    @allure.step("Авторизация продавца")
    def seller_auth(self, login: str, password: str):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element_by_xpath(BUTTON_SEARCH_TOURS)  # Нажимаем "Искать туры"
        self.click_element_by_xpath(BUTTON_ENTER)  # Нажимаем "Войти"
        self.click_element_by_xpath(BUTTON_TOUR_SELLER)  # Нажимаем "Организатор туров"
        self.fill_element_by_xpath(INPUT_LOGIN_SELLER, login)  # Заполняем email
        self.fill_element_by_xpath(INPUT_PASSWORD_SELLER, password)  # Заполняем пароль
        self.click_element_by_xpath(BUTTON_ENTER_SELLER)  # Отправляем форму входа
        self.wait_for_full_load()  # Ожидаем полной загрузки страницы