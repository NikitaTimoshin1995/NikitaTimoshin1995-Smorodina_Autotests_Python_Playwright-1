import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection
from Assertions.client.client_basket.assert_client_basket import AssertionsClientBasket
from Locators.loc_all_directories import ALL_LOCATORS
from pages.client.client_basket.client_basket import ClientBasket
from pages.seller.seller_auth_and_registration import SellerAuthRegistration #Можно будет поменять на SellerSummary, если методы там появятся 
from Assertions.seller.seller_summary.assert_seller_summary import AssertionsSellerSummary
from entities.tour.eni_tour import TourAPI
import allure
from Constants.const_general import URL
from Constants.client.client_auth.const_client_auth import CLIENT_PHONE1
from Constants.seller.seller_summary.const_seller_summary import (
    C_PAYOUT_STATUS1,
    C_PAYOUT_INFO1,
    C_PAYOUT_TYPE5,
    C_PAYOUT_OPERATOR_ID1,
    C_PAYOUT_OPERATOR_ID2
)
from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN5_BASKET,
    SELLER_LOGIN5_BASKET2,
    SELLER_PASSWORD1,
)
from Constants.client.client_tour_card.const_client_tour_card import (
    #Дата
    C_CLIENT_TOUR_CARD_DATAPICKER_DATE1,
    C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME,
    C_CLIENT_TOUR_CARD_DATAPICKER_DATE2,
    C_CLIENT_TOUR_CARD_DATAPICKER_DATE3,
    C_CLIENT_TOUR_CARD_DATAPICKER_DATE4,
    #Выбор участников персональный
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME2,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME3,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME4,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME5,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE1,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE2,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE3,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE4,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE5,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES1,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES2,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES3,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES4,
    #Выбор участников групповой
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP,
    #Цена в кнопке Купить
    C_CLIENT_TOUR_CARD_GROUP_AMOUNT1,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE5,
    C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE6,
    )
