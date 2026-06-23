import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Assertions.seller.seller_company_details.seller_company_details_ip.seller_company_details_ip import AssertionsCompanyDetailsIp
from pages.seller.seller_company_details.seller_company_details_ip.seller_company_details_ip import CompanyDetailsIp
import allure

from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    #Контактная информация общая
    SELLER_COMPANY_FACT_ADDRESS1,
    SELLER_COMPANY_FACT_ADDRESS2,
    SELLER_COMPANY_PHONE2,
    SELLER_COMPANY_EMAIL2,
    SELLER_COMPANY_PHONE3,
    SELLER_COMPANY_EMAIL3_NEW,
    #ИП
    SELLER_COMPANY_IP_INN1_TRUE,
    SELLER_COMPANY_IP_INN1_NOT_FULL,
    SELLER_COMPANY_IP_INN2_FALSE,
    SELLER_COMPANY_IP_INN3_NULL,
    SELLER_COMPANY_IP_FULLNAME1,
    SELLER_COMPANY_IP_FULLNAME2,
    SELLER_COMPANY_IP_OGRN1,
    SELLER_COMPANY_IP_OGRN2,
    SELLER_COMPANY_IP_BILL1,
    SELLER_COMPANY_IP_BILL2,
    SELLER_COMPANY_IP_BIC1,
    SELLER_COMPANY_IP_BIC2,
    SELLER_COMPANY_IP_BANK1,
    SELLER_COMPANY_IP_BANK2,
    SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
    SELLER_COMPANY_LEGAL_OR_IP_STATE_LIQUIDATED
)

#Можно добавить тесты на переход из разных state, как у самозанятого
# Новые валидации на количество цифр

@allure.feature('Продавец')
@allure.story('Данные компании продавца ИП. Новый продавец.')
@pytest.mark.all
@pytest.mark.seller
@pytest.mark.company_details
@pytest.mark.debug

