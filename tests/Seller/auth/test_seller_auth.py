import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
from data.constants import URL, SELLER_LOGIN1, SELLER_PASSWORD1, EXPECTED_URL_AFTER_LOGIN_SELLER  # Импортируем константы
from pages.main_page import MainPage  # Импортируем MainPage
import allure

@allure.feature('Клиент')
@allure.story('Авторизация клиента')
@allure.label('Успешный вход')
def test_auth1(page: Page, intercept_requests):  # Используем фикстуру
    assertions = Assertions(page)  # Создаем экземпляр Assertions
    main_page = MainPage(page)  # Создаем экземпляр MainPage

    # Основной поток теста с использованием метода seller_auth
    main_page.seller_auth(SELLER_LOGIN1, SELLER_PASSWORD1)

    # Проверяем конечный URL после логина
    assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)

    # Проверяем, что все перехваченные запросы завершились успешно (код 200)
    assertions.check_request_statuses(intercept_requests)
   