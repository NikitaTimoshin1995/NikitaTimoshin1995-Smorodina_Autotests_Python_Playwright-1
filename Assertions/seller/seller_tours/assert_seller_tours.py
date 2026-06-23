import allure
from Assertions.assertions import Assertions
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsTours(Assertions): 

    @allure.step("Проверка статуса тура в БД")
    def check_tour_status_in_db(self, db_connection, title, waiting_status):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product_id = None
        product_class_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "SELECT status_id FROM products WHERE name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                product_status = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        if  product_status is None:
            raise AssertionError(f"Тур с названием '{title}' не найден в базе данных за отведенное время.")
        assert product_status == waiting_status, \
            f"Ожидалось, что product_class_id для продукта '{title}' будет {waiting_status}, " \
            f"но в базе он равен {product_status}."