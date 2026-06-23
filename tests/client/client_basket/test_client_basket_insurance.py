СТРАХОВКИ СЕЙЧАС УБРАНЫ


import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection 
from Locators.loc_all_directories import ALL_LOCATORS 
from Assertions.client.client_basket.assert_client_basket import AssertionsClientBasket
from pages.client.client_basket.client_basket import ClientBasket
from pages.seller.seller_auth_and_registration import SellerAuthRegistration #Можно будет поменять на SellerSummary, если методы там появятся 
from Assertions.seller.seller_summary.assert_seller_summary import AssertionsSellerSummary
from entities.tour.eni_tour import TourAPI
import allure
from Constants.const_general import URL
from Constants.client.client_auth.const_client_auth import CLIENT_PHONE1
from Constants.seller.seller_summary.const_seller_summary import C_PAYOUT_TOAST_SUCCESS 
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
    C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP
)
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
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA1,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA2,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA3,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA4,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA5,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA6,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA7,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA8,
    C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA9,
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
    

    #АЛЬФА-СТРАХОВАНИЕ
    #Сет страхуемых1
    C_CLIENT_BASKET_INSURANCE_LASTNAME1,
    C_CLIENT_BASKET_INSURANCE_NAME1,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
    C_CLIENT_BASKET_INSURANCE_BIRTH1,

    C_CLIENT_BASKET_INSURANCE_LASTNAME2,
    C_CLIENT_BASKET_INSURANCE_NAME2,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
    C_CLIENT_BASKET_INSURANCE_BIRTH2,

    C_CLIENT_BASKET_INSURANCE_LASTNAME3,
    C_CLIENT_BASKET_INSURANCE_NAME3,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
    C_CLIENT_BASKET_INSURANCE_BIRTH3,

    C_CLIENT_BASKET_INSURANCE_LASTNAME4,
    C_CLIENT_BASKET_INSURANCE_NAME4,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
    C_CLIENT_BASKET_INSURANCE_BIRTH4,

    C_CLIENT_BASKET_INSURANCE_LASTNAME5,
    C_CLIENT_BASKET_INSURANCE_NAME5,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC5,
    C_CLIENT_BASKET_INSURANCE_BIRTH5,

    C_CLIENT_BASKET_INSURANCE_LASTNAME6,
    C_CLIENT_BASKET_INSURANCE_NAME6,
    C_CLIENT_BASKET_INSURANCE_PATRONYMIC6,
    C_CLIENT_BASKET_INSURANCE_BIRTH6,

    #Кейс1 - Покупка тура со страховкой. Разные значения. Тип страховки 1. Персональный.
    C_CLIENT_BASKET_INSURANCE_DATES1,
    #Тур
    C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE1,
    C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE1,
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB1,
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB1,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB1,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
    C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
    C_CLIENT_BASKET_INSURANCE_PRICE1,
    C_CLIENT_BASKET_INSURANCE_PRICE1_2,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE1,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE1_2,

    #Корзина со страховкой кейс2 - Разные значения. Тип страховки 2. Персональный.
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB2,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_PRICE2,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE2,

