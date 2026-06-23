import allure
from playwright.sync_api import Page, expect, TimeoutError
import re
import psycopg2
import time
from Locators.loc_all_directories import ALL_LOCATORS
from Locators.Seller.seller_tours.seller_tour_card.seller_tour_parametrs.loc_seller_tour_parametrs import LOCATORS_SELLER_TOUR_CREATE_UPDATE

class Assertions:
    def __init__(self, page: Page):
        self.page = page


    @allure.step('Проверка URL')
    def check_url(self, expected_url: str, timeout=30000):
        start_time = time.time() * 1000  
        check_interval = 3000  
        last_error = None
        while (time.time() * 1000 - start_time) < timeout:
            try:
                # Используем короткий таймаут для каждой отдельной проверки
                expect(self.page).to_have_url(expected_url, timeout=check_interval)
                return  
            except Exception as e:
                last_error = e
                time.sleep(check_interval / 1000)  
        if last_error:
            raise last_error
        raise TimeoutError(f"Timeout {timeout}ms exceeded while waiting for URL to become {expected_url}")


    @allure.step('Проверка статусов запросов. Что все с кодом 200')
    def check_request_statuses(self, requests):
        for request in requests:
            response = request.response()  
            assert response is not None, f"Запрос {request.url} не получил ответа"
            assert response.status in (200, 201, 302, 304), f"Запрос {request.url} завершился с кодом {response.status}"


    @allure.step('Проверка наличия ошибки "{text}"')
    def check_div_with_text(self, text: str):
        locator = self.page.locator(f"text={text}")
        expect(locator).to_be_visible()


    @allure.step('Проверка отсутствия ошибки "{text}"')
    def check_div_with_text_not_present(self, text: str, timeout: int = 5000):
        locator = self.page.locator(f"text={text}")
        expect(locator).not_to_be_visible(timeout=timeout)


    @allure.step('Проверка выделения красным поля "{xpath}"')
    def check_border_style_by_xpath(self, xpath: str):
        locator = self.page.locator(f"xpath={xpath}")
        expect(locator).to_have_class(re.compile(r".*\binvalid\b.*"))


    @allure.step('Проверка успешного создания пользователя-продавца в базе данных')
    def check_user_in_db(self, db_connection, email: str, phone: str, active: int, consent_advertising: int):
        max_attempts = 6  
        attempt = 0
        last_exception = None
        while attempt < max_attempts:
            try:
                cursor = db_connection.cursor()
                query = "SELECT login, active, email, phone, consent_advertising FROM users WHERE email = %s"
                cursor.execute(query, (email,))
                user = cursor.fetchone()
                cursor.close()
                assert user is not None, f"Пользователь с email: {email} не найден в базе данных."
                login, user_active, user_email, user_phone, user_consent_advertising = user
                assert login == email, f"Email не совпадает. Ожидалось: {email}, но получено: {login}"
                assert user_active == active, f"Active статус не совпадает. Ожидалось: {active}, но получено: {user_active}"
                assert user_email == email, f"Email не совпадает. Ожидалось: {email}, но получено: {user_email}"
                assert user_phone == phone, f"Телефон не совпадает. Ожидалось: {phone}, но получено: {user_phone}"
                assert user_consent_advertising == consent_advertising, f"Согласие на рекламу не совпадает. Ожидалось: {consent_advertising}, но получено: {user_consent_advertising}"
                allure.step(f"Пользователь успешно найден в базе данных с попытки {attempt + 1}")
                return  
            except AssertionError as e:
                last_exception = e
                attempt += 1
                if attempt < max_attempts:
                    allure.step(f"Попытка {attempt} неуспешна. Повтор через 5 секунд...")
                    time.sleep(5)
        raise last_exception

    @allure.step('Проверка успешного создания пользователя-клиента в базе данных по телефону')
    def check_user_by_phone_in_db(self, db_connection, phone: str, active: int, expected_consent: dict):
        max_attempts = 6
        attempt = 0
        last_exception = None
        while attempt < max_attempts:
            try:
                cursor = db_connection.cursor()
                query = "SELECT active, phone, consents FROM users WHERE phone = %s"
                cursor.execute(query, (phone,))
                user = cursor.fetchone()
                cursor.close()
                assert user is not None, f"Пользователь с телефоном: {phone} не найден в базе данных."
                user_active, user_phone, actual_consent = user
                assert user_phone == phone, f"Телефон не совпадает. Ожидалось: {phone}, но получено: {user_phone}"
                assert user_active == active, f"Active статус не совпадает. Ожидалось: {active}, но получено: {user_active}"
                for key, expected_value in expected_consent.items():
                    assert actual_consent.get(key) == expected_value, \
                        f"Поле {key} не совпадает. Ожидалось: {expected_value}, получено: {actual_consent.get(key)}"
                allure.step(f"Пользователь с телефоном {phone} успешно найден в базе данных с попытки {attempt + 1}")
                return
            except AssertionError as e:
                last_exception = e
                attempt += 1
                if attempt < max_attempts:
                    allure.step(f"Попытка {attempt} неуспешна. Повтор через 5 секунд...")
                    time.sleep(5)
        raise last_exception
    
    @allure.step('Проверка ролей пользователя в базе данных')
    def check_user_roles_in_db(self, db_connection, phone: str, **roles):
        max_attempts = 6
        attempt = 0
        last_exception = None
        while attempt < max_attempts:
            try:
                cursor = db_connection.cursor()
                cursor.execute("SELECT id FROM users WHERE phone = %s", (phone,))
                user = cursor.fetchone()
                assert user is not None, f"Пользователь с телефоном: {phone} не найден в базе данных."
                user_id = user[0]
                cursor.execute("SELECT role_id FROM model_has_roles WHERE model_id = %s", (user_id,))
                roles_from_db = {row[0] for row in cursor.fetchall()}
                cursor.close()
                role_mapping = {
                    "traveller": 49,
                    "operator": 51,
                    "poster_author": 56,
                    "media_author": 55,
                    "admin": 50,
                    "operator_employee": 52,
                    "partner": 53,
                    "referral": 54
                }
                for role_name, expected in roles.items():
                    expected_value = 1 if expected else 0
                    role_id = role_mapping.get(role_name)
                    if role_id is None:
                        raise AssertionError(f"Неизвестная роль: {role_name}")
                    has_role = role_id in roles_from_db
                    assert has_role == (expected == 1), \
                        f"Роль '{role_name}' (ID: {role_id}) не соответствует ожиданию. Ожидалось: {expected}, получено: {1 if has_role else 0}"
                all_expected_roles = {role_mapping[name] for name, expected in roles.items() if expected}
                extra_roles = roles_from_db - all_expected_roles
                if extra_roles:
                    extra_names = [name for name, rid in role_mapping.items() if rid in extra_roles]
                    raise AssertionError(f"Найдены лишние роли: {extra_names} (IDs: {extra_roles})")
                allure.step(f"Роли пользователя с телефоном {phone} успешно проверены с попытки {attempt + 1}")
                return
            except AssertionError as e:
                last_exception = e
                attempt += 1
                if attempt < max_attempts:
                    allure.step(f"Попытка {attempt} неуспешна. Повтор через 5 секунд...")
                    time.sleep(5)
        raise last_exception

    @allure.step('Проверка, что элемент  "{xpath}" отключен')
    def check_element_disabled_by_xpath(self, xpath: str):
        locator = self.page.locator(f"xpath={xpath}")
        is_disabled = locator.evaluate("element => element.hasAttribute('disabled')")
        assert is_disabled, f"Элемент по xpath: {xpath} не отключен."


    @allure.step('Проверка, что элемент "{xpath}" включен')
    def check_element_enabled_by_xpath(self, xpath: str):
        locator = self.page.locator(f"xpath={xpath}")
        is_enabled = locator.evaluate("element => !element.hasAttribute('disabled')")
        assert is_enabled, f"Элемент по xpath: {xpath} отключен."


    @allure.step('Проверка, что значение поля по xpath "{xpath}" равно "{expected_value}"')
    def check_input_value_by_xpath(self, xpath: str, expected_value: str):
        locator = self.page.locator(f"xpath={xpath}")
        actual_value = locator.get_attribute("value")
        assert actual_value == expected_value, f"Ожидалось значение '{expected_value}', получено '{actual_value}' для xpath: {xpath}"
    

    @allure.step('Проверка, что значение поля по xpath "{xpath}" равно "{expected_value}"')
    def check_input_value_by_xpath_div(self, xpath: str, expected_value: str):
        locator = self.page.locator(f"xpath={xpath}")
        actual_value = locator.text_content().strip()  
        assert actual_value == expected_value, f"Ожидалось значение '{expected_value}', получено '{actual_value}' для xpath: {xpath}"


    @allure.step('Проверка значения поля "{locator_name}"')
    def check_field_value_from_locator(self, locator_name: str, expected_value: str):
        xpath = ALL_LOCATORS.get(locator_name)
        assert xpath is not None, f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS"   
        max_wait_time = 30  
        retry_interval = 2  
        max_attempts = max_wait_time // retry_interval
        actual_value = None
        locator = None
        value_matches = False
        last_error = None
        for attempt in range(max_attempts + 1):
            try:
                locator = self.page.locator(f"xpath={xpath}")
                locator.wait_for(state="visible", timeout=2000)
                actual_value = (
                    locator.get_attribute("value") or  # Для input/textarea
                    locator.get_attribute("textContent") or  # Для div/span
                    locator.inner_text()  # Для contenteditable и других элементов
                )
                if actual_value is not None:
                    actual_value_clean = ' '.join(actual_value.strip().split()) if actual_value else ""
                    expected_value_clean = ' '.join(expected_value.strip().split())
                    if actual_value_clean == expected_value_clean:
                        value_matches = True
                        break
                    else:
                        # Значение получено, но не совпадает — ждем и пробуем снова
                        if attempt < max_attempts:
                            time.sleep(retry_interval)
                        continue
                else:
                    # Значение None — ждем и пробуем снова
                    if attempt < max_attempts:
                        time.sleep(retry_interval)
                    continue
            except TimeoutError:
                last_error = f"Элемент не найден по локатору '{locator_name}' (попытка {attempt + 1}/{max_attempts + 1})"
                if attempt < max_attempts:
                    time.sleep(retry_interval)
                continue
            except Exception as e:
                last_error = f"Ошибка при получении значения: {str(e)} (попытка {attempt + 1}/{max_attempts + 1})"
                if attempt < max_attempts:
                    time.sleep(retry_interval)
                continue
        if not value_matches:
            if actual_value is None:
                raise AssertionError(
                    f"Не удалось найти элемент или получить значение за {max_wait_time} секунд\n"
                    f"Локатор: '{locator_name}'\n"
                    f"XPath: {xpath}\n"
                    f"Последняя ошибка: {last_error}"
                )
            else:
                actual_value_clean = ' '.join(actual_value.strip().split()) if actual_value else ""
                expected_value_clean = ' '.join(expected_value.strip().split())
                raise AssertionError(
                    f"Значение поля '{locator_name}' не совпадает после {max_attempts + 1} попыток.\n"
                    f"Ожидалось: '{expected_value_clean}'\n"
                    f"Получено: '{actual_value_clean}'\n"
                    f"Тип элемента: {locator.evaluate('el => el.tagName') if locator else 'N/A'}\n"
                    f"XPath: {xpath}\n"
                    f"Количество попыток: {attempt + 1}"
                )

    
    @allure.step('Проверка, что элемент "{locator_name}" имеет класс "{expected_class}"')
    def check_element_has_class(self, locator_name: str, expected_class: str):
        xpath = ALL_LOCATORS.get(locator_name)
        if not xpath:
            raise ValueError(f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS")
        locator = self.page.locator(f"xpath={xpath}")
        has_class = locator.evaluate("(element, cls) => element.classList.contains(cls)", expected_class)
        assert has_class, f"Элемент '{locator_name}' (xpath: {xpath}) не содержит класс '{expected_class}'"


    @allure.step('Проверка, что элемент "{locator_name}" имеет класс, начинающийся с "{expected_class_start}"')
    def check_element_class_starts_with(self, locator_name: str, expected_class_start: str):
        xpath = ALL_LOCATORS.get(locator_name)
        if not xpath:
            raise ValueError(f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS")
        locator = self.page.locator(f"xpath={xpath}")
        class_list = locator.evaluate("element => Array.from(element.classList)")
        has_matching_class = any(cls.startswith(expected_class_start) for cls in class_list)
        assert has_matching_class, (
            f"Элемент '{locator_name}' (xpath: {xpath}) не содержит класс, "
            f"начинающийся с '{expected_class_start}'. Найденные классы: {class_list}")
        
        
    @allure.step('Проверка, что элемент "{locator_name}" не имеет класса, начинающегося с "{expected_class_start}"')
    def check_element_class_not_starts_with(self, locator_name: str, expected_class_start: str):
        xpath = ALL_LOCATORS.get(locator_name)
        if not xpath:
            raise ValueError(f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS")
        locator = self.page.locator(f"xpath={xpath}")
        class_list = locator.evaluate("element => Array.from(element.classList)")
        has_matching_class = any(cls.startswith(expected_class_start) for cls in class_list)
        assert not has_matching_class, (
            f"Элемент '{locator_name}' (xpath: {xpath}) содержит класс, "
            f"начинающийся с '{expected_class_start}'. Найденные классы: {class_list}")
    

    @allure.step('Проверка отсутствия элемента "{locator_name}" на странице')
    def check_element_not_present(self, locator_name: str, timeout: int = 30000):
        xpath = ALL_LOCATORS.get(locator_name)
        if not xpath:
            raise ValueError(f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS")
        locator = self.page.locator(f"xpath={xpath}")
        expect(locator).to_be_hidden(timeout=timeout)

    
    @allure.step('Проверка присутствия элемента "{locator_name}" на странице')
    def check_element_present(self, locator_name: str, timeout: int = 30000):
        xpath = ALL_LOCATORS.get(locator_name)
        if not xpath:
            raise ValueError(f"Локатор '{locator_name}' не найден в справочнике ALL_LOCATORS")
        locator = self.page.locator(f"xpath={xpath}")
        expect(locator).to_be_visible(timeout=timeout)

    @allure.step('Проверка значения поля по классу')
    def check_field_value_by_class(self, class_name: str, expected_value: str, timeout: int = 10000):
        try:
            locator = self.page.locator(f'.{class_name}')
            locator.wait_for(state='visible', timeout=timeout)
            if locator.evaluate('el => el.tagName.toLowerCase()') in ['input', 'textarea']:
                actual_value = locator.input_value()
            else:
                actual_value = locator.text_content() or locator.inner_text()
            if actual_value is None:
                raise ValueError(f"Не удалось получить значение элемента с классом '{class_name}'")
            actual_value = actual_value.strip()
            assert actual_value == expected_value, (
                f"Ожидаемое значение: '{expected_value}', "
                f"Фактическое значение: '{actual_value}'"
            )
        except Exception as e:
            allure.attach(
                f"Ошибка при проверке поля с классом '{class_name}': {str(e)}",
                name="Ошибка проверки"
            )
            print(f"(ОШИБКА) Проблема при проверке поля с классом '{class_name}': {e}")
            raise


    @allure.step('Проверка toast сообщения')
    def check_toast_message(self, locator_name: str, expected_value: str):
        print(f"Ищем toast с текстом: '{expected_value}'")
        locator = self.page.get_by_text(expected_value).first
        
        # expect автоматически выполняет retry с таймаутом
        expect(locator).to_be_visible()
        
        actual_value = locator.text_content().strip()
        print(f"Найден toast с текстом: '{actual_value}'")
        assert actual_value == expected_value, (
            f"Текст toast сообщения не совпадает.\n"
            f"Ожидалось: '{expected_value}'\n"
            f"Получено: '{actual_value}'"
        )