from Constants.seller.seller_summary.const_seller_summary import C_PAYOUT_TOAST_SUCCESS, C_PAYOUT_INFO2 
from Constants.client.client_basket.const_client_basket import (
    BASKET_PAGE_URL,
    #Данные путешественника
    C_CLIENT_BASKET_LASTNAME,
    C_CLIENT_BASKET_NAME,
    C_CLIENT_BASKET_PATRONYMIC,
    C_CLIENT_BASKET_PHONE,
    C_CLIENT_BASKET_EMAIL,
    C_CLIENT_BASKET_DATE_BORN,
    #Промокод
    C_CLIENT_BASKET_PROMOCODE1,
    C_CLIENT_BASKET_PROMOCODE2,
    C_CLIENT_BASKET_PROMOCODE3,
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
    C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
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
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB3,
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
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB4,
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
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB5,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB5,

    #Шестой кейс для тура1 - Покупка персонального тура c промокодом1
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT6,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT6,
    #Шестой кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB6,
    C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB6,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB6,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB6,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB6,

    #Седьмой кейс для тура1 - Покупка персонального тура c сменой количества уч.
    #Цены в туре
    C_CLIENT_BASKET_TOUR1_PRICE7,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE7,
    #Общие цены
    C_CLIENT_BASKET_NUMBER_TRAVELERS7,
    C_CLIENT_BASKET_TOURS7,
    C_CLIENT_BASKET_ALL_PRICE7,

    #Восьмой кейс для тура1 - Покупка персонального тура с опциями c с промокодом1
    #Цены в туре
    C_CLIENT_BASKET_TOUR1_ALL_PRICE8,
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT8,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT8,
    #Восьмой кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB8,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB8,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB8,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB8,

    #Девятый кейс для тура1 - Покупка персонального тура с опциями c с промокодом2
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT9,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT9,
    #Девятый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB9,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB9,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB9,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB9,  

    #Десятый кейс для тура1 - Покупка персонального тура с опциями c с промокодом3
    #Общие цены
    C_CLIENT_BASKET_COMMENT,

    #Одинадцатый кейс для тура1 - Покупка персонального тура с опциями c с промокодом3
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT11, 
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT11, 
    #Одинадцатый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB11, 
    C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB11, 
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB11, 
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB11, 
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB11, 

    #Двенадцатый кейс для тура1 - Покупка группового тура с промокодом2
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT12,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT12,
    #Двенадцатый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB12,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB12,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB12,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB12,

    #Тринадцатый кейс для тура1 - Покупка группового c изменением количества уч.
    C_CLIENT_BASKET_TOUR1_PRICE13,
    C_CLIENT_BASKET_TOUR1_ALL_PRICE13,
    #Общие цены
    C_CLIENT_BASKET_NUMBER_TRAVELERS13,
    C_CLIENT_BASKET_TOURS13,
    C_CLIENT_BASKET_ALL_PRICE13,
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB13,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB13,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB13,
    C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB13,

    #Четырнадцатый кейс для тура1 - Покупка группового тура с опциями с промокодом1
    #Цены в туре
    C_CLIENT_BASKET_TOUR1_ALL_PRICE14,
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT14,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT14,
    #Четырнадцатый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB14,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB14,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB14,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB14, 

    #Пятнадцатый кейс для тура1 - Покупка группового тура с опциями с промокодом2
    #Общие цены
    C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT15,
    C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT15,
    #Пятнадцатый кейс для тура1 в БД
    C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB15,
    #Заказ4 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB15,
    C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB15,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB15, 

    #Шестнадцатый кейс для тура1 - Покупка группового тура с комментарием
    C_CLIENT_BASKET_COMMENT2,

    #Двадцать третий кейс для тура1 - Покупка персонального тура с выбором времени в карточке тура
    CLIENT_BASKET_TOUR1_DATE_START23,
    CLIENT_BASKET_TOUR1_DATE_END23,
    #Двадцать третий для тура1 в БД
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB23,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB23,
    C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB23,

    #Двадцать четвертый кейс для тура1 - Покупка группового тура с выбором времени в карточке тура и без сверхлимита
    CLIENT_BASKET_TOUR1_DATE_START24,
    CLIENT_BASKET_TOUR1_DATE_END24,
    #Двадцать четвертый для тура1 в БД
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB24,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB24,
    

    #ВТОРОЙ ТУР (Для составного заказа)
    CLIENT_BASKET_TOUR2_BUY_ID,
    CLIENT_BASKET_TOUR2_BUY_A,
    CLIENT_BASKET_TOUR2_TITLE,
    C_CLIENT_BASKET_TOUR2_FORMAT,

    #Первый кейс для тура1 + тур2 - Покупка персонального тура c опциями+ бронирование с опциями группового
    CLIENT_BASKET_TOUR2_DATE_START1,
    CLIENT_BASKET_TOUR2_DATE_END1,
    C_CLIENT_BASKET_TOUR2_PRICE1,
    C_CLIENT_BASKET_TOUR2_OPTIONS1,
    C_CLIENT_BASKET_TOUR2_ALL_PRICE1,
    C_CLIENT_BASKET_TOUR2_ALL_PRICE2,
    #Заказ1
    C_CLIENT_BASKET2_PAYMENT_SUMMA1,
    C_CLIENT_BASKET_TOUR2_ORDER_USERID_DB1,
    C_CLIENT_BASKET_TOUR2_ORDER_SUMMA_DB1,
    #Заказ1 -#Подзаказ1
        #Уже есть у первого тура
    #Заказ1 -#Подзаказ2
    C_CLIENT_BASKET_TOUR2_SUBORDER_COMMISSION_DB1,
    C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
    C_CLIENT_BASKET_TOUR2_SUBORDER_RACEID_DB1,
    C_CLIENT_BASKET_TOUR2_SUBORDER_SUMMA_DB1,
    C_CLIENT_BASKET_TOUR2_SUBORDER_TOURS_SUMMA_DB1,
    C_CLIENT_BASKET_TOUR2_SUBORDER_OPTIONS_SUMMA_DB1,
    #Общие цены
    C_CLIENT_BASKET2_TOURS1,
    C_CLIENT_BASKET2_OPTIONS1,
    C_CLIENT_BASKET2_NUMBER_TRAVELERS1,
    C_CLIENT_BASKET2__ALL_PRICE1,

    
)


@allure.feature('Клиент')
@allure.story('Корзина: Составная покупка')
@pytest.mark.all
@pytest.mark.client
@pytest.mark.basket




