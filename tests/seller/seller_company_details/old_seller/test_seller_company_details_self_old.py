import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Assertions.seller.seller_company_details.seller_company_details_self.seller_company_details_self import AssertionsCompanyDetailsSelf
from pages.seller.seller_company_details.seller_company_details_self.seller_company_details_self import CompanyDetailsSelf
import allure

from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN3_COMPANYDETAILS,
    SELLER_PASSWORD1
)
from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    #Контактная информация общая
    SELLER_COMPANY_FACT_ADDRESS1,
    SELLER_COMPANY_PHONE1,
    SELLER_COMPANY_EMAIL1,
    SELLER_COMPANY_FACT_ADDRESS2,
    SELLER_COMPANY_PHONE2,
    SELLER_COMPANY_EMAIL2,
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
@allure.story('Существующий продавец. Данные компании продавца Самозанятый')
@pytest.mark.all
@pytest.mark.seller
@pytest.mark.company_details
@pytest.mark.debug

class TestSellerCompanyDetailsSelf:

    #Существующий продавец #########################################################################
    @allure.title('Успешное сохранение самозанятого в статус Проверен(STATE SELFACTIVE)')
    def test_seller_company_details_self1(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN1_TRUE,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    SELLER_COMPANY_SELF_STATE_ACTIVE
                                     )
        page.reload
        assertions.check_operator_self_active_fields()
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        
    @allure.title('Успешное сохранение самозанятого в статус Отклонен автомодерацией(STATE SELFINACTIVE)')
    def test_seller_company_details_self2(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN2_FALSE,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    SELLER_COMPANY_SELF_STATE_INACTIVE
                                    )
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
    
    @allure.title('Успешное сохранение самозанятого в статус Отклонен автомодерацией(STATE NULL Неизвестный статус)')
    def test_seller_company_details_self3(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    None
                                    )
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()

    @allure.title('Перевод в статус STATE NULL Неизвестный статус из SELFACTIVE')
    def test_seller_company_details_self4(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 2)
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
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()

    @allure.title('Перевод в статус STATE NULL Неизвестный статус из SELFINACTIVE')
    def test_seller_company_details_self5(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front(page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
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
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()

    @allure.title('Проверка, что кнопка Сохранить у Самозанятого активна только когда все поля заполнены')
    def test_seller_company_details_self6(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    '',
                                                    SELLER_COMPANY_EMAIL1)
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE1,
                                                    '')
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
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
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
                                    SELLER_COMPANY_SELF_INN3_NULL,
                                    SELLER_COMPANY_SELF_PATRONYMIC1,
                                    SELLER_COMPANY_SELF_NAME1,
                                    SELLER_COMPANY_SELF_LASTNAME1,
                                    SELLER_COMPANY_SELF_BILL1,
                                    SELLER_COMPANY_SELF_BIC1,
                                    SELLER_COMPANY_SELF_BANK1,
                                    SELLER_COMPANY_SELF_REFERENCE1,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    None
                                    )
        assertions.check_request_statuses(intercept_requests)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()

    @allure.title('Повторное сохранение данных самозанятого')
    def test_seller_company_details_self7(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsSelf(page)  
        company_details = CompanyDetailsSelf(page)
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################
        company_details.open_company_details_without_create(page,SELLER_LOGIN3_COMPANYDETAILS, SELLER_PASSWORD1)
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
                                                    SELLER_COMPANY_PHONE1,
                                                    SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 2)
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
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 13)
        assertions.check_self_in_db(db_connection, 
                                    SELLER_LOGIN3_COMPANYDETAILS,
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
        # Тут сохраняю данные как были после регистрации.
        company_details.update_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        assertions.check_operator_status(db_connection, SELLER_LOGIN3_COMPANYDETAILS, 0)
        company_details.patch_company_start()
        #########################################################################