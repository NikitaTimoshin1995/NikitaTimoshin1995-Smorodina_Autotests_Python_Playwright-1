import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection, photo_paths  
from Assertions.seller.seller_company_details.seller_company_details_legal.seller_company_details_legal import AssertionsCompanyDetailsLegal
from pages.seller.seller_company_details.seller_company_details_legal.seller_company_details_legal import CompanyDetailsLegal
import allure
from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    #Контактная информация общая
    SELLER_COMPANY_PHONE3,
    SELLER_COMPANY_EMAIL3_NEW,
    SELLER_COMPANY_FACT_ADDRESS1,
    SELLER_COMPANY_PHONE1,
    SELLER_COMPANY_EMAIL1,
    SELLER_COMPANY_FACT_ADDRESS2,
    SELLER_COMPANY_PHONE2,
    SELLER_COMPANY_EMAIL2,
    #ЮР
    SELLER_COMPANY_LEGAL_INN1_TRUE,
    SELLER_COMPANY_LEGAL_INN1_NOT_FULL,
    SELLER_COMPANY_LEGAL_INN2_FALSE,
    SELLER_COMPANY_LEGAL_INN3_NULL,
    SELLER_COMPANY_LEGAL_OPF1,
    SELLER_COMPANY_LEGAL_OPF2,
    SELLER_COMPANY_LEGAL_FULLNAME1,
    SELLER_COMPANY_LEGAL_FULLNAME2,
    SELLER_COMPANY_LEGAL_SHORTNAME1,
    SELLER_COMPANY_LEGAL_SHORTNAME2,
    SELLER_COMPANY_LEGAL_ADDRESS1,
    SELLER_COMPANY_LEGAL_ADDRESS2,
    SELLER_COMPANY_LEGAL_KPP,
    SELLER_COMPANY_LEGAL_KPP2,
    SELLER_COMPANY_LEGAL_OGRN1,
    SELLER_COMPANY_LEGAL_OGRN2,
    SELLER_COMPANY_LEGAL_BILL1,
    SELLER_COMPANY_LEGAL_BILL2,
    SELLER_COMPANY_LEGAL_BIC1,
    SELLER_COMPANY_LEGAL_BIC2,
    SELLER_COMPANY_LEGAL_BANK1,
    SELLER_COMPANY_LEGAL_BANK2,
    SELLER_COMPANY_LEGAL_DIRECTOR1,
    SELLER_COMPANY_LEGAL_DIRECTOR2,
    SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
    SELLER_COMPANY_LEGAL_OR_IP_STATE_LIQUIDATED,
    #Информация для путешественников
    C_SELLER_FIELD_COMPANY_INFO_NAME,
    C_SELLER_FIELD_COMPANY_INFO_YEARS,
    C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
    C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION,
    C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION_DB,
    #Предупреждения
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING1,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING2,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING4,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING5,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING6,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING7,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING8,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING16
)

#Можно добавить тесты на переход из разных state, как у самозанятого, и смена данных на второй сет


@allure.feature('Продавец')
@allure.story('Данные компании продавца ООО. Новый продавец.')
@pytest.mark.all
@pytest.mark.seller
@pytest.mark.company_details


class TestSellerCompanyDetailsLegalNew:

