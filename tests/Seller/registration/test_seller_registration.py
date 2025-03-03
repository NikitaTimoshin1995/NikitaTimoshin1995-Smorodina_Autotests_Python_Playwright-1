import pytest
from playwright.sync_api import Page, expect
from fixtures.all import intercept_requests, db_connection  
from data.assertions import Assertions
from pages.main_page import MainPage
import allure
from Locators.locator_main_page import LOCATORS
from data.constants import SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR, SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, SELLER_REGISTRATION_EMAIL1, EXPECTED_URL_AFTER_LOGIN_SELLER 
                            


@allure.feature('Продавец') 
@allure.story('Регистрация продавца')
@allure.title('Успешная регистрация')
def test_seller_registration(page:Page,intercept_requests, db_connection):
    assertions = Assertions(page)
    main_page = MainPage(page)
    main_page.seller_registration(SELLER_REGISTRATION_NAME_COMPANY1, SELLER_REGISTRATION_PHONE1, SELLER_REGISTRATION_EMAIL1_REGISTR, SELLER_REGISTRATION_PASSWORD1, SELLER_REGISTRATION_REPEAT_PASSWORD1, True, True, True)
    assertions.check_user_in_db(db_connection, SELLER_REGISTRATION_EMAIL1, None, 2, 1)
    main_page.seller_confirm_phone(db_connection, SELLER_REGISTRATION_PHONE1)
    assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
    assertions.check_request_statuses(intercept_requests)