import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
from data.constants import SELLER_LOGIN1, SELLER_PASSWORD1, EXPECTED_URL_AFTER_LOGIN_SELLER, SELLER_AUTH_ERROR1, SELLER_AUTH_ERROR2 # Импортируем константы
from pages.main_page import MainPage  # Импортируем MainPage
import allure
from Locators.locator_main_page import LOCATORS

@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Успешный вход')
def test_seller_auth1(page: Page, intercept_requests):  # Используем фикстуру
    assertions = Assertions(page)  # Создаем экземпляр Assertions
    main_page = MainPage(page)  # Создаем экземпляр MainPage
    main_page.seller_auth(SELLER_LOGIN1, SELLER_PASSWORD1) # Основной поток теста с использованием метода seller_auth
    assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER) # Проверяем конечный URL после логина
    # Проверяем, что все перехваченные запросы завершились успешно (код 200)
    assertions.check_request_statuses(intercept_requests)
   

@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки.Логин и пароль пустые')
def test_seller_auth2(page: Page, intercept_requests):  # Используем фикстуру
    assertions = Assertions(page)  # Создаем экземпляр Assertions
    main_page = MainPage(page)  # Создаем экземпляр MainPage
    main_page.seller_auth("", "") # Основной поток теста с использованием метода seller_auth
    assertions.check_div_with_text(SELLER_AUTH_ERROR1)
    assertions.check_div_with_text(SELLER_AUTH_ERROR2)
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Логин'])
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Пароль'])    

 