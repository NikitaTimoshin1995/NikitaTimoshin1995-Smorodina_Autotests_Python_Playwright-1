import allure
from  Assertions.seller.seller_company_details.assert_seller_company_details import AssertionsCompanyDetails
from playwright.sync_api import Page
from Locators.loc_all_directories import LOC_SELLER_COMPANY_DATA
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsCompanyDetailsIp(AssertionsCompanyDetails):

    @allure.step("Проверка, что данные ИП сохранились")
    def check_ip_in_db(self, db_connection, login: str, inn: str, full_name: str, ogrn: str, payment_account: str, bic: str, bank_title: str,
                        state: str, address: str, phone: str, email: str, nds: int):
        cursor = db_connection.cursor()
        # Получение user_id по логину
        query_user_id = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query_user_id, (login,))
        user_id = cursor.fetchone()
        assert user_id is not None, f"Пользователь с логином: {login} не найден в базе данных."
        user_id = user_id[0]
        # Получение profile_id по user_id
        query_profile_id = "SELECT profile_id FROM profiles WHERE user_id = %s"
        cursor.execute(query_profile_id, (user_id,))
        profile_id = cursor.fetchone()
        assert profile_id is not None, f"Профиль для пользователя с id: {user_id} не найден в базе данных."
        profile_id = profile_id[0]
        # Получение данных профиля по profile_id
        query_profile_data = """
            SELECT inn, full_name, ogrn, payment_account, bic, bank_title, state, address, phone, email, vat_type_id
            FROM profiles_ip WHERE id = %s
        """
        cursor.execute(query_profile_data, (profile_id,))
        profile_data = cursor.fetchone()
        cursor.close()
        assert profile_data is not None, f"Данные профиля с id: {profile_id} не найдены в базе данных."
        (db_inn, db_full_name, db_ogrn, db_payment_account, db_bic, db_bank_title, db_state, db_address, db_phone, db_email, db_vat_type_id) = profile_data
        assert db_inn == inn, f"ИНН не совпадает. Ожидалось: {inn}, но получено: {db_inn}"
        assert db_full_name == full_name, f"Полное имя не совпадает. Ожидалось: {full_name}, но получено: {db_full_name}"
        assert db_ogrn == ogrn, f"ОГРН не совпадает. Ожидалось: {ogrn}, но получено: {db_ogrn}"
        assert db_payment_account == payment_account, f"Расчетный счет не совпадает. Ожидалось: {payment_account}, но получено: {db_payment_account}"
        assert db_bic == bic, f"БИК не совпадает. Ожидалось: {bic}, но получено: {db_bic}"
        assert db_bank_title == bank_title, f"Название банка не совпадает. Ожидалось: {bank_title}, но получено: {db_bank_title}"
        assert db_state == state, f"Статус не совпадает. Ожидалось: {state}, но получено: {db_state}"
        assert db_address == address, f"Адрес не совпадает. Ожидалось: {address}, но получено: {db_address}"
        assert db_phone == phone, f"Телефон не совпадает. Ожидалось: {phone}, но получено: {db_phone}"
        assert db_email == email, f"Email не совпадает. Ожидалось: {email}, но получено: {db_email}"
        assert db_vat_type_id == nds, f"НДС не совпадает. Ожидалось: {nds}, но получено: {db_vat_type_id}"


    @allure.step("Проверка state оператора на фронте ИП")
    def check_operator_ip_state_front(self, page: Page, state: str, timeout_seconds: int = 120, check_interval_seconds: int = 5):
        state_xpath = LOC_SELLER_COMPANY_DATA['STATE ИП в данных компании']
        state_element = page.locator(f'xpath={state_xpath}')
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            try:
                state_element.wait_for(state="visible", timeout=check_interval_seconds * 1000)
                actual_state = state_element.text_content()
                if actual_state == state:
                    return
            except:
                pass
            time.sleep(check_interval_seconds)
        final_actual_state = state_element.text_content() if state_element.count() > 0 else "Элемент не найден или не виден"
        assert False, f"Время ожидания истекло ({timeout_seconds} секунд). Ожидаемый статус: '{state}', фактический статус: '{final_actual_state}'"


    @allure.step("Проверка, что поля у ИП неактивны")
    def check_operator_ip_inactive_fields(self, locator):
        with allure.step("Проверка, что поле 'ИП ФИО' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['ИП ФИО'])
        with allure.step("Проверка, что поле 'ИП ОГРН' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['ИП ОГРН'])
        with allure.step("Проверка, что поле 'ИП Р. / счёт' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['ИП Р. / счёт'])
        with allure.step("Проверка, что поле 'ИП БИК' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['ИП БИК'])
        with allure.step("Проверка, что поле 'ИП Банк' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['ИП Банк'])
            self.check_element_class_starts_with(f'ИП все НДС{locator} блокировка', 'p-disabled') 


    @allure.step("Проверка, что поля у ИП активны")
    def check_operator_ip_active_fields(self, locator):
        with allure.step("Проверка, что поле 'ИП ФИО' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['ИП ФИО'])
        with allure.step("Проверка, что поле 'ИП ОГРН' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['ИП ОГРН'])
        with allure.step("Проверка, что поле 'ИП Р. / счёт' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['ИП Р. / счёт'])
        with allure.step("Проверка, что поле 'ИП БИК' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['ИП БИК'])
        with allure.step("Проверка, что поле 'ИП Банк' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['ИП Банк'])
            self.check_element_class_not_starts_with(f'ИП все НДС{locator} блокировка', 'p-disabled') 


    @allure.step("Проверка, что поля у ИП содержат переданный текст")
    def check_operator_ip_fields_with_text(self, full_name, ogrn ):
        with allure.step("Проверка 'ИП ФИО'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['ИП ФИО'], full_name)
        with allure.step("Проверка 'ИП ОГРН'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['ИП ОГРН'], ogrn)

        