class TestClientBasketComposite:

    @allure.title('Покупка персонального тура + бронирование с опциями группового')
    def test_client_basket_buy1(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, False)
        tour.change_product_status(CLIENT_BASKET_TOUR2_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR2_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        assertions.check_data_participants_ages_tourcard(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE1,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES1,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME2,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE2,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES2,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME3,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE3,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES3,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME4,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE4,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AGES4,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME5,
                                                         C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_PRICE5,
                                                        )
        assertions.check_data_participants_amount_tourcard('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.open_page(CLIENT_BASKET_TOUR2_BUY_A) 
        page.wait_for_timeout(2000)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        clientbasket.add_passengers_to_tourcard_group_booking(4)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Выбор 1й опции в составном туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_2_deployed(CLIENT_BASKET_TOUR2_TITLE,
                                                CLIENT_BASKET_TOUR2_DATE_START1,
                                                CLIENT_BASKET_TOUR2_DATE_END1,
                                                C_CLIENT_BASKET_TOUR2_FORMAT,
                                                C_CLIENT_BASKET_TOUR2_PRICE1,
                                                C_CLIENT_BASKET_TOUR2_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR2_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Развернуть составного первого тура в корзине')
        page.wait_for_timeout(500)
        assertions.check_basket_tour1_2_collapsed(CLIENT_BASKET_TOUR2_TITLE,
                                                CLIENT_BASKET_TOUR2_DATE_START1,
                                                CLIENT_BASKET_TOUR2_DATE_END1,
                                                C_CLIENT_BASKET_TOUR2_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Развернуть второго тура в корзине')
        page.wait_for_timeout(500)
        clientbasket.click_element('Выбор 1й опции в туре2 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре2 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour2_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE3
                                                )
        clientbasket.click_element('Кнопка Развернуть составного первого тура в корзине')
        page.wait_for_timeout(500)
        assertions.check_basket_tour2_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE3
                                                )       
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET2_TOURS1,
                                                C_CLIENT_BASKET2_OPTIONS1,
                                                C_CLIENT_BASKET2_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET2__ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET2_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR2_BUY_ID,
                                           C_CLIENT_BASKET_TOUR2_ORDER_USERID_DB1,
                                          C_CLIENT_BASKET_TOUR2_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR2_BUY_ID,
                                          C_CLIENT_BASKET_TOUR2_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR2_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR2_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR2_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR2_SUBORDER_OPTIONS_SUMMA_DB1,
                                          '11:11',
                                          [],
                                          5,
                                            None
                                          )
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR2_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB3,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 8374.00, 990.65, 150.73, 7232.62, 'authorized') 
        #Проверка выплаты организатору
        suborders = clientbasket.get_suborders_id_code(db_connection, CLIENT_BASKET_TOUR1_BUY_ID)
        SUBORDER_ID1 = suborders[0]['id']
        SUBORDER_CODE1 = suborders[0]['code']
        clientbasket.clear_auth_cookies(page)
        seller_auth.seller_auth(page, SELLER_LOGIN5_BASKET, SELLER_PASSWORD1)
        clientbasket.fill_element('Номер подзаказа в сводке продавца', str(SUBORDER_ID1))
        clientbasket.fill_element('Код в сводке продавца', str(SUBORDER_CODE1))
        clientbasket.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_TOAST_SUCCESS) 
        assertions_summary.check_order_operations_in_db(db_connection,
                                                         SUBORDER_ID1,
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB3,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        suborders = clientbasket.get_suborders_id_code(db_connection, CLIENT_BASKET_TOUR2_BUY_ID)
        SUBORDER_ID2 = suborders[0]['id']
        SUBORDER_CODE2 = suborders[0]['code']
        clientbasket.clear_auth_cookies(page)
        seller_auth.seller_auth(page, SELLER_LOGIN5_BASKET2, SELLER_PASSWORD1)
        clientbasket.fill_element('Номер подзаказа в сводке продавца', str(SUBORDER_ID2))
        clientbasket.fill_element('Код в сводке продавца', str(SUBORDER_CODE2))
        clientbasket.click_element('Кнопка Получить оплату в сводке продавца')
        assertions.check_toast_message('Всплывающий toast ошибки в сводке продавца', C_PAYOUT_TOAST_SUCCESS) 
        assertions_summary.check_order_operations_in_db(db_connection,
                                                         SUBORDER_ID2,
                                                         C_CLIENT_BASKET_TOUR2_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO2,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID2                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)
        tour.change_product_status(CLIENT_BASKET_TOUR2_BUY_ID,6)





 