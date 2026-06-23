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
    C_PAYOUT_OPERATOR_ID1
)
from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN5_BASKET,
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
from Constants.seller.seller_summary.const_seller_summary import C_PAYOUT_TOAST_SUCCESS 
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
    C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
    
)


@allure.feature('Клиент')
@allure.story('Корзина: Покупка одного тура')
@pytest.mark.all
@pytest.mark.client
@pytest.mark.basket


class TestClientBasketBooking:

#Тест на автоподстановку из браузера для неавторизованного не получилось сделать
#Добавить проверку уменьшения свободных мест, как будет сделана


    @allure.title('Бронирование. Покупка персонального тура')
    def test_client_basket_booking1(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
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
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3774.00, 384.95, 67.93, 3321.12, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура')
    def test_client_booking_booking2(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 12000.00, 1224, 216, 10560, 'authorized')
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура с опциями')
    def test_client_booking_booking3(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE3
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE3
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS3,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE3
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA3)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3824, 390.05, 68.83, 3365.12, 'authorized')
        # #Проверка выплаты организатору 
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
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура с опциями')
    def test_client_booking_booking4(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS4,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE4
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE4
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS4,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE4
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA4)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB4,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB4,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB4,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB4,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 12050, 1229.1, 216.9, 10604, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB4,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура c промокодом1')
    def test_client_booking_booking5(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1000)
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE1)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT5,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT5
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA5)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB5,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB5,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3509.82, 125.52, 63.18, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB5,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура c промокодом2')
    def test_client_booking_booking6(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1000)
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE2)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT6,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT6
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA6)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB6,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB6,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB6,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB6,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB6,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3674.00, 286.75, 66.13, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB6,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура c сменой количества уч.')
    def test_client_booking_booking7(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(1,2,2,2,2)
        assertions.check_data_participants_amount_tourcard_booking('2','2','2','2','2')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('10 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE5)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE7,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE7
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('2','2','2','2','2')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE7
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS7,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS7, 
                                                C_CLIENT_BASKET_ALL_PRICE7
                                                )
        clientbasket.add_passengers_to_basket(1,1,1,1,1)
        clientbasket.minus_passengers_to_basket(2,3,3,3,3)
        clientbasket.add_passengers_to_basket(0,2,3,4,5)
        page.wait_for_timeout(500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                        )
        page.wait_for_timeout(500)
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA7)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3774.00, 384.95, 67.93, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура с опциями c с промокодом1')
    def test_client_booking_booking8(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE1)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE8
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE8
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS3,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT8,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT8
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA8)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB8,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB5,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB8,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB8,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB8,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3556.32, 127.19, 64.01, 3365.12, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB8,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура с опциями c с промокодом2')
    def test_client_booking_booking9(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE2)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE8
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE8
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS3,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT9,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT9
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA9)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB9,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_PROCODEID_DB6,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB9,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB9,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB9,
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
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3724.00, 291.85, 67.03, 3365.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB9,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура с комментарием')
    def test_client_booking_booking10(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
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
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        clientbasket.fill_element('Комментарий в корзине', C_CLIENT_BASKET_COMMENT)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          C_CLIENT_BASKET_COMMENT
                                          )
        
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3774.00, 384.95, 67.93, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура с промокодом1')
    def test_client_booking_booking11(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE1)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT11,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT11
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA11)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB11,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB11,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB11,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB11,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 11160.00, 399.12, 200.88, 10560.00, 'authorized')
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB11,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура с промокодом2')
    def test_client_booking_booking12(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE2)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT12,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT12
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA12)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB12,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB12,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB12,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB12,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 11900.00, 1125.80, 214.20, 10560.00, 'authorized')
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB12,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового c изменением количества уч.')
    def test_client_booking_booking13(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                                C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        clientbasket.minus_passengers_to_basket_group(2)
        clientbasket.add_passengers_to_basket_group(12)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '13')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_TOUR1_FORMAT,
                                        C_CLIENT_BASKET_TOUR1_PRICE13,
                                        C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                        C_CLIENT_BASKET_TOUR1_ALL_PRICE13
                                        )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        page.wait_for_timeout(500)
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_TOUR1_ALL_PRICE13
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS13,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS13, 
                                                C_CLIENT_BASKET_ALL_PRICE13
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA13)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB13,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB13,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB13,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB13,
                                            None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 62000.00, 6324, 1116, 54560, 'authorized')
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB14,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура с опциями с промокодом1')
    def test_client_booking_booking14(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE1)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE14
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE14
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS3,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT14,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT14
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA14)
        ORDER_UUID = (db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB14,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB14,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB14,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB14,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB3,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1)
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 11206.50, 400.78, 201.72, 10604, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB14,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)
    
    @allure.title('Бронирование. Покупка группового тура с опциями с промокодом2')
    def test_client_booking_booking15(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        clientbasket.click_element('Выбор 1й опции в туре1 в корзине')
        clientbasket.click_element('Выбор 2й опции в туре1 в корзине')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE2)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS3,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE14
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE14
                                                )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS3,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2,
                                                C_CLIENT_BASKET_ALL_PRICE_BEFORE_DISCOUNT15,
                                                C_CLIENT_BASKET_ALL_PRICE_AFTER_DISCOUNT15
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA15)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB15,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB15,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB15,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB15,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB3,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 11950.00, 1130.90, 215.10, 10604, 'authorized')
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB15,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура с комментарием')
    def test_client_booking_booking16(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.fill_element('Комментарий в корзине', C_CLIENT_BASKET_COMMENT2)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                        C_CLIENT_BASKET_COMMENT2
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1)
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 12000.00, 1224, 216, 10560, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)        

    @allure.title('Бронирование. Неавторизованный пользователь. Покупка персонального')
    def test_client_booking_booking17(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page)
        seller_auth = SellerAuthRegistration(page) 
        assertions_summary = AssertionsSellerSummary(page) 
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        assertions.check_data_datapicker_tourcard_no_auth_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_no_auth_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента неавторизован бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента неавторизован бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_no_auth_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента неавторизован бронирование')
        assertions.check_data_participants_ages_tourcard_no_auth_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_no_auth_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_no_auth_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_no_auth_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента неавторизован бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_no_auth_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента неавторизован бронирование')
        clientbasket.client_auth_tour_card(db_connection,CLIENT_PHONE1)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Неавторизованный пользователь. Покупка группового')
    def test_client_booking_booking18(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) 
        assertions_summary = AssertionsSellerSummary(page) 
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_no_auth_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_no_auth_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура2 в карточке тура клиента неавторизован бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента неавторизован бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_no_auth_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента неавторизован бронирование')
        assertions.check_data_participants_amount_tourcard_group_no_auth_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_no_auth_booking(2)
        assertions.check_data_participants_amount_tourcard_group_no_auth_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента неавторизован бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_no_auth_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента неавторизован бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента неавторизован бронирование')
        clientbasket.client_auth_tour_card(db_connection,CLIENT_PHONE1)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Неавторизованный пользователь. Вход в корзине. Покупка персонального')
    def test_client_booking_booking19(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('кнопка Профиль из карточки тура')
        clientbasket.click_element('кнопка Выйти бронирование')
        page.wait_for_timeout(2000)
        clientbasket.open_page(BASKET_PAGE_URL)
        page.wait_for_timeout(1000)
        clientbasket.fill_main_traveller_noauth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_PHONE,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)
        assertions.check_basket_tour1_deployed_no_auth(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket_no_auth(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket_no_auth('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине неавторизован')
        assertions.check_basket_tour1_collapsed_no_auth(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block_no_auth(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине неавторизован')
        clientbasket.client_confirm_phone_basket_enter(db_connection, CLIENT_PHONE1)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
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
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Неавторизованный пользователь. Вход в корзине. Покупка группового')
    def test_client_booking_booking20(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('кнопка Профиль из карточки тура')
        clientbasket.click_element('кнопка Выйти бронирование')
        page.wait_for_timeout(2000)
        clientbasket.open_page(BASKET_PAGE_URL)
        page.wait_for_timeout(1000)
        clientbasket.fill_main_traveller_noauth(C_CLIENT_BASKET_LASTNAME,
                                         C_CLIENT_BASKET_NAME,
                                         C_CLIENT_BASKET_PATRONYMIC,
                                         C_CLIENT_BASKET_PHONE,
                                         C_CLIENT_BASKET_EMAIL,
                                         C_CLIENT_BASKET_DATE_BORN,)
        assertions.check_basket_tour1_deployed_no_auth(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group_no_auth(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине неавторизован')
        assertions.check_basket_tour1_collapsed_no_auth(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block_no_auth(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине неавторизован')
        clientbasket.client_confirm_phone_basket_enter(db_connection, CLIENT_PHONE1)
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Смена дат в корзине. Из персональной в групповую')
    def test_client_booking_booking21(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
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
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        clientbasket.click_element('Датапикер в туре1 в корзине')
        clientbasket.click_element('Дата2 в датапикере в туре1 в корзине')
        clientbasket.click_element('Применить в датапикере в туре1 в корзине')
        page.wait_for_timeout(1000)
        clientbasket.add_passengers_to_basket_group(2)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1, # Это обход бага, тут должен быть пустой prices
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1)
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 12000.00, 1224, 216, 10560, 'authorized') 
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Смена дат в корзине. Из группового в персональный')
    def test_client_booking_booking22(self, page: Page, db_connection ):  
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE3)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE2)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')   
        clientbasket.click_element('Датапикер в туре1 в корзине')
        clientbasket.click_element('Дата1 в датапикере в туре1 в корзине')
        clientbasket.click_element('Применить в датапикере в туре1 в корзине')
        page.wait_for_timeout(1000)
        clientbasket.add_passengers_to_basket(0,2,3,4,5)
        page.wait_for_timeout(1000)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2, # Это обход бага, тут должен быть пустой NUMBER_TRAVELERS
                                            None
                                          )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3774.00, 384.95, 67.93, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка персонального тура с выбором времени в карточке тура')
    def test_client_booking_booking23(self, page: Page, db_connection ):  
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Четвертая дата тура1 в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        clientbasket.click_element('Время4 тура1 в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента с временем бронирование')
        page.wait_for_timeout(1000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE3)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_ages_tourcard_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_tourcard_booking('1','0','0','0','0')
        clientbasket.add_passengers_to_tourcard_booking(0,2,3,4,5)
        assertions.check_data_participants_amount_tourcard_booking('1','2','3','4','5')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('15 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE2)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START23,
                                                CLIENT_BASKET_TOUR1_DATE_END23,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_data_participants_ages_basket(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME1,
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
        assertions.check_data_participants_amount_basket('1','2','3','4','5')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START23,
                                                CLIENT_BASKET_TOUR1_DATE_END23,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE1
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS1,
                                                C_CLIENT_BASKET_OPTIONS1,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS1, 
                                                C_CLIENT_BASKET_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA1)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                           C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB23,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB23,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB23,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 3774.00, 384.95, 67.93, 3321.12, 'authorized')
        # #Проверка выплаты организатору 
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
                                                         C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Бронирование. Покупка группового тура')
    def test_client_booking_booking24(self, page: Page, db_connection ): 
        assertions = AssertionsClientBasket(page) 
        clientbasket = ClientBasket(page) 
        seller_auth = SellerAuthRegistration(page) #Можно будет поменять на SellerSummary, если методы там появятся 
        assertions_summary = AssertionsSellerSummary(page)
        tour = TourAPI()
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,5)
        tour.change_product_booking(db_connection, CLIENT_BASKET_TOUR1_TITLE, True)
        clientbasket.client_auth(db_connection,CLIENT_PHONE1) 
        page.wait_for_timeout(500)
        clientbasket.save_auth_cookies(page)
        clientbasket.open_page(CLIENT_BASKET_TOUR1_BUY_A) 
        page.wait_for_timeout(2000)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE1_NOTIME)
        assertions.check_number_participants_rolled_booking('1 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE1)
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Пятая дата тура1 в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        clientbasket.click_element('Время4 тура1 в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента с временем бронирование')
        page.wait_for_timeout(500)
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE6)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        assertions.check_data_datapicker_tourcard_booking(C_CLIENT_TOUR_CARD_DATAPICKER_DATE4)
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP,
                                                               C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_AMOUNT_GROUP )
        clientbasket.add_passengers_to_tourcard_group_booking(2)
        assertions.check_data_participants_amount_tourcard_group_booking(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Выбор участников в карточке тура клиента бронирование')
        page.wait_for_timeout(500)
        assertions.check_number_participants_rolled_booking('3 чел')
        assertions.check_field_value_from_locator('Цена кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_PRICE_BUTTON_VALUE4)
        assertions.check_field_value_from_locator('Количество участников кнопки Купить в карточке тура клиента бронирование', C_CLIENT_TOUR_CARD_GROUP_AMOUNT1)
        clientbasket.click_element('Кнопка Купить в карточке тура клиента бронирование')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        page.wait_for_timeout(1500)
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START24,
                                                CLIENT_BASKET_TOUR1_DATE_END24,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_TOUR1_PRICE2,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '3')
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START24,
                                                CLIENT_BASKET_TOUR1_DATE_END24,
                                                C_CLIENT_BASKET_TOUR1_ALL_PRICE2
                                                )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_TOURS2,
                                                C_CLIENT_BASKET_OPTIONS2,
                                                C_CLIENT_BASKET_NUMBER_TRAVELERS2, 
                                                C_CLIENT_BASKET_ALL_PRICE2
                                                )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET_PAYMENT_SUMMA2)
        ORDER_UUID = assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                        C_CLIENT_BASKET_TOUR1_ORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                        None,
                                        CLIENT_BASKET_TOUR1_BUY_ID,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB24,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_SUMMA_DB2,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB24,
                                        [],
                                        C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB2,
                                          None
                                        )
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1)
        assertions.check_payment_in_db(db_connection, ORDER_UUID, 'card', 12000.00, 1224, 216, 10560, 'authorized')  
        # #Проверка выплаты организатору 
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
                                                        C_CLIENT_BASKET_TOUR1_SUBORDER_SUMMA_DB2,
                                                        C_PAYOUT_STATUS1,
                                                        C_PAYOUT_INFO1,
                                                        C_PAYOUT_TYPE5,
                                                        C_PAYOUT_OPERATOR_ID1                                                  
                                                        )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)