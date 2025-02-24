import pytest
import allure
from fixtures.all import intercept_requests
from data.constants import SELLER_LOGIN, SELLER_PASSWORD, URL, EXPECTED_URL_AFTER_LOGIN 
from pages.main_page import MainPage
from data.assertions import Assertions
from data.constants import EXPECTED_URL_AFTER_LOGIN, URL

@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.label('Успешный вход')
def test_auth1(page, intercept_requests):
    assertions = Assertions(page)
    main_page = MainPage(page)  # Создаем экземпляр класса MainPage

    # Вызов методов, которые уже содержат Allure-декораторы
    main_page.goto(URL)  # Переход на главную страницу
    main_page.click_search_tours()  # Нажимаем на кнопку "Искать туры"
    main_page.click_login()  # Нажимаем на кнопку "Войти"
    main_page.click_tour_organizer()  # Нажимаем на "Организатор туров"
    main_page.fill_email(SELLER_LOGIN)  # Заполняем email
    main_page.fill_password(SELLER_PASSWORD)  # Заполняем пароль
    main_page.submit_login()  # Нажимаем кнопку "Войти"

    # Проверяем конечный URL после логина
    assert main_page.check_url(EXPECTED_URL_AFTER_LOGIN), "URL не совпадает"

    # Проверка, что все запросы с кодом 200
    assertions.assert_request_statuses(intercept_requests)