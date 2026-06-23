import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Assertions.seller.seller_company_details.seller_company_details_self.seller_company_details_self import AssertionsCompanyDetailsSelf
from pages.seller.seller_company_details.seller_company_details_self.seller_company_details_self import CompanyDetailsSelf
import allure

from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    #Контактная информация общая
    SELLER_COMPANY_FACT_ADDRESS1,
    SELLER_COMPANY_PHONE1,
    SELLER_COMPANY_EMAIL1,
    SELLER_COMPANY_FACT_ADDRESS2,
    SELLER_COMPANY_PHONE2,
    SELLER_COMPANY_EMAIL2,
    SELLER_COMPANY_PHONE3,
    SELLER_COMPANY_EMAIL3_NEW,
    #Самозанятый
    SELLER_COMPANY_SELF_INN1_TRUE,
    SELLER_COMPANY_SELF_INN1_NOT_FULL,
    SELLER_COMPANY_SELF_INN2_FALSE,
    SELLER_COMPANY_SELF_INN3_NULL,
    SELLER_COMPANY_SELF_LASTNAME1,
    SELLER_COMPANY_SELF_LASTNAME2,
    SELLER_COMPANY_SELF_NAME1,
    SELLER_COMPANY_SELF_NAME2,
    SELLER_COMPANY_SELF_PATRONYMIC1,
    SELLER_COMPANY_SELF_PATRONYMIC2,
    SELLER_COMPANY_SELF_BILL1,
    SELLER_COMPANY_SELF_BILL2,
    SELLER_COMPANY_SELF_BIC1,
    SELLER_COMPANY_SELF_BIC2,
    SELLER_COMPANY_SELF_BANK1,
    SELLER_COMPANY_SELF_BANK2,
    SELLER_COMPANY_SELF_REFERENCE1,
    SELLER_COMPANY_SELF_REFERENCE2,
    SELLER_COMPANY_SELF_STATE_ACTIVE,
    SELLER_COMPANY_SELF_STATE_INACTIVE
)

# Новые валидации на количество цифр

@allure.feature('Продавец')
@allure.story('Данные компании продавца Самозанятый. Новый продавец.')
@pytest.mark.all
@pytest.mark.seller
@pytest.mark.company_details
@pytest.mark.debug


