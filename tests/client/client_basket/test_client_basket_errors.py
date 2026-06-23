import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Assertions.client.client_basket.assert_client_basket import AssertionsClientBasket
from Locators.loc_all_directories import ALL_LOCATORS
from pages.client.client_basket.client_basket import ClientBasket
from pages.seller.seller_auth_and_registration import SellerAuthRegistration #Можно будет поменять на SellerSummary, если методы там появятся 
from Assertions.seller.seller_summary.assert_seller_summary import AssertionsSellerSummary
from entities.tour.eni_tour import TourAPI
from entities.user.eni_user import UserAPI
import allure
from Constants.const_general import URL
from Constants.client.client_auth.const_client_auth import CLIENT_PHONE1, CLIENT_PHONE2
from Constants.seller.seller_summary.const_seller_summary import C_PAYOUT_TOAST_SUCCESS 
from Constants.client.client_tour_card.const_client_tour_card import C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP
from Constants.client.client_basket.const_client_basket import (
    #URL
    BASKET_PAGE_URL,
    #Пустая корзина
    CLIENT_BASKET_EMPTY_H1_VALUE,
    CLIENT_BASKET_EMPTY_H2_VALUE,
    CLIENT_BASKET_EMPTY_DESCRIPTION_VALUE,
    #Данные путешественника
    C_CLIENT_BASKET_LASTNAME,
    C_CLIENT_BASKET_NAME,
    C_CLIENT_BASKET_PATRONYMIC,
    C_CLIENT_BASKET_PHONE,
    C_CLIENT_BASKET_EMAIL,
    C_CLIENT_BASKET_EMAIL2,
    C_CLIENT_BASKET_EMAIL3,
    C_CLIENT_BASKET_EMAIL4,
    C_CLIENT_BASKET_DATE_BORN,
    #Данные путешественника ошибки
    C_CLIENT_BASKET_LASTNAME_ERROR,
    C_CLIENT_BASKET_NAME_ERROR,
    C_CLIENT_BASKET_EMAIL_ERROR,
    C_CLIENT_BASKET_EMAIL_ERROR2,
    C_CLIENT_BASKET_DATE_BORN_ERROR,
    #Промокод
    C_CLIENT_BASKET_PROMOCODE_NON_EXISTENT,
    C_CLIENT_BASKET_PROMOCODE1,
    C_CLIENT_BASKET_PROMOCODE2,
    C_CLIENT_BASKET_PROMOCODE3,
    C_CLIENT_BASKET_PROMOCODE4,
    C_CLIENT_BASKET_PROMOCODE5,
    C_CLIENT_BASKET_PROMOCODE6,
    C_CLIENT_BASKET_PROMOCODE7,
    #Ошибки
    C_CLIENT_BASKET_ERROR1,
    C_CLIENT_BASKET_ERROR2,
    C_CLIENT_BASKET_ERROR3,
    C_CLIENT_BASKET_ERROR4,
    C_CLIENT_BASKET_ERROR5,
    C_CLIENT_BASKET_ERROR6,
    C_CLIENT_BASKET_ERROR7,
    C_CLIENT_BASKET_ERROR8,
    C_CLIENT_BASKET_ERROR9,
    #Твои платежи
    C_CLIENT_BASKET_PAYMENT_SUMMA1,
    C_CLIENT_BASKET_PAYMENT_SUMMA2,
    C_CLIENT_BASKET_PAYMENT_SUMMA3,
    C_CLIENT_BASKET_PAYMENT_SUMMA4,
    C_CLIENT_BASKET_PAYMENT_SUMMA5,
    C_CLIENT_BASKET_PAYMENT_SUMMA6,
    C_CLIENT_BASKET_PAYMENT_SUMMA7,
    C_CLIENT_BASKET_PAYMENT_SUMMA8,
    C_CLIENT_BASKET_PAYMENT_SUMMA9,
    C_CLIENT_BASKET_PAYMENT_SUMMA10,
    C_CLIENT_BASKET_PAYMENT_SUMMA11,
    C_CLIENT_BASKET_PAYMENT_SUMMA12,
    C_CLIENT_BASKET_PAYMENT_SUMMA13,
    C_CLIENT_BASKET_PAYMENT_SUMMA14,
    C_CLIENT_BASKET_PAYMENT_SUMMA15,
    C_CLIENT_BASKET_PAYMENT_SUMMA16,
    #Страница успешной оплаты
    C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
    C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
    C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON,
    #Общее для всех заказов и подзаказов
    C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
    C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,


    #Первый тур 
    CLIENT_BASKET_TOUR1_BUY_ID,
    CLIENT_BASKET_TOUR1_BUY_A,
    CLIENT_BASKET_TOUR1_TITLE,
    C_CLIENT_BASKET_TOUR1_FORMAT,
    C_CLIENT_BASKET_TOUR1_CLASS,

    #Первый тур #Первый кейс для тура1 - Персональный
    CLIENT_BASKET_TOUR1_DATE_START1,
    CLIENT_BASKET_TOUR1_DATE_END1,
    C_CLIENT_BASKET_TOUR1_PRICE1,
    C_CLIENT_BASKET_TOUR1_OPTIONS1,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE1,
    #БД.Заказ1
    C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
    #БД.Подзаказ1
    CLIENT_BASKET_TOUR1_BUY_ID,
    C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
    #Общее
    C_CLIENT_BASKET_TOURS1,
    C_CLIENT_BASKET_OPTIONS1,
    C_CLIENT_BASKET_NUMBER_TRAVELERS1,
    C_CLIENT_BASKET_ALL_PRICE1,
    YOUR_PAYMENT_URL,

    #Второй кейс для тура1 - Групповой
    CLIENT_BASKET_TOUR1_DATE_START2,
    CLIENT_BASKET_TOUR1_DATE_END2,
    C_CLIENT_BASKET_TOUR1_PRICE2,
    C_CLIENT_BASKET_TOUR1_OPTIONS2,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE2,
    #БД.Заказ2
    C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
    #БД.Подзаказ2
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURID_DB2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB2,
    #Общее
    C_CLIENT_BASKET_TOURS2,
    C_CLIENT_BASKET_OPTIONS2,
    C_CLIENT_BASKET_NUMBER_TRAVELERS2,
    C_CLIENT_BASKET_ALL_PRICE2,

    #Третий кейс для тура1 - Персональный с опциями
    C_CLIENT_BASKET_TOUR1_OPTIONS3,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE3,
    #Общие цены
    C_CLIENT_BASKET_OPTIONS3,
    C_CLIENT_BASKET_ALL_PRICE3,
    #Третий кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB3,
    #Заказ3 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB3,
    C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB3,

    #Четвертый кейс для тура1 - Персональный с опциями
    C_CLIENT_BASKET_TOUR1_OPTIONS4,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE4,
    #Общие цены
    C_CLIENT_BASKET_OPTIONS4,
    C_CLIENT_BASKET_ALL_PRICE4,
    #Четвертый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB4,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB4,
    C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB4,

    #Пятый кейс для тура1 - Покупка персонального тура c промокодом1
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT5,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT5,
    #Пятый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB5,
    C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB5,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB5,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB5,

    #Шестой кейс для тура1 - Покупка персонального тура c промокодом1
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT6,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT6,
    #Шестой кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB6,
    C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB6,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB6,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB6,

)

