import allure
from Assertions.seller.seller_tours.seller_tour_card.assert_seller_tour_card import AssertionsTourCard
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsTourParametrs(AssertionsTourCard): 


    @allure.step("Проверка, что кнопка Сохранить в создани/редактировании тура активна")
    def check_operator_tour_param_button_create_active(self):
        self.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Сохранить в создании тура продавца'])


    @allure.step("Проверка, что кнопка Сохранить в создани/редактировании тура неактивна")
    def check_operator_tour_param_button_create_inactive(self):
        self.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка Сохранить в создании тура продавца'])


    @allure.step("Проверка, что кнопка На проверку в создани/редактировании тура неактивна")
    def check_operator_tour_param_button_on_review_inactive(self):
        self.check_element_disabled_by_xpath(ALL_LOCATORS['Кнопка на проверку в создании туру'])

    @allure.step("Проверка, что кнопка На проверку в создани/редактировании тура активна")
    def check_operator_tour_param_button_on_review_active(self):
        self.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка на проверку в создании туру'])


    @allure.step("Проверка статуса тура на фронте")
    def check_operator_tour_create_status_front(self, page: Page, status: str):
        status_xpath = ALL_LOCATORS['Текст статуса в создании тура продавца']
        start_time = time.time()
        while time.time() - start_time < 30:
            try:
                status_element = page.locator(f'xpath={status_xpath}')
                status_element.wait_for(state="visible")
                actual_status = status_element.text_content()
                assert actual_status == status, f"Ожидаемый статус: '{status}', фактический статус: '{actual_status}'"
                return  
            except Exception as e:
                allure.attach(f"Ошибка при проверке статуса: {e}", attachment_type=allure.attachment_type.TEXT)
                time.sleep(1) 
        raise AssertionError(f"Статус '{status}' не найден за 30 секунд.")
    

    @allure.title('Проверка создания тура в БД с ожиданием')
    def check_create_tour_in_db(self, db_connection, title: str, status_id: int, product_duration_id: int, number_nights: int, slug: str, operator_id: int):
        timeout = 30
        interval = 5
        elapsed = 0
        product = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select id, name, status_id, product_duration_id, number_nights, slug, operator_id from products where name = %s"
            cursor.execute(query, (title,))
            product = cursor.fetchone()
            cursor.close()
            if product is not None:
                product_id, name, product_status_id, product_product_duration_id, product_number_nights, product_slug, product_operator_id = product
                expected_slug = f"{slug}-{product_id}-{product_operator_id:04d}"
                if (name == title and 
                    product_status_id == status_id and 
                    product_product_duration_id == product_duration_id and 
                    product_number_nights == number_nights and 
                    product_slug == expected_slug and 
                    product_operator_id == operator_id):
                    break
                else:
                    print(f"Запись найдена, но поля не совпадают. Ожидание...")
                    product = None  
            time.sleep(interval)
            elapsed += interval
        assert product is not None, f"Тур с названием: {title} не найден в базе данных после ожидания {timeout} секунд."
        product_id, name, product_status_id, product_product_duration_id, product_number_nights, product_slug, product_operator_id = product
        expected_slug = f"{slug}-{product_id}-{product_operator_id:04d}"
        assert name == title, f"Название не совпадает. Ожидалось: {title}, но получено: {name}"
        assert product_status_id == status_id, f"Статус не совпадает. Ожидалось: {status_id}, но получено: {product_status_id}"
        assert product_product_duration_id == product_duration_id, f"Формат путешествия не совпадает. Ожидалось: {product_duration_id}, но получено: {product_product_duration_id}"
        assert product_number_nights == number_nights, f"Количество ночей не совпадает. Ожидалось: {number_nights}, но получено: {product_number_nights}"
        assert product_slug == expected_slug, f"Slug не совпадает. Ожидалось: {expected_slug}, но получено: {product_slug}"
        assert product_operator_id == operator_id, f"Operator ID не совпадает. Ожидалось: {operator_id}, но получено: {product_operator_id}"


    @allure.title('Проверка создания тура в БД с предварительным бронированием')
    def check_create_tour_in_db_with_reservations(self, db_connection, title: str, status_id: int, product_duration_id: int, number_nights: int, operator_id: int, advance_booking: bool ):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select name, status_id, product_duration_id, number_nights, operator_id, advance_booking from products where name = %s"
            cursor.execute(query, (title,))
            product = cursor.fetchone()
            cursor.close()
            if product is not None:
                break
            else:
                time.sleep(interval)
                elapsed += interval
        assert product is not None, f"Тур с названием: {title} не найден в базе данных после ожидания {timeout} секунд."
        name, product_status_id, product_product_duration_id, product_number_nights, product_operator_id, product_advance_booking = product
        assert name == title, f"Название не совпадает. Ожидалось: {title}, но получено: {name}"
        assert product_status_id == status_id, f"Cтатус не совпадает. Ожидалось: {status_id}, но получено: {product_status_id}"
        assert product_product_duration_id == product_duration_id, f"Формат путешествия не совпадает. Ожидалось: {product_duration_id}, но получено: {product_product_duration_id}"
        assert product_number_nights == number_nights, f"Количество ночей не совпадает. Ожидалось: {number_nights}, но получено: {product_number_nights}"
        assert product_operator_id == operator_id, f"Operator ID не совпадает. Ожидалось: {operator_id}, но получено: {product_operator_id}"
        assert product_advance_booking == advance_booking, f"Предварительное бронирование не совпадает. Ожидалось: {advance_booking}, но получено: {product_advance_booking}"


    @allure.title('Проверка создания тура в БД с жанрами')
    def check_create_tour_in_db_with_genre(self, db_connection, title: str, genre1: int, genre2: int):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select id from products where name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                product_id = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        assert product_id is not None, f"Тур с названием: {title} не найден в базе данных после ожидания {timeout} секунд."
        cursor = db_connection.cursor()
        query_genres = "select genre_id from product_genre where product_id = %s order by genre_id"
        cursor.execute(query_genres, (product_id,))
        genres = cursor.fetchall()
        cursor.close()
        assert len(genres) == 2, f"Ожидалось 2 жанра, получено {len(genres)}."
        genre_ids = [row[0] for row in genres]
        genre_ids.sort()
        expected_genres = sorted([genre1, genre2])
        assert genre_ids == expected_genres, \
            f"Жанры не совпадают. Ожидалось: {expected_genres}, получено: {genre_ids}"
   

    @allure.step("Проверка наличия SVG рядом с текстом: '{text}'")
    def check_svg_near_text(self, text: str):
        locator = self.page.locator(f"div._statusField_1488g_11", has_text=text)
        count = locator.count()
        assert count > 0, f"Не найдено элементов с текстом '{text}'"
        for i in range(count):
            element = locator.nth(i)
            svg_locator = element.locator("svg")
            expect(svg_locator).to_be_visible()
       
    @allure.step("Проверка наличия IMG рядом с текстом: '{text}'")            
    def check_img_near_text(self, text: str):
        locator = self.page.locator(f"div._statusField_1488g_11", has_text=text)
        count = locator.count()
        assert count > 0, f"Не найдено элементов с текстом '{text}'"
        for i in range(count):
            element = locator.nth(i)
            expect(element.locator("img")).to_be_visible()

    @allure.step('Проверка что тогл бронирования выключен/включен на фронте')
    def verify_toggle_checked_by_xpath(self, page, xpath_or_key, expected_checked_value):
        # формируем XPath из словаря по ключу
        xpath = f"xpath={ALL_LOCATORS[xpath_or_key]}"
        # ищем элемент по XPath
        element = page.query_selector(xpath)
        if element is None:
            raise Exception(f'Элемент по XPath "{xpath}" не найден.')
        checked_value = element.get_attribute('checked')
        if checked_value is None:
            checked_value = 'false'
        assert checked_value.lower() == expected_checked_value.lower(), \
            f"Ожидалось: '{expected_checked_value}', но атрибут 'checked' равен: '{checked_value}'"
        

    @allure.step('Проверка, что чекбокс по локатору {xpath_or_key} отмечен или не отмечен')
    def verify_checkbox_state(self, page, xpath_or_key, expected_checked: bool):
        xpath = f"xpath={ALL_LOCATORS[xpath_or_key]}"
        element = page.query_selector(xpath)
        if element is None:
            raise Exception(f'Элемент по XPath "{xpath}" не найден.')
        is_checked = page.eval_on_selector(xpath, '''
            (el) => {
                const style = window.getComputedStyle(el, '::after');
                // Проверяем, что псевдоэлемент существует и видим
                return style && style.display !== 'none' && style.opacity !== '0';
            }
        ''')
        assert is_checked == expected_checked, \
            f"Ожидалось, что чекбокс по локатору '{xpath_or_key}' будет {'отмечен' if expected_checked else 'не отмечен'}, " \
            f"но оно оказалось {'отмечен' if is_checked else 'не отмечен'}."
        

    @allure.step('Проверка какой класс выбран на фронте')
    def verify_classes_by_xpath(self, page, bool1, bool2, bool3):
        # Определяем XPath
        xpath1 = f"xpath={ALL_LOCATORS['1й класс в параметрах тура']}"
        xpath2 = f"xpath={ALL_LOCATORS['2й класс в параметрах тура']}"
        xpath3 = f"xpath={ALL_LOCATORS['3й класс в параметрах тура']}"
        xpaths_and_classes = [
            (xpath1, bool1),
            (xpath2, bool2),
            (xpath3, bool3)
        ]
        for idx, (xpath, bool_value) in enumerate(xpaths_and_classes, start=1):
            element = page.query_selector(xpath)
            if element is None:
                raise Exception(f'Элемент по XPath {xpath} (номер {idx}) не найден.')
            class_attr = element.get_attribute('class')
            if class_attr is None:
                raise Exception(f'Элемент по XPath {xpath} (номер {idx}) не имеет атрибута class.')
            if bool_value:
                assert '_classItem_8k0bi_7' in class_attr, \
                    f'Для элемента по XPath {xpath} (номер {idx}) ожидается класс "_classItem_8k0bi_7".'
                assert '_classItemClick_8k0bi_20' in class_attr, \
                    f'Для элемента по XPath {xpath} (номер {idx}) ожидается класс "_classItemClick_8k0bi_20".'
            else:
                assert '_classItem_8k0bi_7' in class_attr, \
                    f'Для элемента по XPath {xpath} (номер {idx}) ожидается класс "_classItem_8k0bi_7".'
                assert '_classItemClick_8k0bi_20' not in class_attr, \
                    f'Для элемента по XPath {xpath} (номер {idx}) не ожидается класс "_classItemClick_8k0bi_20".'
                

    @allure.title('Проверка создания тура в БД с классом')
    def check_create_tour_in_db_with_class(self, db_connection, title: str, service_class: int):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product_id = None
        product_class_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "SELECT product_class_id FROM products WHERE name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                product_class_id = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        if product_class_id is None:
            raise AssertionError(f"Тур с названием '{title}' не найден в базе данных за отведенное время.")
        assert product_class_id == service_class, \
            f"Ожидалось, что product_class_id для продукта '{title}' будет {service_class}, " \
            f"но в базе он равен {product_class_id}."
        

    @allure.step('Проверка какой транспорт выбран на фронте')
    def verify_transport_front_by_xpath(self, page, is_own_car_selected, is_organizer_car_selected):
        xpath_own_car = f"xpath={ALL_LOCATORS['На своей машине в параметрах тура']}"
        xpath_org_car = f"xpath={ALL_LOCATORS['На машине организатора в параметрах тура']}"
        xpaths_and_states = [
            (xpath_own_car, is_own_car_selected),
            (xpath_org_car, is_organizer_car_selected)
        ]
        for idx, (xpath, is_selected) in enumerate(xpaths_and_states, start=1):
            element = page.query_selector(xpath)
            if element is None:
                raise Exception(f'Элемент транспорта по XPath {xpath} (номер {idx}) не найден.')
            class_attr = element.get_attribute('class')
            if class_attr is None:
                raise Exception(f'Элемент транспорта по XPath {xpath} (номер {idx}) не имеет атрибута class.')
            if is_selected:
                assert '_transportItemClick_1olxa_20' in class_attr, \
                    f'Для выбранного транспорта по XPath {xpath} (номер {idx}) ожидается класс "_transportItemClick_1olxa_20".'
                checkmark = element.query_selector('._checkmark_1olxa_37')
                assert checkmark is not None, \
                    f'Для выбранного транспорта по XPath {xpath} (номер {idx}) ожидается элемент с галочкой.'
            else:
                assert '_transportItemClick_1olxa_20' not in class_attr, \
                    f'Для невыбранного транспорта по XPath {xpath} (номер {idx}) не ожидается класс "_transportItemClick_1olxa_20".'
                checkmark = element.query_selector('._checkmark_1olxa_37')
                assert checkmark is None, \
                    f'Для невыбранного транспорта по XPath {xpath} (номер {idx}) не ожидается элемент с галочкой.'
                

    @allure.title('Проверка создания тура в БД с транспортом')
    def check_create_tour_in_db_with_transport(self, db_connection, title: str, transport: int):
        timeout = 30  
        interval = 5  
        elapsed = 0
        transport_type_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "SELECT transport_type_id FROM products WHERE name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                transport_type_id = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        if transport_type_id is None:
            raise AssertionError(f"Тур с названием '{title}' не найден в базе данных за отведенное время.")
        assert transport_type_id == transport, \
            f"Ожидалось, что product_class_id для продукта '{title}' будет {transport}, " \
            f"но в базе он равен {transport_type_id}."
        

    @allure.title('Проверка создания тура в БД с фото')
    def check_create_tour_in_db_with_photo(self, db_connection, title: str, count_photo):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select id from products where name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                product_id = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        assert product_id is not None, f"Тур с названием: {title} не найден в базе данных после ожидания {timeout} секунд."
        cursor = db_connection.cursor()
        query_photos = "select count(*) from product_pictures where product_id = %s"
        cursor.execute(query_photos, (product_id,))
        photos_count = cursor.fetchone()[0]
        cursor.close()
        assert photos_count == count_photo, (
            f"Количество фотографий в БД ({photos_count}) не соответствует ожидаемому ({count_photo}) "
            f"для тура с ID {product_id}"
        )


    @allure.step("Проверить наличие предупреждения о количестве фото")
    def check_photo_count_warning_visible(self):
        warning_locator = ALL_LOCATORS.get('Предупреждение о количестве фото в создании тура продавца')
        if not warning_locator:
            raise ValueError("Локатор предупреждения не найден в справочнике ALL_LOCATORS")      
        try:
            element = self.page.locator(f'xpath={warning_locator}')
            # Ждем видимости элемента
            element.wait_for(state="visible", timeout=15000)
            # Получаем текст внутри элемента
            warning_text = element.inner_text()
            # Проверяем наличие ожидаемого текста
            expected_substring = "Может быть максимум 10 фото."
            if expected_substring not in warning_text:
                raise AssertionError(f"Текст предупреждения не содержит ожидаемый фрагмент: '{expected_substring}'. Получено: '{warning_text}'")
            return True
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="warning_not_displayed",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Элемент предупреждения не отображается или содержит неправильный текст: {str(e)}")
        

    @allure.step("Проверить, что фото {photo_number} отмечено как главное")
    def check_main_photo_marked(self, photo_number: int):
        if not 1 <= photo_number <= 10:
            raise ValueError("Номер фото должен быть от 1 до 10")
        locator_key = f'Лэйбл главного фото для Фото{photo_number} в создании тура продавца'
        main_photo_locator = ALL_LOCATORS.get(locator_key)
        
        if not main_photo_locator:
            raise ValueError(f"Локатор для главного фото {photo_number} не найден в справочнике")
        try:
            element = self.page.locator(f'xpath={main_photo_locator}')
            element.wait_for(state="visible", timeout=15000)
            return True
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"main_photo_{photo_number}_not_marked",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Фото {photo_number} не отмечено как главное: {str(e)}")
        

    @allure.title('Проверка создания тура в БД с Описанием')
    def check_create_tour_in_db_with_desc(self, db_connection, title: str, tour_desc: str):
        timeout = 30  # Максимальное время ожидания в секундах
        interval = 5  # Интервал между попытками в секундах
        start_time = time.time()
        last_exception = None
        while time.time() - start_time < timeout:
            cursor = None
            try:
                cursor = db_connection.cursor()
                query = "SELECT description FROM products WHERE name = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()
                if result is not None:
                    db_description = result[0]
                    if db_description == tour_desc:
                        return True  # Успешная проверка
                    else:
                        last_exception = AssertionError(
                            f"Описание тура не совпадает\n"
                            f"Ожидалось: '{tour_desc}'\n"
                            f"Получено: '{db_description}'"
                        )
            except Exception as e:
                last_exception = e
            finally:
                if cursor is not None:
                    cursor.close()
            time.sleep(interval)
        if last_exception is not None:
            raise last_exception
        raise AssertionError(
            f"Тур с названием '{title}' не найден в БД "
            f"в течение {timeout} секунд"
        )

 
    @allure.title('Проверка создания тура в БД с Что входит')
    def check_create_tour_in_db_with_in_price(self, db_connection, title: str, in_price: str):
        timeout = 30  # Максимальное время ожидания в секундах
        interval = 5  # Интервал между попытками в секундах
        start_time = time.time()
        last_exception = None
        while time.time() - start_time < timeout:
            cursor = None
            try:
                cursor = db_connection.cursor()
                query = "SELECT description_inc_price FROM products WHERE name = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()
                if result is not None:
                    db_description = result[0]
                    if db_description == in_price:
                        return True  # Успешная проверка
                    else:
                        last_exception = AssertionError(
                            f"Описание тура не совпадает\n"
                            f"Ожидалось: '{in_price}'\n"
                            f"Получено: '{db_description}'"
                        )
            except Exception as e:
                last_exception = e
            finally:
                if cursor is not None:
                    cursor.close()
            time.sleep(interval)
        if last_exception is not None:
            raise last_exception
        raise AssertionError(
            f"Тур с названием '{title}' не найден в БД "
            f"в течение {timeout} секунд"
        )


    @allure.title('Проверка создания тура в БД с Что  не входит')
    def check_create_tour_in_db_with_not_in_price(self, db_connection, title: str, not_in_price: str):
        timeout = 30  # Максимальное время ожидания в секундах
        interval = 5  # Интервал между попытками в секундах
        start_time = time.time()
        last_exception = None
        while time.time() - start_time < timeout:
            cursor = None
            try:
                cursor = db_connection.cursor()
                query = "SELECT description_not_inc_price FROM products WHERE name = %s"
                cursor.execute(query, (title,))
                result = cursor.fetchone()
                
                if result is not None:
                    db_description = result[0]
                    if db_description == not_in_price:
                        return True  # Успешная проверка
                    else:
                        last_exception = AssertionError(
                            f"Описание тура не совпадает\n"
                            f"Ожидалось: '{not_in_price}'\n"
                            f"Получено: '{db_description}'"
                        )
            except Exception as e:
                last_exception = e
            finally:
                if cursor is not None:
                    cursor.close()
            time.sleep(interval)
        if last_exception is not None:
            raise last_exception
        raise AssertionError(
            f"Тур с названием '{title}' не найден в БД "
            f"в течение {timeout} секунд"
        )
    

    @allure.title('Проверка создания тура в БД с кому подходит')
    def check_create_tour_in_db_with_suitable(self, db_connection, title: str, suitable1: int, suitable2: int):
        timeout = 30  
        interval = 5  
        elapsed = 0
        product_id = None
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select id from products where name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                product_id = result[0]
                break
            else:
                time.sleep(interval)
                elapsed += interval
        assert product_id is not None, f"Тур с названием: {title} не найден в базе данных после ожидания {timeout} секунд."
        cursor = db_connection.cursor()
        query_suitables = "select suitable_id from product_suitables where product_id = %s order by suitable_id"
        cursor.execute(query_suitables, (product_id,))
        suitables = cursor.fetchall()
        cursor.close()
        assert len(suitables) == 2, f"Ожидалось 2 кому подходит, получено {len(suitables)}."
        suitable_ids = [row[0] for row in suitables]
        suitable_ids.sort()
        expected_suitables = sorted([suitable1, suitable2])
        assert suitable_ids == expected_suitables, \
            f"Кому подходит не совпадают. Ожидалось: {expected_suitables}, получено: {suitable_ids}"
        

    @allure.title('Проверка создания тура в БД с идентификатором отеля')
    def check_create_tour_in_db_with_hotelid(self, db_connection, title: str, hotelid: str, hotelid_link: str):
        timeout = 30
        interval = 5
        elapsed = 0
        while elapsed < timeout:
            cursor = db_connection.cursor()
            query = "select hotel_id, hotel_ref from products where name = %s"
            cursor.execute(query, (title,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                db_hotel_id, db_hotel_ref = result
                if db_hotel_id == hotelid and db_hotel_ref == hotelid_link:
                    return True
                error_msg = (f"Данные тура не совпадают:\n"
                            f"Ожидалось: hotel_id={hotelid}, hotel_ref={hotelid_link}\n"
                            f"Фактически: hotel_id={db_hotel_id}, hotel_ref={db_hotel_ref}")
                raise AssertionError(error_msg)
            time.sleep(interval)
            elapsed += interval
        raise AssertionError(f"Тур с title='{title}' не найден в БД в течение {timeout} секунд")


    @allure.title('Проверка создания тура все поля кроме основного неактивны')
    def check_create_tour_all_fields_disable(self, disable_class):
        self.check_element_class_starts_with('Блок жанров в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок классов в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок транспорта в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок фото в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок описания в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок что входит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок что не входит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок кому подходит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок маршрут в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок часовой пояс в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок идентификатор отеля в параметрах тура', disable_class)


    @allure.title('Проверка создания тура все поля неактивны')
    def check_create_tour_all_with_general_fields_disable(self, disable_class):
        self.check_element_class_starts_with('Блок основное в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок жанров в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок классов в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок транспорта в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок фото в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок описания в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок что входит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок что не входит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок кому подходит в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок маршрут в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок часовой пояс в параметрах тура', disable_class)
        self.check_element_class_starts_with('Блок идентификатор отеля в параметрах тура', disable_class)