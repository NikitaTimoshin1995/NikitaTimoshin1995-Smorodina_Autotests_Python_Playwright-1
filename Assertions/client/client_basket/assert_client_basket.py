
import allure
from Assertions.client.client_tour_card.assert_client_tour_card import AssertionsClientTourCard
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS
import time
from typing import Optional

class AssertionsClientBasket(AssertionsClientTourCard):
    #ОБЩЕЕ
    @allure.step('Проверка последнего заказа в базе данных')
    def check_last_order_in_db(self, db_connection, product_id, expected_user_id=None, expected_summa=None, 
                            expected_status_id=None, expected_promocode_id=None, expected_tour_id=None, 
                            expected_race_id=None, expected_order_type=None, expected_commission_value=None, 
                            expected_summa_ot=None, expected_status_id_ot=None, expected_price_tour=None, 
                            expected_discount=None, expected_price_options=None, expected_start_time=None,
                            expected_price_ids=None, expected_number_travelers=None, expected_comment=None,
                            check_doc_travel_pdf=True):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
        last_order = cursor.fetchone()
        assert last_order is not None, "Не найдено ни одного заказа в базе данных"
        order_id = last_order[0]
        cursor.execute("""
            SELECT user_id, summa, status_id, promocode_id, comment, doc_travel_pdf, uuid 
            FROM orders WHERE id = %s
        """, (order_id,))
        order_data = cursor.fetchone()
        assert order_data is not None, f"Заказ с ID {order_id} не найден в базе данных"
        user_id, summa, status_id, promocode_id, comment, doc_travel_pdf, uuid = order_data
        if expected_user_id is not None:
            assert user_id == expected_user_id, f"user_id не совпадает. Ожидалось: {expected_user_id}, но получено: {user_id}"
        if expected_summa is not None:
            expected_summa_float = float(expected_summa)
            summa_float = float(summa)
            assert summa_float == expected_summa_float, f"summa не совпадает. Ожидалось: {expected_summa:.2f}, но получено: {summa:.2f}"
        if expected_status_id is not None:
            assert status_id == expected_status_id, f"status_id не совпадает. Ожидалось: {expected_status_id}, но получено: {status_id}"
        if expected_promocode_id is not None:
            assert promocode_id == expected_promocode_id, f"promocode_id не совпадает. Ожидалось: {expected_promocode_id}, но получено: {promocode_id}"
        if expected_comment is not None:
            assert comment == expected_comment, f"comment не совпадает. Ожидалось: {expected_comment}, но получено: {comment}"
        if check_doc_travel_pdf:
            assert doc_travel_pdf is not None, f"doc_travel_pdf для заказа ID {order_id} равен NULL"
        cursor.execute("""
            SELECT tour_id, race_id, order_type, commission_value, summa, status_id, 
                price_tour, discount, price_options, start_time, price_ids, number_travelers 
            FROM order_tours WHERE order_id = %s and tour_id=%s
        """, (order_id, product_id))   
        order_tour_data = cursor.fetchone()
        assert order_tour_data is not None, f"Данные order_tours для заказа ID {order_id} не найдены"
        tour_id, race_id, order_type, commission_value, summa_ot, status_id_ot, price_tour, discount, price_options, start_time, price_ids, number_travelers = order_tour_data
        if expected_tour_id is not None:
            assert tour_id == expected_tour_id, f"tour_id не совпадает. Ожидалось: {expected_tour_id}, но получено: {tour_id}"
        if expected_race_id is not None:
            assert race_id == expected_race_id, f"race_id не совпадает. Ожидалось: {expected_race_id}, но получено: {race_id}"
        if expected_order_type is not None:
            assert order_type == expected_order_type, f"order_type не совпадает. Ожидалось: {expected_order_type}, но получено: {order_type}"
        if expected_commission_value is not None:
            assert commission_value == expected_commission_value, f"commission_value не совпадает. Ожидалось: {expected_commission_value}, но получено: {commission_value}"
        if expected_summa_ot is not None:
            expected_summa_ot_float = float(expected_summa_ot)  
            summa_ot_float = float(summa_ot)  
            assert summa_ot_float == expected_summa_ot_float, f"summa в order_tours не совпадает. Ожидалось: {expected_summa_ot:.2f}, но получено: {summa_ot:.2f}"  
        if expected_status_id_ot is not None:
            assert status_id_ot == expected_status_id_ot, f"status_id в order_tours не совпадает. Ожидалось: {expected_status_id_ot}, но получено: {status_id_ot}"
        if expected_price_tour is not None:
            expected_price_tour_float = float(expected_price_tour)  
            price_tour_float = float(price_tour)  
            assert price_tour_float == expected_price_tour_float, f"price_tour не совпадает. Ожидалось: {expected_price_tour:.2f}, но получено: {price_tour:.2f}"  
        if expected_discount is not None:
            expected_discount_float = float(expected_discount)  
            discount_float = float(discount)  
            assert discount_float == expected_discount_float, f"discount не совпадает. Ожидалось: {expected_discount:.2f}, но получено: {discount:.2f}"  
        if expected_price_options is not None:
            assert price_options == expected_price_options, f"price_options не совпадает. Ожидалось: {expected_price_options}, но получено: {price_options}"
        if expected_start_time is not None:
            assert start_time == expected_start_time, f"start_time не совпадает. Ожидалось: {expected_start_time}, но получено: {start_time}"
        if expected_price_ids is not None:
            assert price_ids == expected_price_ids, f"price_ids не совпадает. Ожидалось: {expected_price_ids}, но получено: {price_ids}"
        if expected_number_travelers is not None:
            assert number_travelers == expected_number_travelers, f"number_travelers не совпадает. Ожидалось: {expected_number_travelers}, но получено: {number_travelers}" 
        cursor.close()
        return uuid


    @allure.step('Проверка страховки в последнем заказе')
    def check_insurance_in_last_order(self, db_connection, expected_insurance):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
        last_order = cursor.fetchone()
        assert last_order is not None, "Не найдено ни одного заказа в базе данных"
        order_id = last_order[0]
        cursor.execute("SELECT summa_insurance FROM orders WHERE id = %s", (order_id,))
        order_data = cursor.fetchone()
        assert order_data is not None, f"Заказ с ID {order_id} не найден в базе данных"
        actual_insurance = order_data[0]
        assert actual_insurance == expected_insurance, f"summa_insurance не совпадает. Ожидалось: {expected_insurance}, но получено: {actual_insurance}"
        cursor.close()
        return order_id
    

    @allure.step('Проверка данных страховки в базе данных')
    def check_insurance_data_in_db(self, db_connection, order_id, start_date=None, end_date=None, number_days=None,
                                price=None, insurance_type=None, status=None):
        cursor = db_connection.cursor()
        cursor.execute("SELECT policy_period_from, policy_period_till, multi_days, prem_rur, struh_sum_type, status_id FROM order_insurances WHERE order_id = %s", (order_id,))
        insurance_data = cursor.fetchone()
        assert insurance_data is not None, f"Страховка для заказа ID {order_id} не найдена в базе данных"
        actual_start_date, actual_end_date, actual_number_days, actual_price, actual_insurance_type, actual_status = insurance_data
        if start_date is not None:
            assert str(actual_start_date) == start_date, f"policy_period_from не совпадает. Ожидалось: {start_date}, но получено: {actual_start_date}"
        if end_date is not None:
            assert str(actual_end_date) == end_date, f"policy_period_till не совпадает. Ожидалось: {end_date}, но получено: {actual_end_date}"
        if number_days is not None:
            assert actual_number_days == number_days, f"multi_days не совпадает. Ожидалось: {number_days}, но получено: {actual_number_days}"
        if price is not None:
            if isinstance(actual_price, float) and isinstance(price, float):
                assert abs(actual_price - price) < 0.01, f"prem_rur не совпадает. Ожидалось: {price}, но получено: {actual_price}"
            else:
                assert actual_price == price, f"prem_rur не совпадает. Ожидалось: {price}, но получено: {actual_price}"
        if insurance_type is not None:
            assert actual_insurance_type == insurance_type, f"struh_sum_type не совпадает. Ожидалось: {insurance_type}, но получено: {actual_insurance_type}"
        if status is not None:
            assert actual_status == status, f"status_id не совпадает. Ожидалось: {status}, но получено: {actual_status}"
        cursor.close()


    @allure.step('Проверка статусов заказа и подзаказа в базе данных с повторными попытками')
    def check_order_statuses_in_db(self, db_connection, expected_order_status: int, expected_suborder_status: int):
        max_attempts = 15
        attempt = 1
        last_error = None
        while attempt <= max_attempts:
            try:
                cursor = db_connection.cursor()
                cursor.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
                last_order = cursor.fetchone()
                assert last_order is not None, "Не найдено ни одного заказа в базе данных"
                order_id = last_order[0]
                cursor.execute("SELECT status_id FROM orders WHERE id = %s", (order_id,))
                order_status_result = cursor.fetchone()
                assert order_status_result is not None, f"Заказ с ID {order_id} не найден"
                actual_order_status = order_status_result[0]
                assert actual_order_status == expected_order_status, f"Статус заказа не совпадает. Ожидалось: {expected_order_status}, но получено: {actual_order_status}"
                cursor.execute("SELECT status_id FROM order_tours WHERE order_id = %s", (order_id,))
                suborder_status_results = cursor.fetchall()
                assert len(suborder_status_results) > 0, f"Подзаказы для заказа ID {order_id} не найдены"
                problematic_suborders = []
                for status_id, in suborder_status_results:
                    if status_id != expected_suborder_status:
                        problematic_suborders.append(f"статус: {status_id}")
                if problematic_suborders:
                    error_msg = f"Найдены подзаказы с некорректным статусом. Ожидалось: {expected_suborder_status}. Проблемные подзаказы: {', '.join(problematic_suborders)}. Всего подзаказов: {len(suborder_status_results)}"
                    raise AssertionError(error_msg)
                cursor.close()
                return
            except AssertionError as e:
                last_error = str(e)
                cursor.close()
                if attempt == max_attempts:
                    break
                time.sleep(10)
                attempt += 1
        raise AssertionError(f"Проверка не пройдена после {max_attempts} попыток с интервалом 10 секунд. Последняя ошибка: {last_error}")
    

    @allure.step("Проверка страницы успешной оплаты")
    def check_page_successful_payment(self, title: str, description: str, button_text: str):
        self.check_field_value_from_locator('Заголовок на странице успешной оплаты', title)
        self.check_field_value_from_locator('Описание на странице успешной оплаты', description)
        self.check_field_value_from_locator('Кнопка на странице успешной оплаты', button_text)


    #АВТОРИЗОВАН
    @allure.step("Проверка элементов пустой корзины")
    def check_empty_basket(self, expected_my_basket, expected_empty_here, expected_description):
        self.check_field_value_from_locator('Заголовок в пустой корзине клиента', expected_my_basket)
        self.check_field_value_from_locator('Подзаголовок в пустой корзине клиента', expected_empty_here)
        self.check_field_value_from_locator('Описание в пустой корзине клиента', expected_description)


    @allure.step("Проверка первого тура в свернутом состоянии")
    def check_basket_tour1_collapsed(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок первого тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала первого тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания первого тура в корзине', end_date)
        self.check_field_value_from_locator('Общая цена первого тура в корзине', all_price)


    @allure.step("Проверка первого тура в развернутом состоянии")
    def check_basket_tour1_deployed(self, title: str, start_date: str, end_date: str, format: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок первого тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала первого тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания первого тура в корзине', end_date)
        self.check_field_value_from_locator('Формат первого тура в корзине', format)
        self.check_field_value_from_locator('Цена первого тура в корзине', price)
        self.check_field_value_from_locator('Цена опций первого тура в корзине', options)
        self.check_field_value_from_locator('Общая цена первого тура в корзине', all_price)


    @allure.step("Проверка категорий возрастов в корзине")
    def check_data_participants_ages_basket(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в корзине', category1)
        self.check_field_value_from_locator('Цена возраст1 в корзине', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в корзине', ages1)
        self.check_field_value_from_locator('Название возраст2 в корзине', category2)
        self.check_field_value_from_locator('Цена возраст2 в корзине', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в корзине', ages2)
        self.check_field_value_from_locator('Название возраст3 в корзине', category3)
        self.check_field_value_from_locator('Цена возраст3 в корзине', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в корзине', ages3)
        self.check_field_value_from_locator('Название возраст4 в корзине', category4)
        self.check_field_value_from_locator('Цена возраст4 в корзине', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в корзине', ages4)
        self.check_field_value_from_locator('Название возраст5 в корзине', category5)
        self.check_field_value_from_locator('Цена возраст5 в корзине', price5)


    @allure.step("Проверка количества участников разных возрастов в корзине")
    def check_data_participants_amount_basket(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в корзине', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в корзине', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в корзине', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в корзине', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в корзине', participants_number5)


    @allure.step("Проверка категорий возрастов в корзине группового")
    def check_data_participants_ages_basket_group(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в корзине', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в корзине', participants_number)

    #Составной
    @allure.step("Проверка составного первого тура в свернутом состоянии")
    def check_basket_tour1_2_collapsed(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок составного первого тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала составного первого тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания составного первого тура в корзине', end_date)
        self.check_field_value_from_locator('Общая цена составного первого тура в корзине', all_price)


    @allure.step("Проверка составного первого тура в развернутом состоянии")
    def check_basket_tour1_2_deployed(self, title: str, start_date: str, end_date: str, format: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок составного первого тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала составного первого тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания составного первого тура в корзине', end_date)
        self.check_field_value_from_locator('Формат составного первого тура в корзине', format)
        self.check_field_value_from_locator('Цена составного первого тура в корзине', price)
        self.check_field_value_from_locator('Цена опций составного первого тура в корзине', options)
        self.check_field_value_from_locator('Общая цена составного первого тура в корзине', all_price)


    @allure.step("Проверка составного второго тура в свернутом состоянии")
    def check_basket_tour2_collapsed(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок второго тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала второго тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания второго тура в корзине', end_date)
        self.check_field_value_from_locator('Общая цена второго тура в корзине', all_price)


    @allure.step("Проверка составного второго тура в развернутом состоянии")
    def check_basket_tour2_deployed(self, title: str, start_date: str, end_date: str, format: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок второго тура в корзине', title)
        self.check_field_value_from_locator('Дата и время начала второго тура в корзине', start_date)
        self.check_field_value_from_locator('Дата окончания второго тура в корзине', end_date)
        self.check_field_value_from_locator('Формат второго тура в корзине', format)
        self.check_field_value_from_locator('Цена второго тура в корзине', price)
        self.check_field_value_from_locator('Цена опций второго тура в корзине', options)
        self.check_field_value_from_locator('Общая цена второго тура в корзине', all_price)


    @allure.step("Проверка общих цен")
    def check_basket_tour1_all_price_block(self, price: str, options: str, number_travelers: str, all_price): 
        self.check_field_value_from_locator('Цена всех туров в корзине', price)
        self.check_field_value_from_locator('Цена всех опций в корзине', options)
        # self.check_field_value_from_locator('Страховка в общих ценах с туром 1', insurance) #Страховка
        self.check_field_value_from_locator('Количество путешественников в корзине', number_travelers) 
        self.check_field_value_from_locator('Общая цена корзины', all_price)


    @allure.step("Проверка общих цен с промокодом")
    def check_basket_tour1_all_price_block_with_promocode(self, price: str, options: str, number_travelers: str, all_price_before_discount: str, all_price_after_discount: str):
        self.check_field_value_from_locator('Цена всех туров в корзине', price)
        self.check_field_value_from_locator('Цена всех опций в корзине', options)
        # self.check_field_value_from_locator('Страховка в общих ценах с туром 1', insurance) #Страховка
        self.check_field_value_from_locator('Количество путешественников в корзине', number_travelers)
        self.check_field_value_from_locator('Общая цена корзины до скидки', all_price_before_discount)
        self.check_field_value_from_locator('Общая цена корзины после скидки', all_price_after_discount)


    #НЕАВТОРИЗОВАН
    @allure.step("Проверка элементов пустой корзины неавторизован")
    def check_empty_basket_no_auth(self, expected_my_basket, expected_empty_here, expected_description):
        self.check_field_value_from_locator('Заголовок в пустой корзине клиента', expected_my_basket)
        self.check_field_value_from_locator('Подзаголовок в пустой корзине клиента', expected_empty_here)
        self.check_field_value_from_locator('Описание в пустой корзине клиента', expected_description)


    @allure.step("Проверка первого тура в свернутом состоянии неавторизован")
    def check_basket_tour1_collapsed_no_auth(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок первого тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала первого тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания первого тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Общая цена первого тура в корзине неавторизован', all_price)


    @allure.step("Проверка первого тура в развернутом состоянии неавторизован")
    def check_basket_tour1_deployed_no_auth(self, title: str, start_date: str, end_date: str, format: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок первого тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала первого тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания первого тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Формат первого тура в корзине неавторизован', format)
        self.check_field_value_from_locator('Цена первого тура в корзине неавторизован', price)
        self.check_field_value_from_locator('Цена опций первого тура в корзине неавторизован', options)
        self.check_field_value_from_locator('Общая цена первого тура в корзине неавторизован', all_price)


    @allure.step("Проверка категорий возрастов в корзине неавторизован")
    def check_data_participants_ages_basket_no_auth(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в корзине неавторизован', category1)
        self.check_field_value_from_locator('Цена возраст1 в корзине неавторизован', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в корзине неавторизован', ages1)
        self.check_field_value_from_locator('Название возраст2 в корзине неавторизован', category2)
        self.check_field_value_from_locator('Цена возраст2 в корзине неавторизован', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в корзине неавторизован', ages2)
        self.check_field_value_from_locator('Название возраст3 в корзине неавторизован', category3)
        self.check_field_value_from_locator('Цена возраст3 в корзине неавторизован', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в корзине неавторизован', ages3)
        self.check_field_value_from_locator('Название возраст4 в корзине неавторизован', category4)
        self.check_field_value_from_locator('Цена возраст4 в корзине неавторизован', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в корзине неавторизован', ages4)
        self.check_field_value_from_locator('Название возраст5 в корзине неавторизован', category5)
        self.check_field_value_from_locator('Цена возраст5 в корзине неавторизован', price5)


    @allure.step("Проверка количества участников разных возрастов в корзине неавторизован")
    def check_data_participants_amount_basket_no_auth(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в корзине неавторизован', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в корзине неавторизован', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в корзине неавторизован', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в корзине неавторизован', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в корзине неавторизован', participants_number5)


    @allure.step("Проверка категорий возрастов в корзине группового неавторизован")
    def check_data_participants_ages_basket_group_no_auth(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в корзине неавторизован', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в корзине неавторизован', participants_number)


    @allure.step("Проверка составного первого тура в свернутом состоянии неавторизован")
    def check_basket_tour1_2_collapsed_no_auth(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок составного первого тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала составного первого тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания составного первого тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Общая цена составного первого тура в корзине неавторизован', all_price)


    @allure.step("Проверка составного первого тура в развернутом состоянии неавторизован")
    def check_basket_tour1_2_deployed_no_auth(self, title: str, start_date: str, end_date: str, format: str, tour_class: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок составного первого тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала составного первого тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания составного первого тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Формат составного первого тура в корзине неавторизован', format)
        self.check_field_value_from_locator('Класс составного первого тура в корзине неавторизован', tour_class)
        self.check_field_value_from_locator('Цена составного первого тура в корзине неавторизован', price)
        self.check_field_value_from_locator('Цена опций составного первого тура в корзине неавторизован', options)
        self.check_field_value_from_locator('Общая цена составного первого тура в корзине неавторизован', all_price)


    @allure.step("Проверка составного второго тура в свернутом состоянии неавторизован")
    def check_basket_tour2_collapsed_no_auth(self, title: str, start_date: str, end_date: str, all_price):
        self.check_field_value_from_locator('Заголовок второго тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала второго тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания второго тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Общая цена второго тура в корзине неавторизован', all_price)


    @allure.step("Проверка составного второго тура в развернутом состоянии неавторизован")
    def check_basket_tour2_deployed_no_auth(self, title: str, start_date: str, end_date: str, format: str, price: str, options: str, all_price):
        self.check_field_value_from_locator('Заголовок второго тура в корзине неавторизован', title)
        self.check_field_value_from_locator('Дата и время начала второго тура в корзине неавторизован', start_date)
        self.check_field_value_from_locator('Дата окончания второго тура в корзине неавторизован', end_date)
        self.check_field_value_from_locator('Формат второго тура в корзине неавторизован', format)
        self.check_field_value_from_locator('Цена второго тура в корзине неавторизован', price)
        self.check_field_value_from_locator('Цена опций второго тура в корзине неавторизован', options)
        self.check_field_value_from_locator('Общая цена второго тура в корзине неавторизован', all_price)


    @allure.step("Проверка общих цен неавторизован")
    def check_basket_tour1_all_price_block_no_auth(self, price: str, options: str, insurance: str, number_travelers: str, all_price): 
        self.check_field_value_from_locator('Цена всех туров в корзине неавторизован', price)
        self.check_field_value_from_locator('Цена всех опций в корзине неавторизован', options)
        self.check_field_value_from_locator('Страховка в общих ценах с туром 1 неавторизован', insurance)
        self.check_field_value_from_locator('Количество путешественников в корзине неавторизован', number_travelers) 
        self.check_field_value_from_locator('Общая цена корзины неавторизован', all_price)


    @allure.step("Проверка общих цен с промокодом неавторизован")
    def check_basket_tour1_all_price_block_with_promocode_no_auth(self, price: str, options: str, insurance: str, number_travelers: str, all_price_before_discount: str, all_price_after_discount: str):
        self.check_field_value_from_locator('Цена всех туров в корзине неавторизован', price)
        self.check_field_value_from_locator('Цена всех опций в корзине неавторизован', options)
        self.check_field_value_from_locator('Страховка в общих ценах с туром 1 неавторизован', insurance)
        self.check_field_value_from_locator('Количество путешественников в корзине неавторизован', number_travelers)
        self.check_field_value_from_locator('Общая цена корзины до скидки неавторизован', all_price_before_discount)
        self.check_field_value_from_locator('Общая цена корзины после скидки неавторизован', all_price_after_discount)

    @allure.step('Проверка платежа в базе данных')
    def check_payment_in_db(self, db_connection, order_id, expected_payment_method=None, expected_amount=None,
                            expected_commission_our=None, expected_commission_provider=None,
                            expected_sum_merchant=None, expected_status=None):
        max_attempts = 6
        attempt = 0
        last_exception = None
        while attempt < max_attempts:
            try:
                cursor = db_connection.cursor()
                cursor.execute("""
                    SELECT payment_method, payment_url, amount, commission_our, commission_provider,
                        sum_merchant, status
                    FROM payments
                    WHERE payable_id = %s
                    AND payable_type = 'smorodinaOrder'
                    AND type = 'marketplace'
                """, (str(order_id),))
                payment = cursor.fetchone()
                cursor.close()
                assert payment is not None, f"Платеж для order_id: {order_id} не найден в базе данных"
                payment_method, payment_url, amount, commission_our, commission_provider, sum_merchant, status = payment
                if expected_payment_method is not None:
                    assert payment_method == expected_payment_method, f"payment_method не совпадает. Ожидалось: {expected_payment_method}, но получено: {payment_method}"
                if expected_amount is not None:
                    expected_amount_float = float(expected_amount)
                    amount_float = float(amount)
                    assert amount_float == expected_amount_float, f"amount не совпадает. Ожидалось: {expected_amount:.2f}, но получено: {amount:.2f}"
                if expected_commission_our is not None:
                    expected_commission_our_float = float(expected_commission_our)
                    commission_our_float = float(commission_our)
                    assert commission_our_float == expected_commission_our_float, f"commission_our не совпадает. Ожидалось: {expected_commission_our:.2f}, но получено: {commission_our:.2f}"
                if expected_commission_provider is not None:
                    expected_commission_provider_float = float(expected_commission_provider)
                    commission_provider_float = float(commission_provider)
                    assert commission_provider_float == expected_commission_provider_float, f"commission_provider не совпадает. Ожидалось: {expected_commission_provider:.2f}, но получено: {commission_provider:.2f}"
                if expected_sum_merchant is not None:
                    expected_sum_merchant_float = float(expected_sum_merchant)
                    sum_merchant_float = float(sum_merchant)
                    assert sum_merchant_float == expected_sum_merchant_float, f"sum_merchant не совпадает. Ожидалось: {expected_sum_merchant:.2f}, но получено: {sum_merchant:.2f}"
                if expected_status is not None:
                    assert status == expected_status, f"status не совпадает. Ожидалось: {expected_status}, но получено: {status}"
                assert payment_url is not None, f"payment_url для заказа {order_id} равен NULL"
                allure.step(f"Платеж для order_id {order_id} успешно проверен с попытки {attempt + 1}")
                return
            except AssertionError as e:
                last_exception = e
                attempt += 1
                if attempt < max_attempts:
                    allure.step(f"Попытка {attempt} неуспешна. Повтор через 5 секунд...")
                    time.sleep(5)
        raise last_exception