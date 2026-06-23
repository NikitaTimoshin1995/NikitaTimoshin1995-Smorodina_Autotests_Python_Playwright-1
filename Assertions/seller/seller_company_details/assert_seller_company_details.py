import allure
from Assertions.assertions import Assertions
from playwright.sync_api import Page
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsCompanyDetails(Assertions):

    #Общие проверки
    @allure.step("Проверка статуса оператора в БД")
    def check_operator_status(self, db_connection, operator_email: str, status: int):
        cursor = db_connection.cursor()
        query = "SELECT status FROM operators WHERE email = %s"
        timeout = 30  
        interval = 2  
        end_time = time.time() + timeout
        try:
            while time.time() < end_time:
                cursor.execute(query, (operator_email,))
                result = cursor.fetchone()  
                if result is None:
                    raise ValueError(f"Оператор с email '{operator_email}' не найден.")  
                current_status = result[0]  
                if current_status == status:
                    print(f"Статус оператора '{operator_email}' соответствует ожидаемому: {current_status}.")
                    return
                time.sleep(interval)
            raise ValueError(
                f"Таймаут {timeout} секунд. Статус оператора '{operator_email}' не соответствует ожидаемому. "
                f"Последний полученный: {current_status}, Ожидаемый: {status}."
            )     
        finally:
            cursor.close()


    @allure.step("Проверка статуса оператора на фронте")
    def check_operator_status_front(self, page: Page, status: str):
        status_xpath = ALL_LOCATORS['Статус в данных компании']
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
    

    @allure.step("Проверка, что кнопка 'Сохранить' в данных компании неактивна")
    def check_operator_company_button_inactive(self, timeout=30):
        start_time = time.time()
        xpath = ALL_LOCATORS['кнопка Сохранить в данных компании продавца']
        while time.time() - start_time < timeout:
            try:
                self.check_element_disabled_by_xpath(xpath)
                return  
            except AssertionError:
                time.sleep(1)
        raise AssertionError("Кнопка 'Сохранить' осталась активной после ожидания 30 секунд.")
    

    @allure.step("Проверка, что кнопка Сохранить в данных компании активна")
    def check_operator_company_button_active(self):
        self.check_element_enabled_by_xpath(ALL_LOCATORS['кнопка Сохранить в данных компании продавца'])
    

    @allure.step("Проверка, что под инн появился текст '{text}'")
    def check_operator_company_inn_state_null(self, text: str):
        timeout = 30
        interval = 5
        start_time = time.time()
        xpath = ALL_LOCATORS['Текст под инн']  # Получаем строку с xpath
        while time.time() - start_time < timeout:
            try:
                self.check_input_value_by_xpath_div(xpath, text)  # Передаем строку с xpath
                return
            except AssertionError:
                pass
            time.sleep(interval)
        try:
            locator = self.page.locator(f"xpath={xpath}")
            actual_value = locator.text_content().strip()
        except Exception:
            actual_value = "не удалось получить значение"
        raise AssertionError(f"Текст '{text}' не появился под инн за {timeout} секунд. Последнее значение: '{actual_value}'")
    

    @allure.title('Проверка создания оператора в БД с фото')
    def check_operator_info__photo_db(self, db_connection, login: str, count_photo):
        timeout = 30  
        interval = 3  
        for elapsed in range(0, timeout, interval):
            cursor = db_connection.cursor()
            try:
                query_user = "SELECT id FROM users WHERE email = %s"
                cursor.execute(query_user, (login,))
                user_result = cursor.fetchone()
                if user_result is None:
                    print(f"Пользователь {login} не найден, ждем {interval} сек...")
                    continue
                user_id = user_result[0]
                query_operator = "SELECT id FROM operators WHERE admin_id = %s"
                cursor.execute(query_operator, (user_id,))
                operator_result = cursor.fetchone()
                if operator_result is None:
                    print(f"Оператор для user_id {user_id} не найден, ждем {interval} сек...")
                    continue
                operator_id = operator_result[0]
                query_photos = "SELECT count(*) FROM operator_images WHERE operator_id = %s"
                cursor.execute(query_photos, (operator_id,))
                photos_count = cursor.fetchone()[0]
                if photos_count == count_photo:
                    print(f"Успех! Найдено {photos_count} фото для оператора {operator_id}")
                    return
                else:
                    print(f"Фото: {photos_count} из {count_photo} для оператора {operator_id}, ждем {interval} сек...")   
            finally:
                cursor.close()
            if elapsed + interval < timeout:
                time.sleep(interval)
        raise AssertionError(
            f"Не удалось найти оператора с {count_photo} фото для логина {login} за {timeout} секунд"
    )


    @allure.step("Проверка логотипа оператора в БД")
    def check_operator_logo_in_db(self, db_connection, login: str, has_logo: bool):
        timeout = 30
        interval = 3
        elapsed = 0
        while elapsed < timeout:
            try:
                cursor = db_connection.cursor()
                query_user_id = "SELECT id FROM users WHERE email = %s"
                cursor.execute(query_user_id, (login,))
                user_id = cursor.fetchone()
                if user_id is None:
                    cursor.close()
                    time.sleep(interval)
                    elapsed += interval
                    continue   
                user_id = user_id[0]
                query_logo = "SELECT logo FROM operators WHERE admin_id = %s"
                cursor.execute(query_logo, (user_id,))
                logo_result = cursor.fetchone()
                cursor.close()
                if logo_result is None:
                    time.sleep(interval)
                    elapsed += interval
                    continue
                logo_value = logo_result[0]
                if has_logo:
                    if logo_value is not None:
                        return
                else:
                    if logo_value is None:
                        return
            except Exception:
                pass 
            time.sleep(interval)
            elapsed += interval
        assert False, f"Логотип оператора с логином {login} не соответствует ожиданию. Ожидалось: {'не null' if has_logo else 'null'}"