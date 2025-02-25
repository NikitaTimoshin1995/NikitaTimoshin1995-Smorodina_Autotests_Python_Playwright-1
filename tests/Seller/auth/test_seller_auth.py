# tests/Seller/auth/test_seller_auth.py
import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
from data.constants import URL, SELLER_LOGIN1, SELLER_PASSWORD1, EXPECTED_URL_AFTER_LOGIN  # Импортируем константы
from pages.main_page import MainPage  # Импортируем MainPage
import allure

@allure.feature('Клиент')
@allure.story('Авторизация клиента')
@allure.label('Успешный вход')
def test_auth1(page: Page, intercept_requests):  # Используем фикстуру
    assertions = Assertions(page)  # Создаем экземпляр Assertions
    main_page = MainPage(page)  # Создаем экземпляр MainPage

    # Основной поток теста с использованием методов из MainPage
    with allure.step('Открыть главную страницу'):
        main_page.open(URL)
    main_page.click_search_tours()
    main_page.click_login()
    main_page.click_tour_organizer()
    main_page.fill_email(SELLER_LOGIN1)
    main_page.fill_password(SELLER_PASSWORD1)
    main_page.submit_login()

    # Проверяем конечный URL после логина
    with allure.step('Проверка URL после входа'):
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN)
   