#     #Новый продавец ##########################################################################
    @allure.title('Новый продавец.Успешное сохранение Юр.лица в статус Проверен(STATE ACTIVE). Только обязательные поля')
    def test_seller_company_details_legal_new1(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details =CompanyDetailsLegal(page)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)
        ##########################################################################
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        assertions.check_operator_legal_active_fields(1)
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  1,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          '',
                                          '',
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)                  
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_LEGAL_INN1_TRUE,
                                    SELLER_COMPANY_LEGAL_OPF1,
                                    SELLER_COMPANY_LEGAL_FULLNAME1,
                                    SELLER_COMPANY_LEGAL_SHORTNAME1,
                                    SELLER_COMPANY_LEGAL_ADDRESS1,
                                    SELLER_COMPANY_LEGAL_KPP,
                                    SELLER_COMPANY_LEGAL_OGRN1,
                                    SELLER_COMPANY_LEGAL_BILL1,
                                    SELLER_COMPANY_LEGAL_BIC1,
                                    SELLER_COMPANY_LEGAL_BANK1,                        
                                    SELLER_COMPANY_LEGAL_DIRECTOR1,
                                    SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    2
                                     )
        assertions.check_operator_info_in_db(db_connection,
                                             SELLER_COMPANY_EMAIL3_NEW,
                                             C_SELLER_FIELD_COMPANY_INFO_NAME,
                                             None,
                                             None,
                                             C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION_DB)
        assertions.check_operator_legal_active_fields(1)
        assertions.check_operator_info_fields_active()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )      
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        page.reload()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец.Успешное сохранение Юр.лица в статус Отклонен автомодерацией(STATE LIQUIDATED) Только обязательные поля')
    def test_seller_company_details_legal_new2(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details = CompanyDetailsLegal(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN2_FALSE)
        assertions.check_operator_legal_state_front(page, 'ликвидирована')
        assertions.check_operator_legal_active_fields(1)
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN2_FALSE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  2,
                                                  1 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          '',
                                          '',
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_LEGAL_INN2_FALSE,
                                    SELLER_COMPANY_LEGAL_OPF1,
                                    SELLER_COMPANY_LEGAL_FULLNAME1,
                                    SELLER_COMPANY_LEGAL_SHORTNAME1,
                                    SELLER_COMPANY_LEGAL_ADDRESS1,
                                    SELLER_COMPANY_LEGAL_KPP,
                                    SELLER_COMPANY_LEGAL_OGRN1,
                                    SELLER_COMPANY_LEGAL_BILL1,
                                    SELLER_COMPANY_LEGAL_BIC1,
                                    SELLER_COMPANY_LEGAL_BANK1,                        
                                    SELLER_COMPANY_LEGAL_DIRECTOR1,
                                    SELLER_COMPANY_LEGAL_OR_IP_STATE_LIQUIDATED,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    9
                                     )
        assertions.check_operator_legal_active_fields(1)
        assertions.check_operator_info_fields_active()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN2_FALSE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        page.wait_for_timeout(500)
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        page.reload()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN2_FALSE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец.Успешное сохранение Юр.лица в статус Отклонен автомодерацией(STATE NULL Неизвестный статус) Только обязательные поля')
    def test_seller_company_details_legal_new3(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details = CompanyDetailsLegal(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN3_NULL)
        assertions.check_operator_company_inn_state_null('Ничего не найдено')
        assertions.check_operator_legal_active_fields(2)
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN3_NULL,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  2 )
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          '',
                                          '',
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Не пройдена автомодерация')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 13)
        assertions.check_operator_legal_state_front(page, 'Неизвестный статус') 
        assertions.check_request_statuses(intercept_requests)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_LEGAL_INN3_NULL,
                                    SELLER_COMPANY_LEGAL_OPF1,
                                    SELLER_COMPANY_LEGAL_FULLNAME1,
                                    SELLER_COMPANY_LEGAL_SHORTNAME1,
                                    SELLER_COMPANY_LEGAL_ADDRESS1,
                                    SELLER_COMPANY_LEGAL_KPP,
                                    SELLER_COMPANY_LEGAL_OGRN1,
                                    SELLER_COMPANY_LEGAL_BILL1,
                                    SELLER_COMPANY_LEGAL_BIC1,
                                    SELLER_COMPANY_LEGAL_BANK1,                         
                                    SELLER_COMPANY_LEGAL_DIRECTOR1,
                                    None,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    5
                                     )
        assertions.check_operator_info_in_db(db_connection,
                                             SELLER_COMPANY_EMAIL3_NEW,
                                             C_SELLER_FIELD_COMPANY_INFO_NAME,
                                             None,
                                             None,
                                             C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION_DB)
        assertions.check_operator_legal_active_fields(1)
        assertions.check_operator_info_fields_active()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN3_NULL,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        page.wait_for_timeout(500)
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        page.reload()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN3_NULL,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            '',
                                                            '',
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец.Проверка, что кнопка Сохранить у Юр.лица активна только когда все поля заполнены')
    def test_seller_company_details_legal_new4(self, page: Page, db_connection,intercept_requests, photo_paths):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details = CompanyDetailsLegal(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        assertions.check_operator_legal_active_fields(1)
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  1,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL3_NEW)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        paths = photo_paths("1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg", "11.jpg")
        company_details.upload_photos_company('Инфо организатора поле загрузки фото', *paths)
        assertions.check_operator_info__photo_db(db_connection, SELLER_COMPANY_EMAIL3_NEW, 10)
        assertions.check_operator_logo_in_db(db_connection, SELLER_COMPANY_EMAIL3_NEW, False)
        paths = photo_paths( "avatar.webp")
        company_details.upload_photos_company('Инфо организатора поле загрузки аватара', *paths)
        assertions.check_operator_logo_in_db(db_connection, SELLER_COMPANY_EMAIL3_NEW, True)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_LEGAL_INN1_TRUE,
                                    SELLER_COMPANY_LEGAL_OPF1,
                                    SELLER_COMPANY_LEGAL_FULLNAME1,
                                    SELLER_COMPANY_LEGAL_SHORTNAME1,
                                    SELLER_COMPANY_LEGAL_ADDRESS1,
                                    SELLER_COMPANY_LEGAL_KPP,
                                    SELLER_COMPANY_LEGAL_OGRN1,
                                    SELLER_COMPANY_LEGAL_BILL1,
                                    SELLER_COMPANY_LEGAL_BIC1,
                                    SELLER_COMPANY_LEGAL_BANK1,                        
                                    SELLER_COMPANY_LEGAL_DIRECTOR1,
                                    SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    2
                                     )
        assertions.check_operator_info_in_db(db_connection,
                                             SELLER_COMPANY_EMAIL3_NEW,
                                             C_SELLER_FIELD_COMPANY_INFO_NAME,
                                             C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                             C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                             C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION_DB)
        assertions.check_operator_legal_active_fields(1)
        assertions.check_operator_info_fields_active()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                                            C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        page.reload()
        assertions.check_operator_legal_all_fields_with_text(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                        SELLER_COMPANY_LEGAL_OPF1,
                                                        SELLER_COMPANY_LEGAL_FULLNAME1,
                                                        SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                        SELLER_COMPANY_LEGAL_ADDRESS1,
                                                        SELLER_COMPANY_LEGAL_KPP,
                                                        SELLER_COMPANY_LEGAL_OGRN1,
                                                        SELLER_COMPANY_LEGAL_BILL1,
                                                        SELLER_COMPANY_LEGAL_BIC1,
                                                        SELLER_COMPANY_LEGAL_BANK1,
                                                        SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                        SELLER_COMPANY_FACT_ADDRESS1,
                                                        SELLER_COMPANY_PHONE1,
                                                        SELLER_COMPANY_EMAIL3_NEW
                                                        )
        assertions.check_operator_org_info_fields_with_text(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                                            C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                                            C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                                            C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Проверка вывода ошибок')
    def test_seller_company_details_legal_new5(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details = CompanyDetailsLegal(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        assertions.check_operator_company_button_active()
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING1)
        assertions.check_operator_legal_fields_border_normal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        assertions.check_operator_legal_fields_border_short_red()
        assertions.check_operator_legal_fields_errors_short()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN3_NULL)
        assertions.check_operator_legal_active_fields(2)
        company_details.fill_element('Юр ИНН',  '')
        company_details.fill_element('Юр Полное наименование',  '')
        company_details.fill_element('Юр Краткое наименование',  '')
        company_details.fill_element('Контактная информация Телефон',  '')
        company_details.fill_element('Контактная информация E-mail',  '')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_legal_fields_border_full_red()
        assertions.check_operator_legal_fields_errors_full()
        # ИНН
        company_details.company_details_choice_fill_inn_legal('1')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('12')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('123')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('1234')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('12345')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('123456')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('1234567')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('12345678')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('123456789')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING11)
        assertions.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        company_details.company_details_choice_fill_inn_legal('1234567891')
        assertions.check_field_value_from_locator('Юр ИНН предепреждение1', 'Ничего не найдено')
        assertions.check_element_class_not_starts_with('Юр ИНН граница', '_inputError')
        #ОПФ
        company_details.fill_element('Юр ОПФ', SELLER_COMPANY_LEGAL_OPF1)    
        assertions.check_element_class_not_starts_with('Юр ОПФ граница', '_inputError') 
        #Полное имя  
        company_details.fill_element('Юр Полное наименование', SELLER_COMPANY_LEGAL_FULLNAME1)    
        assertions.check_element_class_not_starts_with('Юр Полное наименование граница', '_inputError')
        #Краткое имя
        company_details.fill_element('Юр Краткое наименование', SELLER_COMPANY_LEGAL_SHORTNAME1)  
        assertions.check_element_class_not_starts_with('Юр Краткое наименование граница', '_inputError')
        #ЮР адрес
        company_details.fill_element('Юр Юр. адрес', SELLER_COMPANY_LEGAL_ADDRESS1)  
        assertions.check_element_class_not_starts_with('Юр Юр. адрес граница', '_inputError')
        #КПП
        company_details.fill_element('Юр КПП', '1') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '12') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '1234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '12345') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '123456') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '1234567') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '12345678') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING12)
        assertions.check_element_class_starts_with('Юр КПП граница', '_inputError')
        company_details.fill_element('Юр КПП', '123456789') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_not_starts_with('Юр КПП граница', '_inputError')
        #ОГРН
        company_details.fill_element('Юр ОГРН', '1') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '12') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '1234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '12345') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '123456') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '1234567') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '12345678') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '123456789') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '1234567891') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '12345678911') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '123456789112') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING13)
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '12345678911234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        company_details.fill_element('Юр ОГРН', '1234567891123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_not_starts_with('Юр ОГРН граница красная', '_inputError')
        #Р. / счёт
        company_details.fill_element('Юр Р. / счёт', '1') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234567') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345678') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456789') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234567891') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345678911') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456789112') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234567891123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345678911234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456789112345') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234567891123456') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345678911234567') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456789112345678') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '1234567891123456789') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING14)
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '123456789112345678921') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        company_details.fill_element('Юр Р. / счёт', '12345678911234567892') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_not_starts_with('Юр Р. / счёт граница', '_inputError')
        #БИК
        company_details.fill_element('Юр БИК', '1') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '12') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '123') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '1234') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '12345') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '123456') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '1234567') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '12345678') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING15)
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '1234567891') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        company_details.fill_element('Юр БИК', '123456789') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_element_class_not_starts_with('Юр БИК граница красная', '_inputError')
        #БАНК
        company_details.fill_element('Юр Банк', SELLER_COMPANY_LEGAL_BANK1)
        assertions.check_element_class_not_starts_with('Юр Банк граница', '_inputError')
        #ФИО ген. директора
        company_details.fill_element('Юр ФИО ген. директора', SELLER_COMPANY_LEGAL_DIRECTOR1)        
        assertions.check_element_class_not_starts_with('Юр ФИО ген. директора граница', '_inputError')
        #Контактная информация
        company_details.fill_element('Контактная информация Факт. адрес',  SELLER_COMPANY_FACT_ADDRESS1)
        assertions.check_element_class_not_starts_with('Контактная информация Факт. адрес граница', '_inputError')
        company_details.fill_element('Контактная информация Телефон',  SELLER_COMPANY_PHONE1)
        assertions.check_element_class_not_starts_with('Контактная информация Телефон граница', '_inputError')
        company_details.fill_element('Контактная информация E-mail',  SELLER_COMPANY_EMAIL1)
        assertions.check_element_class_not_starts_with('Контактная информация E-mail граница', '_inputError')
        #Информация для путешественников
        company_details.fill_element('Инфо организатора имя', 'Никита')
        assertions.check_element_class_not_starts_with('Инфо организатора имя граница', '_inputError')
        company_details.fill_element('Инфо организатора описание', C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)
        assertions.check_element_class_not_starts_with('Инфо организатора описание граница', '_inputError')
        # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

    @allure.title('Новый продавец. Проверка, что не сохраняются данные без обязательных полей')
    def test_seller_company_details_legal_new6(self, page: Page, db_connection,intercept_requests):  
        assertions = AssertionsCompanyDetailsLegal(page)  
        company_details = CompanyDetailsLegal(page)
        company_details.open_company_details_with_create(page, db_connection)
        company_details.open_company_details_choice_form_legal()
        assertions.check_operator_legal_inactive_fields(1)
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        assertions.check_operator_legal_active_fields(1)
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  0,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)               
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING16)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_legal('',
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)  
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)     
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')  
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)       
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)   
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)  
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)   
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)  
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)   
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)    
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)   
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)  
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)    
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)    
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)   
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  '',
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)  
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION)   
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  '',
                                                  5,
                                                  1)  
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_contacts('',
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      '',
                                                      SELLER_COMPANY_EMAIL1)
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      '')
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info('',
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        page.reload()
        company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
        assertions.check_operator_legal_state_front(page, 'действующая')
        company_details.fill_company_details_legal(SELLER_COMPANY_LEGAL_INN1_TRUE,
                                                  SELLER_COMPANY_LEGAL_OPF1,
                                                  SELLER_COMPANY_LEGAL_FULLNAME1,
                                                  SELLER_COMPANY_LEGAL_SHORTNAME1,
                                                  SELLER_COMPANY_LEGAL_ADDRESS1,
                                                  SELLER_COMPANY_LEGAL_KPP,
                                                  SELLER_COMPANY_LEGAL_OGRN1,
                                                  SELLER_COMPANY_LEGAL_BILL1,
                                                  SELLER_COMPANY_LEGAL_BIC1,
                                                  SELLER_COMPANY_LEGAL_BANK1,
                                                  SELLER_COMPANY_LEGAL_DIRECTOR1,
                                                  5,
                                                  1)
        company_details.fill_company_details_contacts(SELLER_COMPANY_FACT_ADDRESS1,
                                                      SELLER_COMPANY_PHONE1,
                                                      SELLER_COMPANY_EMAIL1)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          C_SELLER_FIELD_COMPANY_INFO_YEARS,
                                          C_SELLER_FIELD_COMPANY_INFO_COUNT_TOURS,
                                          '') 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    None,
                                    None,
                                    'ООО Автотест2',
                                    'ООО Автотест2',
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,                        
                                    None,
                                    None,
                                    None,
                                    SELLER_COMPANY_PHONE3,
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    10
                                     )
        assertions.check_operator_info_in_db(db_connection,
                                             SELLER_COMPANY_EMAIL3_NEW,
                                             None,
                                             None,
                                             None,
                                             None)
        company_details.fill_company_info(C_SELLER_FIELD_COMPANY_INFO_NAME,
                                          '',
                                          '',
                                          C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION) 
        company_details.click_element('кнопка Сохранить в данных компании продавца')
        assertions.check_operator_status_front( page, 'Проверен')
        assertions.check_operator_status(db_connection, SELLER_COMPANY_EMAIL3_NEW, 2)
        assertions.check_request_statuses(intercept_requests)
        assertions.check_legal_in_db(db_connection, 
                                    SELLER_COMPANY_EMAIL3_NEW,
                                    SELLER_COMPANY_LEGAL_INN1_TRUE,
                                    SELLER_COMPANY_LEGAL_OPF1,
                                    SELLER_COMPANY_LEGAL_FULLNAME1,
                                    SELLER_COMPANY_LEGAL_SHORTNAME1,
                                    SELLER_COMPANY_LEGAL_ADDRESS1,
                                    SELLER_COMPANY_LEGAL_KPP,
                                    SELLER_COMPANY_LEGAL_OGRN1,
                                    SELLER_COMPANY_LEGAL_BILL1,
                                    SELLER_COMPANY_LEGAL_BIC1,
                                    SELLER_COMPANY_LEGAL_BANK1,                        
                                    SELLER_COMPANY_LEGAL_DIRECTOR1,
                                    SELLER_COMPANY_LEGAL_OR_IP_STATE_ACTIVE,
                                    SELLER_COMPANY_FACT_ADDRESS1,
                                    SELLER_COMPANY_PHONE1,
                                    SELLER_COMPANY_EMAIL1,
                                    5
                                     )
        assertions.check_operator_info_in_db(db_connection,
                                             SELLER_COMPANY_EMAIL3_NEW,
                                             C_SELLER_FIELD_COMPANY_INFO_NAME,
                                             None,
                                             None,
                                             C_SELLER_FIELD_COMPANY_INFO_DESCRIPTION_DB)