@allure.feature('Клиент')
@allure.story('Корзина: Ошибки')
@pytest.mark.all
@pytest.mark.client
@pytest.mark.basket




class TestClientBasketErrors:
# Введите корректный email
#Негативные кейсы с очищением корзины

    # @allure.title('Пустая корзина')
    # def test_client_basket_errors1(self, page: Page, db_connection ):  
    #     assertions = AssertionsClientBasket(page) 
    #     clientbasket = ClientBasket(page)         
    #     clientbasket.client_go_to_auth_basket(CLIENT_PHONE1, db_connection )
    #     assertions.check_url(BASKET_PAGE_URL)
    #     assertions.check_empty_basket(CLIENT_BASKET_EMPTY_H1_VALUE, CLIENT_BASKET_EMPTY_H2_VALUE, CLIENT_BASKET_EMPTY_DESCRIPTION_VALUE)
    #     clientbasket.click_element('Кнопка Начать планирование  в пустой корзине клиента')
    #     assertions.check_url(URL)

    @allure.title('Данные продавца не заполнены. Клиент Авторизован')
    def test_client_basket_errors2(self, page: Page, db_connection ):  
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        user = UserAPI()
        user.delete_user_by_phone(db_connection, CLIENT_PHONE2)
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE2) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        clientbasket.add_passengers_to_tourcard(0,2,3,4,5)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        page.wait_for_timeout(500)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth('',
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        assertions.check_field_value_from_locator('Фамилия в корзине ошибка', C_CLIENT_BASKET_LASTNAME_ERROR)
        assertions.check_element_class_starts_with('Фамилия в корзине граница', '_error')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR1)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth('',
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Условия договора на приобретение продукта')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR9)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         '',
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)        
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        assertions.check_field_value_from_locator('Имя в корзине ошибка', C_CLIENT_BASKET_NAME_ERROR)
        assertions.check_element_class_starts_with('Имя в корзине граница', '_error')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR1)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         '',
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,) 
        clientbasket.click_element('Условия договора на приобретение продукта')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR9)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         '',
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        assertions.check_field_value_from_locator('Емаил в корзине ошибка', C_CLIENT_BASKET_EMAIL_ERROR)
        assertions.check_element_class_starts_with('Емаил в корзине граница', '_error')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR1)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL4,
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        assertions.check_field_value_from_locator('Емаил в корзине ошибка', C_CLIENT_BASKET_EMAIL_ERROR2)
        assertions.check_element_class_starts_with('Емаил в корзине граница', '_error')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR1)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL,
                                         '',)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        assertions.check_field_value_from_locator('Дата рождения в корзине ошибка', C_CLIENT_BASKET_DATE_BORN_ERROR)
        assertions.check_element_class_starts_with('Дата рождения в корзине граница', '_error')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR1)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_EMAIL2,
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        page.wait_for_timeout(200)
        # assertions.check_field_value_from_locator('Емаил в корзине ошибка', C_CLIENT_BASKET_EMAIL_ERROR2)
        # assertions.check_element_class_starts_with('Емаил в корзине граница', '_error') БАГ не выделяе поле, не показывает под ним ошибку, как с остальными
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR7)
        page.reload()
        #Перестала появляться ошибка на фронте, сейчас приходит в store Invalid field BILL_EMAIL
        # page.wait_for_timeout(1500)
        # clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
        #                                  C_CLIENT_BASKET_NAME,
        #                                  C_CLIENT_BASKET_PATRONYMIC,
        #                                  C_CLIENT_BASKET_EMAIL3,
        #                                  C_CLIENT_BASKET_DATE_BORN,)
        # clientbasket.click_element('Кнопка Оплатить картой в корзине')
        # page.wait_for_timeout(200)
        # assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR8)
        page.reload()
        page.wait_for_timeout(1500)
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         '',
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        user.delete_user_by_phone(db_connection, CLIENT_PHONE2)

    @allure.title('Ошибка:Выбрано больше мест, чем доступно в этот день. Персональный. Без учета занятых')
    def test_client_basket_errors3(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Третья дата в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        clientbasket.add_passengers_to_basket(0,1,0,0,0)
        assertions.check_data_participants_amount_basket('1','1','0','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,1,0,0,0)
        assertions.check_data_participants_amount_basket('1','2','0','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,1,0,0)
        assertions.check_data_participants_amount_basket('1','2','1','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,1,0,0)
        assertions.check_data_participants_amount_basket('1','2','2','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,1,0,0)
        assertions.check_data_participants_amount_basket('1','2','3','0','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,1,0)
        assertions.check_data_participants_amount_basket('1','2','3','1','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,1,0)
        assertions.check_data_participants_amount_basket('1','2','3','2','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,1,0)
        assertions.check_data_participants_amount_basket('1','2','3','3','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,1,0)
        assertions.check_data_participants_amount_basket('1','2','3','4','0')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_data_participants_amount_basket('1','2','3','4','1')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_data_participants_amount_basket('1','2','3','4','2')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_data_participants_amount_basket('1','2','3','4','3')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_data_participants_amount_basket('1','2','3','4','4')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket(1,0,0,0,0)
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_with_error(1,0,0,0,0)
        clientbasket.add_passengers_to_basket(0,1,0,0,0)
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_with_error(0,1,0,0,0)
        clientbasket.add_passengers_to_basket(0,0,1,0,0)
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_with_error(0,0,1,0,0)
        clientbasket.add_passengers_to_basket(0,0,0,1,0)
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_with_error(0,0,0,1,0)
        clientbasket.add_passengers_to_basket(0,0,0,0,1)
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_with_error(0,0,0,0,1)
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])

    @allure.title('Ошибка:Выбрано больше мест, чем доступно в этот день. Групповой. Без учета занятых') 
    def test_client_basket_errors4(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Шестая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '1')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        clientbasket.add_passengers_to_basket_group(5)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '6')
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.add_passengers_to_basket_group(1)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '7')
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])
        clientbasket.minus_passengers_to_basket_group(1)
        assertions.check_div_with_text_not_present(C_CLIENT_BASKET_ERROR2)
        assertions.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Оплатить картой в корзине'])

    @allure.title('Ошибки промокодов')
    def test_client_basket_errors5(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        clientbasket.add_passengers_to_tourcard(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled('15 чел')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE_NON_EXISTENT)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR3)
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE4)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR4)
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE5)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR5)
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE6) #Когда действует не на все туры. Ошибки не приходит. Т.к. корзина может быть составная
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE7)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        assertions.check_div_with_text(C_CLIENT_BASKET_ERROR6)

    @allure.title('Покупка после ошибки, что такая почта уже есть') 
    def test_client_basket_errors6(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_number_participants_rolled('1 чел')
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        assertions.check_data_participants_amount_tourcard('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled('15 чел')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                '0 ₽',
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.fill_main_traveller_auth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         'nikitatimoshinpost@gmail.com',
                                         C_CLIENT_BASKET_DATE_BORN)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине', C_CLIENT_BASKET_ERROR7)
        clientbasket.fill_element('Емаил в корзине', 'nikitatimoshinpost@rambler.ru')
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                            None
                                          )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6) 

    @allure.title('Покупка после ошибки Твоих платежей, что почта неправильная')
    def test_client_basket_errors7(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_number_participants_rolled('1 чел')
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        assertions.check_data_participants_amount_tourcard('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled('15 чел')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1)
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.fill_element('Емаил в корзине', 'nikitatimoshinpost@rambler.ru12345')
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_toast_message('Всплывающий toast ошибки в корзине неавторизованного', C_CLIENT_BASKET_ERROR8)
        clientbasket.fill_element('Емаил в корзине', 'nikitatimoshinpost@rambler.ru')
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                            None
                                          )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)
