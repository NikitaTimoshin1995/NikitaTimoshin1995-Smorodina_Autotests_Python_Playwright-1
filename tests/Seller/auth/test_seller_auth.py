import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests  # Импортируем фикстуру
from data.assertions import Assertions  # Импортируем класс Assertions
from data.constants import (SELLER_LOGIN1, SELLER_PASSWORD1, EXPECTED_URL_AFTER_LOGIN_SELLER, SELLER_AUTH_ERROR1,
                            SELLER_AUTH_ERROR2, SELLER_AUTH_ERROR3, SELLER_AUTH_ERROR4, SELLER_AUTH_ERROR5, CLIENT_LOGIN1,
                            CLIENT_PASSWORD1, REFERENT_LOGIN1, REFERENT_PASSWORD1, SELLER_AUTH_ERROR6, SELLER_LOGIN1_REGISTR )# Импортируем константы
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
@allure.title('Ошибки. Логин и пароль пустые')
def test_seller_auth2(page: Page): 
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth("", "") 
    assertions.check_div_with_text(SELLER_AUTH_ERROR1)
    assertions.check_div_with_text(SELLER_AUTH_ERROR2)
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Логин'])
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Пароль'])  


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Такого логина нет') 
def test_seller_auth3(page:Page):
    assertions = Assertions(page)
    main_page = MainPage(page)
    main_page.seller_auth("НесуществующийЕмаил@.ru","")
    assertions.check_div_with_text(SELLER_AUTH_ERROR3)
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Логин'])


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Неверный пароль')
def test_seller_auth4(page: Page): 
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth(SELLER_LOGIN1, "123") 
    assertions.check_div_with_text(SELLER_AUTH_ERROR4) 


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Зарегистрирован как клиент.')
def test_seller_auth5(page: Page): 
    assertions = Assertions(page) 
    main_page = MainPage(page)  
    main_page.seller_auth(CLIENT_LOGIN1, CLIENT_PASSWORD1) 
    assertions.check_div_with_text(SELLER_AUTH_ERROR5) 


@allure.feature('Продавец') 
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Зарегистрирован как референт.')
def test_seller_auth6(page: Page): 
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth(REFERENT_LOGIN1, REFERENT_PASSWORD1) 
    assertions.check_div_with_text(SELLER_AUTH_ERROR6) 


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Успешный вход, когда логин в другом регистре')
def test_seller_auth7(page: Page, intercept_requests):  
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth(SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1) 
    assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER) 
    assertions.check_request_statuses(intercept_requests)


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Только пароль пустой')
def test_seller_auth8(page: Page): 
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth(SELLER_LOGIN1, "") 
    assertions.check_div_with_text(SELLER_AUTH_ERROR2)
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Пароль'])  


@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@allure.title('Ошибки. Только логин пустой')
def test_seller_auth9(page: Page): 
    assertions = Assertions(page)  
    main_page = MainPage(page)  
    main_page.seller_auth("", SELLER_PASSWORD1) 
    assertions.check_div_with_text(SELLER_AUTH_ERROR1)
    assertions.check_border_style_by_xpath(LOCATORS['границы поля Логин'])

    