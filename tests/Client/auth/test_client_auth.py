import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
from data.constants import URL, SELLER_LOGIN1, SELLER_PASSWORD1, EXPECTED_URL_AFTER_LOGIN_SELLER  # Импортируем константы
import allure

# 1. УСПЕШНЫЙ ВХОД
@allure.feature('Клиент')
@allure.story('Авторизация клиента')
@allure.label('Успешный вход')
def test_auth1(page: Page, intercept_requests):  # Используем фикстуру
    
    assertions = Assertions(page) 
    
    # Основной поток теста
    with allure.step('Открыть главную'):
        page.goto(URL)
    with allure.step('Нажать "Искать туры"'):
        page.get_by_role('button', name='Искать туры').click()
    with allure.step('Нажать "Войти"'):
        page.get_by_role('button', name='Войти').click()
    with allure.step('Нажать "Организатор туров"'):
        page.locator('//h4[text()="Организатор туров"]').click()
    with allure.step('Ввести email'):
        page.fill('input[placeholder="email"]', SELLER_LOGIN1)
    with allure.step('Ввести пароль'):
        page.fill('input[placeholder="пароль"]', SELLER_PASSWORD1)
    with allure.step('Нажать "Войти"'):
        page.click('button[type="submit"]')

    # Проверяем конечный URL после логина
    with allure.step('Проверка url'):
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
