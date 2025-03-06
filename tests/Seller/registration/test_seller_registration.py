import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests, db_connection  
from data.assertions import Assertions
from pages.main_page import MainPage
import allure
from Locators.locator_main_page import LOCATORS
from data.constants import (SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR,
                            SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, SELLER_REGISTRATION_EMAIL1,
                            EXPECTED_URL_AFTER_LOGIN_SELLER,  SELLER_REGISTRATION_PHONE2, SELLER_REGISTRATION_ERROR1,
                            SELLER_REGISTRATION_EMAIL2_REGISTR, SELLER_REGISTRATION_ERROR2, SELLER_REGISTRATION_EMAIL3,
                            SELLER_REGISTRATION_ERROR3, SELLER_REGISTRATION_ERROR4, SELLER_REGISTRATION_ERROR5,
                            SELLER_REGISTRATION_ERROR6, SELLER_REGISTRATION_ERROR7  )
import time
                            


# @allure.feature('Продавец') 
# @allure.story('Регистрация продавца')
# @allure.title('Успешная регистрация')
# def test_seller_registration1(page:Page,intercept_requests, db_connection):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1, SELLER_REGISTRATION_NAME_COMPANY1)
#     main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR,
#                                    SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
#     assertions.check_user_in_db(db_connection, SELLER_REGISTRATION_EMAIL1, None, 2, 1)
#     main_page.seller_confirm_phone(db_connection, SELLER_REGISTRATION_PHONE1)
#     assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
#     assertions.check_request_statuses(intercept_requests)
#     # Удаление пользователя и связанных данных из базы данных
#     main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1, SELLER_REGISTRATION_NAME_COMPANY1)


# @allure.feature('Продавец')
# @allure.story('Регистрация продавца')
# @allure.title('Ошибки.Такое значение поля номер телефона уже существует')
# def test_seller_registration2(page:Page):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE2, SELLER_REGISTRATION_EMAIL1_REGISTR,
#                                    SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR1)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 


# @allure.feature('Продавец')
# @allure.story('Регистрация продавца')
# @allure.title('Ошибки. Номер телефона введен не полностью')
# def test_seller_registration3(page:Page):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, '7123456789', SELLER_REGISTRATION_EMAIL1_REGISTR,
#                                    SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '712345678')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '71234567')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '7123456')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '712345')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '71234')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '7123')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '712')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 
#     main_page.fill_element('поле Номер телефона', '71')
#     main_page.click_element('кнопка Зарегистрироваться') 
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля телефон в регистрации']) 


# @allure.feature('Продавец')
# @allure.story('Регистрация продавца')
# @allure.title('Ошибки.Такое значение поля email уже существует')
# def test_seller_registration4(page:Page):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL2_REGISTR,
#                                    SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR2)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля email в регистрации']) 


# @allure.feature('Продавец')
# @allure.story('Регистрация продавца')
# @allure.title('Ошибки.Емаил без @')
# def test_seller_registration5(page:Page):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL3,
#                                    SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR3)
#     assertions.check_border_style_by_xpath(LOCATORS['границы поля email в регистрации']) 


# @allure.feature('Продавец')
# @allure.story('Регистрация продавца')
# @allure.title('Ошибки. Неправильный пароль')
# def test_seller_registration6(page:Page):
#     assertions = Assertions(page)
#     main_page = MainPage(page)
#     main_page.seller_registration_only_fill(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR,
#                                    '123', '12', True, True, True)
#     assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR7)
#     main_page.seller_registration_fill_passwords('123', '123')
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR5)
#     assertions.check_border_style_by_xpath(LOCATORS['границы придумайте пароль в регистрации продавца'])
#     main_page.seller_registration_fill_passwords('123456', '123456')
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR6)
#     assertions.check_border_style_by_xpath(LOCATORS['границы придумайте пароль в регистрации продавца'])
#     main_page.seller_registration_fill_passwords('nik123', 'nik123')
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR6)
#     assertions.check_border_style_by_xpath(LOCATORS['границы придумайте пароль в регистрации продавца'])
#     main_page.seller_registration_fill_passwords('NIK123', 'NIK123')
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR6)
#     assertions.check_border_style_by_xpath(LOCATORS['границы придумайте пароль в регистрации продавца'])
#     main_page.seller_registration_fill_passwords('Nikita', 'Nikita')
#     assertions.check_div_with_text(SELLER_REGISTRATION_ERROR6)
#     assertions.check_border_style_by_xpath(LOCATORS['границы придумайте пароль в регистрации продавца'])


@allure.feature('Продавец')
@allure.story('Регистрация продавца')
@allure.title('Кнопка зарегистрироваться неактивна, если не отмечены два нужных чекбокса')
def test_seller_registration6(page:Page):
    assertions = Assertions(page)
    main_page = MainPage(page)
    main_page.seller_registration_only_fill(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR,
                                   '123', '123', False, False, False)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(False, False, True)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(False, False, True)
    main_page.handle_agreements(True, False, True)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(True, False, True)
    main_page.handle_agreements(True, False, False)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(True, False, False)
    main_page.handle_agreements(False, True, False)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(False, True, False)
    main_page.handle_agreements(False, False, False)
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(False, True, True )
    assertions.check_element_disabled_by_xpath(LOCATORS['кнопка Зарегистрироваться']) 
    main_page.handle_agreements(False, True, True )
    main_page.handle_agreements(True, True, True )
    assertions.check_element_enabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])
    main_page.handle_agreements(True, True, True )
    main_page.handle_agreements(True, True, False )
    assertions.check_element_enabled_by_xpath(LOCATORS['кнопка Зарегистрироваться'])