#Корзина со страховкой кейс3 - Разные значения. Тип страховки 1. Групповой.
    C_CLIENT_BASKET_INSURANCE_DATES3,  
    #Тур
    C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE3,
    C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE3,
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB3,
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB3,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB3,
    C_CLIENT_BASKET__INSURANCE_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB3,
    C_CLIENT_BASKET_INSURANCE_TOURS_PRICE3,
    C_CLIENT_BASKET_INSURANCE_PRICE3,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE3_1,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE3_2,
    C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB3,
    C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB3,

    #Корзина со страховкой кейс4 - Разные значения. Тип страховки 2. Групповой.
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB4,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_PRICE4,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE4,

    #Сет страхуемых2 - Граничные значения
    C_CLIENT_BASKET_INSURANCE_BORDER_DATES1,
    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME1,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME1,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC1,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH1,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME2,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME2,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC2,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH2,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME3,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME3,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC3,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH3,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME4,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME4,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC4,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH4,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME5,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME5,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC5,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH5,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME6,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME6,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC6,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH6,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME7,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME7,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC7,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH7,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME8,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME8,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC8,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH8,

    C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME9,
    C_CLIENT_BASKET_INSURANCE_BORDER_NAME9,
    C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC9,
    C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH9,

    #Корзина со страховкой кейс5 - Граничные значения. Тип страховки 1. Персональный.
    #Тур
    C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE5,
    C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE5,
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB5,
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB5,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB5,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB5,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS5,
    C_CLIENT_BASKET_INSURANCE_TOURS_PRICE5,
    C_CLIENT_BASKET_INSURANCE_PRICE5,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE5,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE5_2,

    #Корзина со страховкой кейс6 - Граничные значения. Тип страховки 2. Персональный.
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB6,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_PRICE6,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE6,

    #Корзина со страховкой кейс7 - Граничные значения. Тип страховки 1. Групповой.
    #Тур
    C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE7,
    C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE7,
    # #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB7,
    # #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB7,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB7,
    C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB7,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS7,
    C_CLIENT_BASKET_INSURANCE_TOURS_PRICE7,
    C_CLIENT_BASKET_INSURANCE_PRICE7,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE7,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE7_2,

    #Корзина со страховкой кейс8 - Граничные значения. Тип страховки 2. Групповой.
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB8,
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_PRICE8,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE8,

    #Корзина со страховкой кейс9 - Проверка, что промокод не действует на страховку и меньше страхуемых. Разные значения. Тип страховки 1. Персональный.
    #Заказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB9,
    #Заказ1 - #Подзаказ1
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB9,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB9,
    C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_DISCOUNT_DB9, 
    #Общие цены
    C_CLIENT_BASKET_INSURANCE_PRICE9,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_1_BEFORE,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_1_AFTER,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_2_BEFORE,
    C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_2_AFTER,
)


@allure.feature('Клиент')
@allure.story('Корзина: Альфа страхование')
@pytest.mark.all
@pytest.mark.client
@pytest.mark.basket