#          # Удаление пользователя и связанных данных из базы данных
        company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)

#     @allure.title('Новый продавец.Проверка, что подтягивается из DADATA данные в Юр')
#     def test_seller_company_details_legal_new7(self, page: Page, db_connection,intercept_requests):  
#         assertions = AssertionsCompanyDetailsLegal(page)  
#         company_details = CompanyDetailsLegal(page)
#         company_details.open_company_details_with_create(page, db_connection)
#         company_details.open_company_details_choice_form_legal()
#         assertions.check_operator_legal_inactive_fields(1)
#         company_details.company_details_choice_fill_inn_legal(SELLER_COMPANY_LEGAL_INN1_TRUE)
#         assertions.check_operator_legal_state_front(page, 'действующая')
#         assertions.check_operator_legal_active_fields(1)
#         assertions.check_operator_legal_fields_with_text(
#             SELLER_COMPANY_LEGAL_OPF1,
#             SELLER_COMPANY_LEGAL_FULLNAME1,
#             SELLER_COMPANY_LEGAL_FULLNAME1,
#             SELLER_COMPANY_LEGAL_ADDRESS1,
#             SELLER_COMPANY_LEGAL_KPP,
#             SELLER_COMPANY_LEGAL_OGRN1
#         )
#          # Удаление пользователя и связанных данных из базы данных
#         company_details.delete_user_and_related_data(db_connection, SELLER_COMPANY_EMAIL3_NEW)       
