import allure
from pages.base import BasePage
from data.constants import URL

class MainPage(BasePage):
    @allure.step("Авторизация продавца")
    def seller_auth(self, login: str, password: str):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element('кнопка Искать туры')  # Нажимаем "Искать туры"
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.fill_element('поле Логин', login)  # Заполняем email
        self.fill_element('поле Пароль', password)  # Заполняем пароль
        self.click_element('кнопка Вход в авторизации продавца')  # Отправляем форму входа
        self.wait_for_full_load()  # Ожидаем полной загрузки страницы