class TestClientBasketInsurance:

    #Сброс при добавлении участников и кнопке отменить
    #Неавторизованый пользователь


    @allure.title('Покупка тура со страховкой. Разные значения. Тип страховки 1. Персональный.')
    def test_client_basket_insurance1(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        clientbasket.add_passengers_to_basket(0,1,1,2,1)
        assertions.check_data_participants_amount_basket('1','1','1','2','1')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES1)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '774') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE1
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME1,
                                                        C_CLIENT_BASKET_INSURANCE_NAME1,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH1,
                                                        1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME2,
                                                        C_CLIENT_BASKET_INSURANCE_NAME2,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME4,
                                                        C_CLIENT_BASKET_INSURANCE_NAME4,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME5,
                                                        C_CLIENT_BASKET_INSURANCE_NAME5,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC5,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME6,
                                                        C_CLIENT_BASKET_INSURANCE_NAME6,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC6,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH6,
                                                        6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '2580') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_INSURANCE_ALL_PRICE1
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1_2, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE1_2 
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA1) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 2580.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-01', '2028-03-03', 3, 2580.0, '1M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Разные значения. Тип страховки 2. Персональный.')
    def test_client_basket_insurance2(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        clientbasket.add_passengers_to_basket(0,1,1,2,1)
        assertions.check_data_participants_amount_basket('1','1','1','2','1')
        clientbasket.click_element('Тип страховки2 в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES1)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '900') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE1
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME1,
                                                        C_CLIENT_BASKET_INSURANCE_NAME1,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH1,
                                                        1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME2,
                                                        C_CLIENT_BASKET_INSURANCE_NAME2,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME4,
                                                        C_CLIENT_BASKET_INSURANCE_NAME4,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME5,
                                                        C_CLIENT_BASKET_INSURANCE_NAME5,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC5,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME6,
                                                        C_CLIENT_BASKET_INSURANCE_NAME6,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC6,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH6,
                                                        6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '3000') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_INSURANCE_ALL_PRICE1
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE2, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE2
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA2) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB2,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 3000.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-01', '2028-03-03', 3, 3000.0, '2M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB1,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Разные значения. Тип страховки 1. Групповой.')
    def test_client_basket_insurance3(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '1')
        clientbasket.add_passengers_to_basket_group(5)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '6')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES3)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '774') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE3,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE3_1
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME1,
                                                        C_CLIENT_BASKET_INSURANCE_NAME1,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH1,
                                                        1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME2,
                                                        C_CLIENT_BASKET_INSURANCE_NAME2,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME4,
                                                        C_CLIENT_BASKET_INSURANCE_NAME4,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME5,
                                                        C_CLIENT_BASKET_INSURANCE_NAME5,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC5,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME6,
                                                        C_CLIENT_BASKET_INSURANCE_NAME6,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC6,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH6,
                                                        6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '2580') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE3,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE3
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE3
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE3,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE3, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE3_2
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA3) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB3,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 2580.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-02', '2028-03-04', 3, 2580.0, '1M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB3,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Разные значения. Тип страховки 2. Групповой.')
    def test_client_basket_insurance4(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '1')
        clientbasket.add_passengers_to_basket_group(5)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '6')
        clientbasket.click_element('Тип страховки2 в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES3)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '900') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE3,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE3_1
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME1,
                                                        C_CLIENT_BASKET_INSURANCE_NAME1,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH1,
                                                        1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME2,
                                                        C_CLIENT_BASKET_INSURANCE_NAME2,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME4,
                                                        C_CLIENT_BASKET_INSURANCE_NAME4,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME5,
                                                        C_CLIENT_BASKET_INSURANCE_NAME5,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC5,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME6,
                                                        C_CLIENT_BASKET_INSURANCE_NAME6,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC6,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH6,
                                                        6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '3000') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE3,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE3
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE3
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE3,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE4, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE4
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA4) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB4,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB3,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 3000.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-02', '2028-03-04', 3, 3000.0, '2M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB3,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Разные значения. Тип страховки 1. Персональный.')
    def test_client_basket_insurance5(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        clientbasket.add_passengers_to_basket(1,2,2,2,1)
        assertions.check_data_participants_amount_basket('2','2','2','2','1')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES1)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '1161') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE5,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS5,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE5
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH1,
                                                            1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH6,
                                                            6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH7,
                                                            7)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH8,
                                                            8)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH9,
                                                            9)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '2838') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE5,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE5
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_INSURANCE_ALL_PRICE5
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE5,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE5, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS5,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE5_2 
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA5) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 2838.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-01', '2028-03-03', 3, 2838.0, '1M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB5,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Граничные значения. Тип страховки 2. Персональный.')
    def test_client_basket_insurance6(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        clientbasket.add_passengers_to_basket(1,2,2,2,1)
        assertions.check_data_participants_amount_basket('2','2','2','2','1')
        clientbasket.click_element('Тип страховки2 в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES1)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '1350') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE5,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS5,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE5
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH1,
                                                            1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH6,
                                                            6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH7,
                                                            7)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH8,
                                                            8)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH9,
                                                            9)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '3300') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE5,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE5
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_INSURANCE_ALL_PRICE5
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE5,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE6, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS5,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE6
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA6) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB6,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB5,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 3300.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-01', '2028-03-03', 3, 3300.0, '2M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB5,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Граничные значения. Тип страховки 1. Групповой.')
    def test_client_basket_insurance7(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '1')
        clientbasket.add_passengers_to_basket_group(8)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '9')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES3)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '1161') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE7,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS7,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE7
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH1,
                                                            1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH6,
                                                            6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH7,
                                                            7)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH8,
                                                            8)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH9,
                                                            9)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '3483') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE7,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE7
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE7
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE7,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE7, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS7,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE7_2
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA7) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB7,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB7,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB7,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB7,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 3483.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-02', '2028-03-04', 3, 3483.0, '1M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB7,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Покупка тура со страховкой. Граничные значения. Тип страховки 2. Групповой.')
    def test_client_basket_insurance8(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Вторая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '1')
        clientbasket.add_passengers_to_basket_group(8)
        assertions.check_data_participants_ages_basket_group(C_CLIENT_TOUR_CARD_SELECT_PARTICIPANTS_NAME_GROUP, '9')
        clientbasket.click_element('Тип страховки2 в туре1 в корзине')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES3)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '1350') 
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE7,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS7,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE7
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC1,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH1,
                                                            1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC2,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC4,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC5,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH5,
                                                        5)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC6,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH6,
                                                            6)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC7,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH7,
                                                            7)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC8,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH8,
                                                            8)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_BORDER_LASTNAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_NAME9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_PATRONYMIC9,
                                                            C_CLIENT_BASKET_INSURANCE_BORDER_BIRTH9,
                                                            9)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '4050') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START2,
                                                CLIENT_BASKET_TOUR1_DATE_END2,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE7,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE7
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START2,
                                        CLIENT_BASKET_TOUR1_DATE_END2,
                                        C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE7
                                        )
        assertions.check_basket_tour1_all_price_block(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE7,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE8, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS7,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE8
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA8) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB8,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB2,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB7,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB7,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TOURS_DISCOUNT_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_PARTICIPANTS_DB3,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB7,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 4050.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-02', '2028-03-04', 3, 4050.0, '2M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB7,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)

    @allure.title('Проверка, что промокод не действует на страховку и меньше страхуемых. Разные значения. Тип страховки 1. Персональный.')
    def test_client_basket_insurance9(self, page: Page, db_connection): 
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
        clientbasket.click_element_by_class_part('_datepicker')
        page.wait_for_timeout(1000)
        clientbasket.click_element('Первая дата тура1 в карточке тура клиента')
        clientbasket.click_element('Кнопка Принять в датапикере в карточке тура клиента')
        clientbasket.click_element('Кнопка Купить в карточке тура клиента')
        clientbasket.click_element('Кнопка Корзина у авторизованного пользователя из тура')
        assertions.check_data_participants_amount_basket('1','0','0','0','0')
        clientbasket.add_passengers_to_basket(0,1,1,2,1)
        assertions.check_data_participants_amount_basket('1','1','1','2','1')
        clientbasket.fill_element('Поле ввода промокода в корзине', C_CLIENT_BASKET_PROMOCODE1)
        clientbasket.click_element('Кнопка Применить промокод в корзине')
        page.wait_for_timeout(1500)
        assertions.check_field_value_from_locator('Даты страховки в туре1 в корзине', C_CLIENT_BASKET_INSURANCE_DATES1)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '774') 
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE1,
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_1_BEFORE,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_1_AFTER
                                                     )
        clientbasket.click_element('Кнопка Добавить в страховке в туре1 в корзине')
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME1,
                                                        C_CLIENT_BASKET_INSURANCE_NAME1,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC1,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH1,
                                                        1)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME2,
                                                        C_CLIENT_BASKET_INSURANCE_NAME2,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC2,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH2,
                                                        2)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME3,
                                                        C_CLIENT_BASKET_INSURANCE_NAME3,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC3,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH3,
                                                        3)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        clientbasket.client_add_client_insurance_basket(page, C_CLIENT_BASKET_INSURANCE_LASTNAME4,
                                                        C_CLIENT_BASKET_INSURANCE_NAME4,
                                                        C_CLIENT_BASKET_INSURANCE_PATRONYMIC4,
                                                        C_CLIENT_BASKET_INSURANCE_BIRTH4,
                                                        4)
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        clientbasket.click_element('Кнопка Далее в страховке в туре1 в корзине')
        page.wait_for_timeout(2000)
        assertions.check_field_value_from_locator('Цена страховки в туре1 в корзине', '1548') 
        assertions.check_basket_tour1_deployed(CLIENT_BASKET_TOUR1_TITLE,
                                                CLIENT_BASKET_TOUR1_DATE_START1,
                                                CLIENT_BASKET_TOUR1_DATE_END1,
                                                C_CLIENT_BASKET_TOUR1_FORMAT,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_PRICE1,
                                                C_CLIENT_BASKET_TOUR1_OPTIONS1,
                                                C_CLIENT_BASKET_INSURANCE_TOUR1_ALL_PRICE1
                                                )
        clientbasket.click_element('Кнопка Развернуть/Свернуть первого тура в корзине')
        assertions.check_basket_tour1_collapsed(CLIENT_BASKET_TOUR1_TITLE,
                                        CLIENT_BASKET_TOUR1_DATE_START1,
                                        CLIENT_BASKET_TOUR1_DATE_END1,
                                        C_CLIENT_BASKET_INSURANCE_ALL_PRICE1
                                        )
        assertions.check_basket_tour1_all_price_block_with_promocode(C_CLIENT_BASKET_INSURANCE_TOURS_PRICE1,
                                                      C_CLIENT_BASKET_OPTIONS1,
                                                      C_CLIENT_BASKET_INSURANCE_PRICE9, 
                                                      C_CLIENT_BASKET_INSURANCE_NUMBER_TRAVELERS1,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_2_BEFORE,
                                                      C_CLIENT_BASKET_INSURANCE_ALL_PRICE9_2_AFTER
                                                     )
        clientbasket.click_element('Кнопка Оплатить картой в корзине')
        assertions.check_url(YOUR_PAYMENT_URL)
        assertions.check_field_value_from_locator('Сумма в твоих платежах', C_CLIENT_BASKET3_INSURANCE_PAYMENT_SUMMA9) 
        assertions.check_last_order_in_db(db_connection, CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_ORDER_USERID_DB,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_ORDER_SUMMA_DB9,
                                          C_CLIENT_BASKET_TOUR1_ORDER_STATUS1_DB1,
                                          None,
                                          CLIENT_BASKET_TOUR1_BUY_ID,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_RACEID_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TYPE_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_COMMISSION_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB9,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS1_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_SUMMA_DB9,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_TOURS_DISCOUNT_DB9,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_OPTIONS_SUMMA_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_TIME_DB1,
                                          C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_PARTICIPANTS_DB1,
                                          C_CLIENT_BASKET_TOUR1_SUBORDER_NUMBER_TRAVELERS_DB1,
                                          None
                                          )
        ORDER_ID = assertions.check_insurance_in_last_order(db_connection, 1548.00)
        assertions.check_insurance_data_in_db(db_connection, ORDER_ID, '2028-03-01', '2028-03-03', 3, 1548.0, '1M', 0)
        clientbasket.successful_payment()
        assertions.check_page_successful_payment(C_CLIENT_SUCCESSUFUL_PAYMENT_TITLE,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_DESCRIPTION,
                                                 C_CLIENT_SUCCESSUFUL_PAYMENT_BUTTON)
        assertions.check_order_statuses_in_db(db_connection, C_CLIENT_BASKET_TOUR1_ORDER_STATUS2_DB1, C_CLIENT_BASKET_TOUR1_SUBORDER_STATUS2_DB1) 
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
                                                         C_CLIENT_BASKET_INSURANCE_TOUR1_SUBORDER_SUMMA_DB9,
                                                         C_PAYOUT_STATUS1,
                                                         C_PAYOUT_INFO1,
                                                         C_PAYOUT_TYPE5,
                                                         C_PAYOUT_OPERATOR_ID1                                                  
                                                         )
        tour.change_product_status(CLIENT_BASKET_TOUR1_BUY_ID,6)