import json
import allure
from Assertions.seller.seller_tours.seller_tour_card.seller_tour_parametrs.assert_seller_tour_parametrs import AssertionsTourParametrs
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsTourWaypoints(AssertionsTourParametrs): 

    @allure.title('Проверка часового пояса тура в БД')
    def check_tour_timezone_in_db(self, db_connection, title: str, timezone: int):
        timeout = 30  
        interval = 5  
        elapsed = 0
        fact_timezone = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            # Сначала находим ID тура по названию
            query = "SELECT id FROM products WHERE name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            if result is not None:
                tour_id = result[0]
                # Затем находим часовой пояс для этого тура
                query = "SELECT zone_id FROM itineraries WHERE tour_id = %s"
                cursor.execute(query, (tour_id,))
                timezone_result = cursor.fetchone()
                cursor.close()       
                if timezone_result is not None:
                    fact_timezone = timezone_result[0]
                    break
            else:
                cursor.close()     
            time.sleep(interval)
            elapsed += interval    
        if fact_timezone is None:
            raise AssertionError(f"Тур с названием '{title}' или его часовой пояс не найдены в базе данных за отведенное время.")      
        assert fact_timezone == timezone, \
            f"Ожидалось, что часовой пояс для тура '{title}' будет {timezone}, " \
            f"но в базе он равен {fact_timezone}."
        

    @allure.step("Проверка, что кнопка Сохранить в точке сбора продавца неактивна")
    def check_seller_waypoint_collection_point_button_save_inactive(self):
        self.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Сохранить в точке сбора в создании тура продавца'])
    

    @allure.step("Проверка, что выбор дня в точке сбора продавца неактивен")
    def check_seller_waypoint_collection_point_day_inactive(self):
        self.check_element_disabled_by_xpath(ALL_LOCATORS['День в точке сбора в создании тура продавца'])
    

    @allure.title('Проверка сохранения точки в БД')
    def check_seller_waypoint_in_db(self, db_connection, tour_title: str, cords: str, point_time: str, title: str, description: str, photo: int, point_type: int):
        timeout = 30
        interval = 5
        start_time = time.time()
        last_error = None
        
        def compare_json(expected, actual):
            try:
                # Если оба параметра строки - преобразуем в dict
                if isinstance(expected, str) and isinstance(actual, str):
                    return json.loads(expected) == json.loads(actual)
                # Если один параметр строка, а другой уже dict
                elif isinstance(expected, str):
                    return json.loads(expected) == actual
                elif isinstance(actual, str):
                    return expected == json.loads(actual)
                # Если оба уже dict
                else:
                    return expected == actual
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Ошибка сравнения JSON: {e}")
                return False

        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            if elapsed >= timeout:
                error_msg = (f"Точка маршрута не найдена или параметры не совпадают в течение {timeout} секунд.\n"
                            f"Последняя ошибка: {last_error}\n"
                            f"Ожидаемые значения: cords={cords}, time={point_time}, title={title}, "
                            f"description={description}, photo={photo}, point_type={point_type}")
                raise AssertionError(error_msg)
            
            cursor = None
            try:
                db_connection.rollback()
                cursor = db_connection.cursor()
                
                # Находим тур
                cursor.execute("SELECT id FROM products WHERE name = %s", (tour_title,))
                tour_result = cursor.fetchone()
                if not tour_result:
                    last_error = f"Тур с названием '{tour_title}' не найден"
                    time.sleep(interval)
                    continue
                    
                # Находим точку маршрута
                cursor.execute("""
                    SELECT id, info, event_time, point_type_id, description 
                    FROM product_details 
                    WHERE product_id = %s AND point_type_id = %s
                """, (tour_result[0], point_type))
                point_result = cursor.fetchone()
                
                if not point_result:
                    last_error = f"Точка маршрута типа {point_type} не найдена для тура '{tour_title}'"
                    time.sleep(interval)
                    continue
                    
                # Проверяем количество фото
                cursor.execute("SELECT COUNT(id) FROM product_detail_pictures WHERE product_detail_id = %s", (point_result[0],))
                photo_count = cursor.fetchone()[0]
                
                # Сравниваем параметры
                errors = []
                
                # Координаты (JSON сравнение)
                if not compare_json(cords, point_result[1]):
                    errors.append(f"Координаты не совпадают")
                
                # Время
                if str(point_result[2]) != str(point_time):
                    errors.append(f"Время: ожидалось {point_time}, получено {point_result[2]}")
                
                # Тип точки
                if point_result[3] != point_type:
                    errors.append(f"Тип точки: ожидалось {point_type}, получено {point_result[3]}")
                
                # Описание (сравниваем как есть)
                if str(point_result[4]) != str(description):
                    errors.append(f"Описание не совпадает")
                
                # Количество фото
                if photo_count != photo:
                    errors.append(f"Количество фото: ожидалось {photo}, получено {photo_count}")
                
                if not errors:
                    return True
                    
                last_error = "; ".join(errors)
                
            except Exception as e:
                last_error = f"Ошибка при проверке БД: {str(e)}"
                db_connection.rollback()
            finally:
                if cursor:
                    cursor.close()
            
            time.sleep(interval)