class TestSellerCompanyDetailsSelf:

    #Новый продавец #########################################################################
    @allure.title('Новый продавец. Успешное сохранение самозанятого в статус Проверен(STATE SELFACTIVE)')
    def test_seller_company_details_self_new1(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN1_NOT_FULL)
        assertions.check_operator_self_inactive_fields()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN1_TRUE)
        assertions.check_operator_self_state_front(page, 'Зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN1_TRUE,
                                                  SELLER_COMPANY_SELF_LASTNAME1,
                                                  SELLER_COMPANY_SELF_NAME1,
                                                  SELLER_COMPANY_SELF_PATRONYMIC1,
                                                  SELLER_COMPANY_SELF_BILL1,
                                                  SELLER_COMPANY_SELF_BIC1,
                                                  SELLER_COMPANY_SELF_BANK1,
                                                  SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN1_TRUE,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_STATE_ACTIVE
                                     )
        page.reload
        assertions.check_operator_self_active_fields()
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)
        
    @allure.title('Новый продавец. Успешное сохранение самозанятого в статус Отклонен автомодерацией(STATE SELFINACTIVE)')
    def test_seller_company_details_self_new2(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN2_FALSE)
        assertions.check_operator_self_state_front(page, 'Не зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN2_FALSE,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN2_FALSE,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_STATE_INACTIVE
                                    )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)
    
    @allure.title('Новый продавец. Успешное сохранение самозанятого в статус Отклонен автомодерацией(STATE NULL Неизвестный статус)')
    def test_seller_company_details_self_new3(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN3_NULL)
        # assertions.check_operator_self_state_front(page, 'Неизвестный статус')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    None
                                    )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Перевод в статус STATE NULL Неизвестный статус из SELFACTIVE')
    def test_seller_company_details_self_new4(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN1_TRUE)
        assertions.check_operator_self_state_front(page, 'Зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN1_TRUE,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.check_operator_self_state_hidden(page)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_self_state_front(page, 'Неизвестный статус')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Перевод в статус STATE NULL Неизвестный статус из SELFINACTIVE')
    def test_seller_company_details_self_new5(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN2_FALSE)
        assertions.check_operator_self_state_front(page, 'Не зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN2_FALSE,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                   SELLER_COMPANY_PHONE3,
                                                   SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.check_operator_self_state_hidden(page)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_self_state_front(page, 'Неизвестный статус')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Проверка, что кнопка Сохранить у Самозанятого активна только когда все поля заполнены')
    def test_seller_company_details_self_new6(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN1_TRUE)
        assertions.check_operator_self_state_front(page, 'Зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts('',
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    '',
                                                    SELLER_COMPANY_EMAIL3_NEW)
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    '')
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        company_details.fill_company_details_self('',
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()         
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                '',
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()   
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                '',
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()               
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                '',
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()               
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                '',
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()               
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                '',
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()               
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                '',
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_inactive()              
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                '' )
        assertions.check_operator_company_button_inactive()               
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        assertions.check_operator_company_button_active() 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Повторное сохранение данных самозанятого')
    def test_seller_company_details_self_new7(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_self()
        assertions.check_operator_self_inactive_fields()
        assertions.check_operator_company_button_inactive ()
        company_details.company_details_choice_fill_inn_self(SELLER_COMPANY_SELF_INN1_TRUE)
        assertions.check_operator_self_state_front(page, 'Зарегистрирован как самозанятый')
        assertions.check_operator_self_active_fields()
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN1_TRUE,
                                                SELLER_COMPANY_SELF_LASTNAME1,
                                                SELLER_COMPANY_SELF_NAME1,
                                                SELLER_COMPANY_SELF_PATRONYMIC1,
                                                SELLER_COMPANY_SELF_BILL1,
                                                SELLER_COMPANY_SELF_BIC1,
                                                SELLER_COMPANY_SELF_BANK1,
                                                SELLER_COMPANY_SELF_REFERENCE1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE3,
                                                    SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_self_in_db(db_connection, 
                            SELLER_COMPANY_EMAIL3_NEW,
                            SELLER_COMPANY_SELF_INN1_TRUE,
                            SELLER_COMPANY_SELF_PATRONYMIC1,
                            SELLER_COMPANY_SELF_NAME1,
                            SELLER_COMPANY_SELF_LASTNAME1,
                            SELLER_COMPANY_SELF_BILL1,
                            SELLER_COMPANY_SELF_BIC1,
                            SELLER_COMPANY_SELF_BANK1,
                            SELLER_COMPANY_SELF_REFERENCE1,
                            SELLER_COMPANY_FACT_ADDRESS1,
                            SELLER_COMPANY_PHONE3,
                            SELLER_COMPANY_EMAIL3_NEW,
                            SELLER_COMPANY_SELF_STATE_ACTIVE
                            )
        company_details.fill_company_details_self(SELLER_COMPANY_SELF_INN3_NULL,
                                                SELLER_COMPANY_SELF_LASTNAME2,
                                                SELLER_COMPANY_SELF_NAME2,
                                                SELLER_COMPANY_SELF_PATRONYMIC2,
                                                SELLER_COMPANY_SELF_BILL2,
                                                SELLER_COMPANY_SELF_BIC2,
                                                SELLER_COMPANY_SELF_BANK2,
                                                SELLER_COMPANY_SELF_REFERENCE2 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS2,
                                                    SELLER_COMPANY_PHONE2,
                                                    SELLER_COMPANY_EMAIL2)
        company_details.check_operator_self_state_hidden(page)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_self_state_front(page, 'Неизвестный статус')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC2,
                                    SELLER_COMPANY_SELF_NAME2,
                                    SELLER_COMPANY_SELF_LASTNAME2,
                                    SELLER_COMPANY_SELF_BILL2,
                                    SELLER_COMPANY_SELF_BIC2,
                                    SELLER_COMPANY_SELF_BANK2,
                                    SELLER_COMPANY_SELF_REFERENCE2,
                                    SELLER_COMPANY_FACT_ADDRESS2,
                                    SELLER_COMPANY_PHONE2,
                                    SELLER_COMPANY_EMAIL2,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)