class TestSellerCompanyDetailsIp:

    # #Новый продавец #########################################################################
    @allure.title('Новый продавец. Успешное сохранение ИП в статус Проверен(STATE ACTIVE)')
    def test_seller_company_details_ip_new1(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details =CompanyDetailsIp(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN1_NOT_FULL)
        assertions.check_operator_ip_inactive_fields(1)
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN1_TRUE)
        assertions.check_operator_ip_state_front(page, 'действующая')
        assertions.check_operator_ip_active_fields(1)
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN1_TRUE,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                1,
                                                1
                                                  )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  SELLER_COMPANY_IP_INN1_TRUE,
                                  SELLER_COMPANY_IP_FULLNAME1,
                                  SELLER_COMPANY_IP_OGRN1,
                                  SELLER_COMPANY_IP_BILL1,
                                  SELLER_COMPANY_IP_BIC1,
                                  SELLER_COMPANY_IP_BANK1,
                                  SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
                                  SELLER_COMPANY_FACT_ADDRESS1,
                                  SELLER_COMPANY_PHONE3,
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  2
                                    )
        page.reload()
        assertions.check_operator_ip_active_fields(1)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Успешное сохранение ИП в статус Отклонен автомодерацией(STATE LIQUIDATED)')
    def test_seller_company_details_ip_new2(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details =CompanyDetailsIp(page)
        # Пока обнуляю продавца и перед стартом тестов, на всякий случай
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive ()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN2_FALSE)
        assertions.check_operator_ip_state_front(page, 'ликвидирована')
        assertions.check_operator_ip_active_fields(1)
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN2_FALSE,
                                                SELLER_COMPANY_IP_FULLNAME2,
                                                SELLER_COMPANY_IP_OGRN2,
                                                SELLER_COMPANY_IP_BILL2,
                                                SELLER_COMPANY_IP_BIC2,
                                                SELLER_COMPANY_IP_BANK2,
                                                2,
                                                1
                                                  )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  SELLER_COMPANY_IP_INN2_FALSE,
                                  SELLER_COMPANY_IP_FULLNAME2,
                                  SELLER_COMPANY_IP_OGRN2,
                                  SELLER_COMPANY_IP_BILL2,
                                  SELLER_COMPANY_IP_BIC2,
                                  SELLER_COMPANY_IP_BANK2,
                                  SELLER_COMPANY_LEGAL_OR_IP_STATE_LIQUIDATED,
                                  SELLER_COMPANY_FACT_ADDRESS1,
                                  SELLER_COMPANY_PHONE3,
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  9
                                    )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Успешное сохранение ИП в статус Отклонен автомодерацией(STATE NULL Неизвестный статус)')
    def test_seller_company_details_ip_new3(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details =CompanyDetailsIp(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN3_NULL)
        assertions.check_operator_company_inn_state_null('Ничего не найдено')
        assertions.check_operator_ip_active_fields(1)
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                3,
                                                2
                                                )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_operator_ip_state_front(page, 'Неизвестный статус') 
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_IP_INN3_NULL,
                                    SELLER_COMPANY_IP_FULLNAME1,
                                    SELLER_COMPANY_IP_OGRN1,
                                    SELLER_COMPANY_IP_BILL1,
                                    SELLER_COMPANY_IP_BIC1,
                                    SELLER_COMPANY_IP_BANK1,
                                    None,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    8
                                        )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Проверка, что кнопка Сохранить у ИП активна только когда все поля заполнены')
    def test_seller_company_details_ip_new6(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details = CompanyDetailsIp(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN1_TRUE)
        assertions.check_operator_ip_state_front(page, 'действующая')
        assertions.check_operator_ip_active_fields(1)
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                0,
                                                1
                                                  )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                1,
                                                2
                                                  )
        assertions.check_operator_company_button_active()
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
        assertions.check_operator_company_button_active()
        company_details.fill_company_details_ip('',
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                '',
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                '',
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                '',
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                '',
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                '',
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                7,
                                                2
                                                  )
        assertions.check_operator_company_button_inactive()
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN3_NULL,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                4,
                                                2
                                                  )
        assertions.check_operator_company_button_active()
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_IP_INN3_NULL,
                                    SELLER_COMPANY_IP_FULLNAME1,
                                    SELLER_COMPANY_IP_OGRN1,
                                    SELLER_COMPANY_IP_BILL1,
                                    SELLER_COMPANY_IP_BIC1,
                                    SELLER_COMPANY_IP_BANK1,
                                    None,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    6
                                        )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Повторное сохранение ИП')
    def test_seller_company_details_ip_new7(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details = CompanyDetailsIp(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN1_TRUE)
        assertions.check_operator_ip_state_front(page, 'действующая')
        assertions.check_operator_ip_active_fields(1)
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN1_TRUE,
                                                SELLER_COMPANY_IP_FULLNAME1,
                                                SELLER_COMPANY_IP_OGRN1,
                                                SELLER_COMPANY_IP_BILL1,
                                                SELLER_COMPANY_IP_BIC1,
                                                SELLER_COMPANY_IP_BANK1,
                                                5,
                                                1
                                                  )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE3,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  SELLER_COMPANY_IP_INN1_TRUE,
                                  SELLER_COMPANY_IP_FULLNAME1,
                                  SELLER_COMPANY_IP_OGRN1,
                                  SELLER_COMPANY_IP_BILL1,
                                  SELLER_COMPANY_IP_BIC1,
                                  SELLER_COMPANY_IP_BANK1,
                                  SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
                                  SELLER_COMPANY_FACT_ADDRESS1,
                                  SELLER_COMPANY_PHONE3,
                                  SELLER_COMPANY_EMAIL3_NEW,
                                                5
                                    )
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN2_FALSE)
        assertions.check_operator_ip_state_front(page, 'ликвидирована')
        company_details.fill_company_details_ip(SELLER_COMPANY_IP_INN2_FALSE,
                                                SELLER_COMPANY_IP_FULLNAME2,
                                                SELLER_COMPANY_IP_OGRN2,
                                                SELLER_COMPANY_IP_BILL2,
                                                SELLER_COMPANY_IP_BIC2,
                                                SELLER_COMPANY_IP_BANK2,
                                                6,
                                                1
                                                  )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS2,
                                                      SELLER_COMPANY_PHONE2,
                                                      SELLER_COMPANY_EMAIL2)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_ip_in_db(db_connection, 
                                  SELLER_COMPANY_EMAIL3_NEW,
                                  SELLER_COMPANY_IP_INN2_FALSE,
                                  SELLER_COMPANY_IP_FULLNAME2,
                                  SELLER_COMPANY_IP_OGRN2,
                                  SELLER_COMPANY_IP_BILL2,
                                  SELLER_COMPANY_IP_BIC2,
                                  SELLER_COMPANY_IP_BANK2,
                                  SELLER_COMPANY_LEGAL_OR_IP_STATE_LIQUIDATED,
                                  SELLER_COMPANY_FACT_ADDRESS2,
                                  SELLER_COMPANY_PHONE2,
                                  SELLER_COMPANY_EMAIL2,
                                  1
                                    )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Проверка, что подтягивается из DADATA данные в ИП')
    def test_seller_company_details_ip_new8(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsIp(page)  
        company_details = CompanyDetailsIp(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_ip()
        assertions.check_operator_ip_inactive_fields(1)
        assertions.check_operator_company_button_inactive()
        company_details.company_details_choice_fill_inn_ip(SELLER_COMPANY_IP_INN1_TRUE)
        assertions.check_operator_ip_state_front(page, 'действующая')
        assertions.check_operator_ip_active_fields(1)
        assertions.check_operator_ip_fields_with_text(
            SELLER_COMPANY_IP_FULLNAME1,
            SELLER_COMPANY_IP_OGRN1
        )
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)     