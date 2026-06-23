import pytest
from playwright.sync_api import Page
from fixtures.all import db_connection  
from Assertions.seller.seller_summary.assert_seller_summary import AssertionsSellerSummary
from pages.seller.seller_auth_and_registration import SellerAuthRegistration # Можно заменить на SellerSummary потом
from entities.tour.eni_tour import TourAPI
from entities.operations.eni_operations import OperationsAPI
import allure
from Locators.loc_all_directories import ALL_LOCATORS
from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN1_REGISTR,
    SELLER_PASSWORD1,
)
from Constants.seller.seller_summary.const_seller_summary import(
    C_PAYOUT_TOAST_SUCCESS,
    C_PAYOUT_ERROR1,
    C_PAYOUT_ERROR2,
    C_PAYOUT_ERROR3,
    C_PAYOUT_ERROR4,
    C_PAYOUT_ERROR5,
    C_PAYOUT_ERROR6,
)


@allure.feature('Продавец')
@allure.story('Сводка продавца')
@pytest.mark.all
@pytest.mark.seller
class TestSellerSummary:

#Успешные кейсы вместе с заказами проверяются

    @allure.title('Ошибки при вводе кода из смс')
    def test_seller_summary1(self, page: Page, db_connection):
        assertions = AssertionsSellerSummary(page) 
        clientsummary = SellerAuthRegistration(page) # Можно заменить на SellerSummary потом
        tour = TourAPI() 
        operation = OperationsAPI()
        operation.delete_operations_by_order_and_type(db_connection, 2330, 5)
        tour.change_product_status(925,5)
        clientsummary.seller_auth(page, SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1)
        assertions.check_url('https://dev.smorodina.ru/operator/summary')
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Получить оплату в сводке продавца'])
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '1' )
        clientsummary.fill_element('Код в сводке продавца', '999')
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Получить оплату в сводке продавца'])
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR1)
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '1' )
        clientsummary.fill_element('Код в сводке продавца', '99999')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR1)
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '1' )
        clientsummary.fill_element('Код в сводке продавца', '9999')
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '1234567' )
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR2)
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '123456' )
        clientsummary.fill_element('Код в сводке продавца', '9999')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR3)  
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '2327' )
        clientsummary.fill_element('Код в сводке продавца', '9999')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR4) 
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '2329' )
        clientsummary.fill_element('Код в сводке продавца', '9999')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR5) 
        page.reload()
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '2330' )
        clientsummary.fill_element('Код в сводке продавца', '5458')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца') 
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_TOAST_SUCCESS) 
        page.reload()  
        clientsummary.fill_element('Номер подзаказа в сводке продавца', '2330' )
        clientsummary.fill_element('Код в сводке продавца', '5458')
        clientsummary.click_element('Кнопка Получить оплату в сводке продавца') 
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_ERROR6)     
        #Проверка в разных статусах тура
        # ПРОВЕРКА В РАЗНЫХ СТАТУСАХ ЗАКАЗА
        operation.delete_operations_by_order_and_type(db_connection, 2330, 5)
        tour.change_product_status(925,5)