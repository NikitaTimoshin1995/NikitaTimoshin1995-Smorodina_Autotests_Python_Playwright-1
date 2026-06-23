import pytest
from playwright.sync_api import Page
from entities.user.eni_user import UserAPI
from fixtures.all import intercept_requests, db_connection  
from Assertions.client.client_auth_and_registration.assert_client_auth_and_registration import AssertionsClientAuthRegistration
from Locators.loc_all_directories import ALL_LOCATORS
from pages.client.client_auth_and_registration import ClientAuthRegistration
import allure
from Constants.client.client_auth.const_client_auth import (
    CLIENT_PHONE1,
    CLIENT_PHONE2,
    EXPECTED_URL_AFTER_LOGIN_CLIENT,
    EXPECTED_URL_AFTER_A_PERSONAL_DATA,
    EXPECTED_URL_AFTER_A_DATA_POLICY,
    EXPECTED_URL_AFTER_A_AGREEMENT,
    C_CLIENT_ERROR1,
    C_CLIENT_CONFIRM_ERROR1,
    C_CLIENT_STATUS_ACTIVE,
    C_CLIENT_CONSENT

)

@allure.feature('Клиент')
@allure.story('Авторизация клиента')
@pytest.mark.all
@pytest.mark.client
class TestClientAuthAndRegistration:


#     #Вход Альфа(недоступна на дев)
#     #Вход VK
#     #Вход по почте и паролю, когда их добавил
#     #Повторная отправка смс
#     #Если номер автозаполнен
#     #Возможно тесты на текст, и закрытие на х или любое место экрана

    @allure.title('Успешная регистрация')
    def test_client_auth1(self, page: Page, intercept_requests, db_connection):  
        assertions = AssertionsClientAuthRegistration(page) 
        clientauth = ClientAuthRegistration(page) 
        user = UserAPI()
        user.delete_user_by_phone(db_connection, CLIENT_PHONE2)
        clientauth.client_auth(db_connection, CLIENT_PHONE2)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_CLIENT)
        clientauth.click_element('кнопка Профиль у клиента')
        assertions.check_request_statuses(intercept_requests)
        assertions.check_user_by_phone_in_db(db_connection, CLIENT_PHONE2, C_CLIENT_STATUS_ACTIVE, C_CLIENT_CONSENT)
        assertions.check_user_roles_in_db(db_connection, CLIENT_PHONE2, traveller=1, operator=0, poster_author=0, media_author=0, admin=0,
                                           operator_employee=0, partner=0, referral=0)
        user.delete_user_by_phone(db_connection, CLIENT_PHONE2)

    @allure.title('Кнопка Продолжить неактивна, если номер неполный')
    def test_client_auth2(self, page: Page):  
        assertions = AssertionsClientAuthRegistration(page) 
        clientauth = ClientAuthRegistration(page) 
        clientauth.client_go_to_auth()
        clientauth.client_fill_phone('+')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+7')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+79')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+799')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+7999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+79999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+799999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+7999999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+79999999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+799999999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+7999999999')
        assertions.check_client_auth_button_inactive()
        clientauth.client_fill_phone('+79999999998')
        assertions.check_client_auth_button_active()

    # #Работает только локально
    # @allure.title('Переход по ссылке Политикой обработки данных')
    # def test_client_auth3(self, page: Page):  
    #     assertions = AssertionsClientAuthRegistration(page) 
    #     clientauth = ClientAuthRegistration(page) 
    #     clientauth.client_go_to_auth()
    #     new_tab = clientauth.client_click_a_data_policy()  
    #     assertions.page = new_tab  
    #     assertions.check_url(EXPECTED_URL_AFTER_A_DATA_POLICY)

    # # Работает только локально
    # @allure.title('Переход по ссылке Пользовательское соглашение в авторизации клиента')
    # def test_client_auth4(self, page: Page):  
    #     assertions = AssertionsClientAuthRegistration(page) 
    #     clientauth = ClientAuthRegistration(page) 
    #     clientauth.client_go_to_auth()
    #     new_tab = clientauth.client_click_a_agreement()  
    #     assertions.page = new_tab  
    #     assertions.check_url(EXPECTED_URL_AFTER_A_AGREEMENT)

    # # Работает только локально
    # @allure.title('Переход по ссылке обработки персональных данных')
    # def test_client_auth5(self, page: Page):  
    #     assertions = AssertionsClientAuthRegistration(page) 
    #     clientauth = ClientAuthRegistration(page) 
    #     clientauth.client_go_to_auth()
    #     new_tab = clientauth.client_click_a_personal_data()  
    #     assertions.page = new_tab  
    #     assertions.check_url(EXPECTED_URL_AFTER_A_PERSONAL_DATA)

    @allure.title('Ошибка. Неправильный код')
    def test_client_auth6(self, page: Page, db_connection): 
        assertions = AssertionsClientAuthRegistration(page) 
        clientauth = ClientAuthRegistration(page)   
        clientauth.client_auth_short(db_connection, CLIENT_PHONE1)
        clientauth.client_enter_sms_code('1','1','1','1')
        assertions.check_field_value_from_locator('Ошибка в Введите код из смс', C_CLIENT_CONFIRM_ERROR1)

    # @allure.title('Вход по VK ID')
    # def test_client_auth5(self, page: Page):  
    #     assertions = AssertionsClientAuthRegistration(page) 
    #     clientauth = ClientAuthRegistration(page) 11
    #     clientauth.client_go_to_auth()
