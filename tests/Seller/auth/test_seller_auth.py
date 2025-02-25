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
    main_page.open_page(URL)  # Открываем главную страницу
    main_page.click_search_tours()  # Нажимаем "Искать туры"
    main_page.click_login()  # Нажимаем "Войти"
    main_page.click_tour_organizer()  # Нажимаем "Организатор туров"
    main_page.fill_email(SELLER_LOGIN1)  # Заполняем email
    main_page.fill_password(SELLER_PASSWORD1)  # Заполняем пароль
    main_page.submit_login()  # Отправляем форму входа

    # Ожидаем полной загрузки страницы после авторизации
    main_page.wait_for_full_load()

    # Проверяем конечный URL после логина
    assertions.check_url(EXPECTED_URL_AFTER_LOGIN)

    # Проверяем, что все перехваченные запросы завершились успешно (код 200)
    assertions.check_request_statuses(intercept_requests)
   