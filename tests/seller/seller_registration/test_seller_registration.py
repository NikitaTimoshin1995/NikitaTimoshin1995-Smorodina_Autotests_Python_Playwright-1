import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Assertions.assertions import Assertions
from pages.seller.seller_auth_and_registration import SellerAuthRegistration
import allure
from Locators.loc_all_directories import ALL_LOCATORS
from Constants.seller.seller_auth.const_seller_auth import EXPECTED_URL_AFTER_LOGIN_SELLER
from Constants.seller.seller_registration.const_seller_registration import (
    SELLER_REGISTRATION_NAME_COMPANY1, 
    SELLER_REGISTRATION_PHONE1, 
    SELLER_REGISTRATION_EMAIL1,
    SELLER_REGISTRATION_EMAIL1_REGISTR, 
    SELLER_REGISTRATION_EMAIL2_REGISTR,
    SELLER_REGISTRATION_PASSWORD1, 
    SELLER_REGISTRATION_REPEAT_PASSWORD1, 
    SELLER_REGISTRATION_ERROR1, 
    SELLER_REGISTRATION_ERROR2,
    SELLER_REGISTRATION_ERROR3, 
    SELLER_REGISTRATION_ERROR4, 
    SELLER_REGISTRATION_ERROR5, 
    SELLER_REGISTRATION_ERROR6, 
    SELLER_REGISTRATION_ERROR7
)

# Добавить тест на переход по ссылке
# Нужно добавить тест на переход в регистрацию из других мест
# Добавить тест, неправильный пароль

@allure.feature('Продавец')
@allure.story('Регистрация продавца')
@pytest.mark.all
@pytest.mark.seller
@pytest.mark.debug

class TestSellerRegistration:

# Нужно проверять номер и удалять, если есть
    @allure.title('Успешная регистрация')
    def test_seller_registration1(self, page: Page, intercept_requests, db_connection):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True, True
        )
        assertions.check_user_in_db(db_connection, SELLER_REGISTRATION_EMAIL1, None, 2, 1)
        main_page.seller_confirm_phone(db_connection, SELLER_REGISTRATION_PHONE1)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        assertions.check_request_statuses(intercept_requests)
        # Удаление пользователя и связанных данных из базы данных
        main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1)

    @allure.title('Ошибки. Такое значение поля номер телефона уже существует')
    def test_seller_registration2(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            '71234567891', 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True
        )
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR1)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля телефон в регистрации'])
    
    @allure.title('Ошибки. Номер телефона введен не полностью')
    def test_seller_registration3(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            '7123456789', 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True
        )
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR4)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля телефон в регистрации'])
    
    @allure.title('Ошибки. Такое значение поля email уже существует')
    def test_seller_registration4(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            SELLER_REGISTRATION_EMAIL2_REGISTR,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True
        )
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR2)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля email в регистрации']) 
    
    @allure.title('Ошибки. Емаил без @')
    def test_seller_registration5(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            'invalid_email', 
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True
        )
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR3)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля email в регистрации']) 

    @allure.title('Ошибки. Неправильный пароль')
    def test_seller_registration6(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration_only_fill(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            '123', '12', True, True, True, True
        )
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR7)
        main_page.seller_registration_fill_passwords('123', '123')
        assertions.check_div_with_text(SELLER_REGISTRATION_ERROR5)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы придумайте пароль в регистрации продавца'])
        # Проверка других некорректных паролей
        invalid_passwords = ['123456', 'nik123', 'NIK123', 'Nikita']
        for password in invalid_passwords:
            main_page.seller_registration_fill_passwords(password, password)
            assertions.check_div_with_text(SELLER_REGISTRATION_ERROR6)
            assertions.check_border_style_by_xpath(ALL_LOCATORS['границы придумайте пароль в регистрации продавца'])

    @allure.title('Кнопка зарегистрироваться неактивна, если не отмечены два нужных чекбокса')
    def test_seller_registration7(self, page: Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_registration_only_fill(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            '123', '123', False, False, False, False
        )
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        # Проверка состояния кнопки при изменении чекбоксов
        main_page.handle_agreements(False, False, False, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, False, False, True)
        main_page.handle_agreements(False, False, False, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, False, False, True)
        main_page.handle_agreements(False, False, True, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, False, True, False)
        main_page.handle_agreements(False, False, True, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, False, True, True)
        main_page.handle_agreements(False, True, False, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, True, False, False)   
        main_page.handle_agreements(False, True, False, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, True, False, True)        
        main_page.handle_agreements(False, True, True, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, True, True, False)     
        main_page.handle_agreements(False, True, True, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(False, True, True, True)    
        main_page.handle_agreements(True, False, False, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, False, False, False)    
        main_page.handle_agreements(True, False, False, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, False, False, True)  
        main_page.handle_agreements(True, False, True, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, False, True, False)
        main_page.handle_agreements(True, False, True, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, False, True, True) 
        main_page.handle_agreements(True, True, False, False)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, True, False, False)
        main_page.handle_agreements(True, True, False, True)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, True, False, True)
        main_page.handle_agreements(True, True, True, False)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])
        main_page.handle_agreements(True, True, True, False)
        main_page.handle_agreements(True, True, True, True)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['кнопка Зарегистрироваться'])

    @allure.title('Регистрация>Выход>Вход')
    def test_seller_registration8(self, page: Page, intercept_requests, db_connection):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1)
        main_page.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY1, 
            SELLER_REGISTRATION_PHONE1, 
            SELLER_REGISTRATION_EMAIL1_REGISTR,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True, True
        )
        assertions.check_user_in_db(db_connection, SELLER_REGISTRATION_EMAIL1, None, 2, 1)
        main_page.seller_confirm_phone(db_connection, SELLER_REGISTRATION_PHONE1)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        main_page.click_element('кнопка Профиль в меню продавца')
        main_page.click_element('кнопка Редактировать в меню продавца') 
        main_page.click_element('кнопка Выйти из аккаунта в профиле продавца')
        page.wait_for_timeout(500)
        main_page.seller_auth(SELLER_REGISTRATION_EMAIL1_REGISTR, SELLER_REGISTRATION_PASSWORD1)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        # Удаление пользователя и связанных данных из базы данных
        main_page.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL1)