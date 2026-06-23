import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests 
from Assertions.assertions import Assertions  
from pages.seller.seller_auth_and_registration import SellerAuthRegistration
import allure
from Locators.loc_all_directories import ALL_LOCATORS
from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN1, 
    SELLER_LOGIN2_DELETE,
    SELLER_PASSWORD1, 
    SELLER_PASSWORD2,
    EXPECTED_URL_AFTER_LOGIN_SELLER, 
    SELLER_AUTH_ERROR1,
    SELLER_AUTH_ERROR2, 
    SELLER_AUTH_ERROR3, 
    SELLER_AUTH_ERROR4, 
    SELLER_AUTH_ERROR5,
    SELLER_AUTH_ERROR6, 
    SELLER_AUTH_ERROR7,
    SELLER_LOGIN1_REGISTR 
)
from Constants.client.client_auth.const_client_auth import (CLIENT_LOGIN1, CLIENT_PASSWORD1)
from Constants.referent.referent_auth.const_referent_auth import (REFERENT_LOGIN1, REFERENT_PASSWORD1)

# ДОБАВИТЬ

# Добавить тесты успешной авторизации для разных статусов продавца (В том числе удаленный)
# Добавить тест с повторной авторизацией после регистрации
# Добавить проверку письма и уведомления после регистрации
# Ошибка при входе за администратора

@allure.feature('Продавец')
@allure.story('Авторизация продавца')
@pytest.mark.all
@pytest.mark.seller
class TestSellerAuth:
    
    @allure.title('Успешный вход')
    def test_seller_auth1(self, page: Page, intercept_requests):  
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)
        main_page.seller_auth(SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        assertions.check_request_statuses(intercept_requests)
    
    @allure.title('Ошибки. Логин и пароль пустые')
    def test_seller_auth2(self, page: Page): 
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth("", "") 
        assertions.check_div_with_text(SELLER_AUTH_ERROR1)
        assertions.check_div_with_text(SELLER_AUTH_ERROR2)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля Логин'])
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля Пароль'])  

    @allure.title('Ошибки. Такого логина нет') 
    def test_seller_auth3(self, page:Page):
        assertions = Assertions(page)
        main_page = SellerAuthRegistration(page)
        main_page.seller_auth("НесуществующийЕмаил@.ru","")
        assertions.check_div_with_text(SELLER_AUTH_ERROR3)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля Логин'])

    @allure.title('Ошибки. Неверный пароль')
    def test_seller_auth4(self, page: Page): 
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth(SELLER_LOGIN1, "123") 
        assertions.check_div_with_text(SELLER_AUTH_ERROR4) 

    @allure.title('Ошибки. Зарегистрирован как клиент.')
    def test_seller_auth5(self, page: Page): 
        assertions = Assertions(page) 
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth(CLIENT_LOGIN1, CLIENT_PASSWORD1) 
        assertions.check_div_with_text(SELLER_AUTH_ERROR5) 

    # Сейчас такой ошибки у нас нет
    # @allure.title('Ошибки. Зарегистрирован как референт.')
    # def test_seller_auth6(self, page: Page): 
    #     assertions = Assertions(page)  
    #     main_page = SellerAuthRegistration(page)  
    #     main_page.seller_auth(REFERENT_LOGIN1, REFERENT_PASSWORD1) 
    #     assertions.check_div_with_text(SELLER_AUTH_ERROR6) 

    @allure.title('Успешный вход, когда логин в другом регистре')
    def test_seller_auth7(self, page: Page, intercept_requests):  
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth(SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1) 
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER) 
        assertions.check_request_statuses(intercept_requests)

    @allure.title('Ошибки. Только пароль пустой')
    def test_seller_auth8(self, page: Page): 
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth(SELLER_LOGIN1, "") 
        assertions.check_div_with_text(SELLER_AUTH_ERROR2)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля Пароль'])  

    @allure.title('Ошибки. Только логин пустой')
    def test_seller_auth9(self, page: Page): 
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth("", SELLER_PASSWORD1) 
        assertions.check_div_with_text(SELLER_AUTH_ERROR1)
        assertions.check_border_style_by_xpath(ALL_LOCATORS['границы поля Логин'])
    
    @allure.title('Ошибки. Продавец удален')
    def test_seller_auth10(self, page: Page): 
        assertions = Assertions(page)  
        main_page = SellerAuthRegistration(page)  
        main_page.seller_auth(SELLER_LOGIN2_DELETE, SELLER_PASSWORD2) 
        assertions.check_div_with_text(SELLER_AUTH_ERROR7)
        