import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
import allure

# Переменные
url = 'https://dev.smorodina.ru/'
partner_login1 = 'nikitatimoshinpost@gmail.com'
partner_password1 = 'Nik123'

# 1. УСПЕШНЫЙ ВХОД
@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.label('Успешный вход')
def test_auth1(page: Page, intercept_requests):  # Используем фикстуру
    assertions = Assertions(page)  # Создаем экземпляр Assertions
    # Основной поток теста
    with allure.step('Открыть главную'):
        page.goto(url)
    with allure.step('Нажать "Искать туры"'):
        page.get_by_role('button', name='Искать туры').click()
    with allure.step('Нажать "Войти"'):
        page.get_by_role('button', name='Войти').click()
    with allure.step('Нажать "Организатор туров"'):
        page.locator('//h4[text()="Организатор туров"]').click()
    with allure.step('Ввести емаил'):
        page.fill('input[placeholder="email"]', partner_login1)
    with allure.step('Ввести пароль'):
        page.fill('input[placeholder="пароль"]', partner_password1)
    with allure.step('Нажать "Войти"'):
        page.click('button[type="submit"]')
    with allure.step('Проверка url'):
        expect(page).to_have_url('https://dev.smorodina.ru/partner/summary')
    # Проверка статусов запросов после выполнения всех действий с использованием класса Assertions
    with allure.step('Проверка, что все запросы с кодом 200'):
        assertions.assert_request_statuses(intercept_requests)  # Проверяем, что все статусы 200