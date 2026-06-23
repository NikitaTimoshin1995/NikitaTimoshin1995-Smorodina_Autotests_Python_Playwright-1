import allure
from Assertions.seller.seller_company_details.assert_seller_company_details import AssertionsCompanyDetails
from playwright.sync_api import Page
from Locators.loc_all_directories import LOC_SELLER_COMPANY_DATA
from Locators.loc_all_directories import ALL_LOCATORS
import time
from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    #Предупреждения
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING1,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING2,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING4,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING5,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING6,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING7,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING8,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING9,
    С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10,
)

class AssertionsCompanyDetailsLegal(AssertionsCompanyDetails):

#Проверки Юр.Лиц
    @allure.step("Проверка, что данные юридического лица сохранились")
    def check_legal_in_db(self, db_connection, login: str, inn: str, opf_full: str, full_name: str,
                        short_name: str, address_legal: str, kpp: str, ogrn: str,
                        payment_account: str, bic: str, bank_title: str, management_fio: str,
                        state: str, address: str, phone: str, email: str, nds: int):
        cursor = db_connection.cursor()
        # Первый запрос для получения user_id
        query_user_id = "SELECT id FROM users WHERE email = %s"
        cursor.execute(query_user_id, (login,))
        user_id = cursor.fetchone()
        assert user_id is not None, f"Пользователь с логином: {login} не найден в базе данных."
        user_id = user_id[0]  # Получаем id пользователя
        # Второй запрос для получения profile_id
        query_profile_id = "SELECT profile_id FROM profiles WHERE user_id = %s"
        cursor.execute(query_profile_id, (user_id,))
        profile_id = cursor.fetchone()
        assert profile_id is not None, f"Профиль для пользователя с id: {user_id} не найден в базе данных."
        profile_id = profile_id[0]  # Получаем profile_id
        # Третий запрос для получения данных профиля, включая новые поля
        query_profile_data = """
            SELECT inn, opf_full, full_name, short_name, address_legal, kpp, ogrn, 
                payment_account, bic, bank_title, management_fio, state, address, phone, email, vat_type_id
            FROM profiles_legal WHERE id = %s
        """
        cursor.execute(query_profile_data, (profile_id,))
        profile_data = cursor.fetchone()
        cursor.close()
        assert profile_data is not None, f"Данные профиля с id: {profile_id} не найдены в базе данных."
        # Распаковываем полученные данные
        (db_inn, db_opf_full, db_full_name, db_short_name, db_address_legal,
        db_kpp, db_ogrn, db_payment_account, db_bic, db_bank_title,
        db_management_fio, db_state, db_address, db_phone, db_email, db_nds) = profile_data
        # Проверяем каждое значение
        assert db_inn == inn, f"ИНН не совпадает. Ожидалось: {inn}, но получено: {db_inn}"
        assert db_opf_full == opf_full, f"Полное наименование ОПФ не совпадает. Ожидалось: {opf_full}, но получено: {db_opf_full}"
        assert db_full_name == full_name, f"Полное наименование не совпадает. Ожидалось: {full_name}, но получено: {db_full_name}"
        assert db_short_name == short_name, f"Краткое наименование не совпадает. Ожидалось: {short_name}, но получено: {db_short_name}"
        assert db_address_legal == address_legal, f"Юридический адрес не совпадает. Ожидалось: {address_legal}, но получено: {db_address_legal}"
        assert db_kpp == kpp, f"КПП не совпадает. Ожидалось: {kpp}, но получено: {db_kpp}"
        assert db_ogrn == ogrn, f"ОГРН не совпадает. Ожидалось: {ogrn}, но получено: {db_ogrn}"
        assert db_payment_account == payment_account, f"Расчетный счет не совпадает. Ожидалось: {payment_account}, но получено: {db_payment_account}"
        assert db_bic == bic, f"БИК не совпадает. Ожидалось: {bic}, но получено: {db_bic}"
        assert db_bank_title == bank_title, f"Название банка не совпадает. Ожидалось: {bank_title}, но получено: {db_bank_title}"
        assert db_management_fio == management_fio, f"ФИО управляющего не совпадает. Ожидалось: {management_fio}, но получено: {db_management_fio}"
        assert db_state == state, f"Статус не совпадает. Ожидалось: {state}, но получено: {db_state}"
        assert db_address == address, f"Адрес не совпадает. Ожидалось: {address}, но получено: {db_address}"
        assert db_phone == phone, f"Телефон не совпадает. Ожидалось: {phone}, но получено: {db_phone}"
        assert db_email == email, f"Email не совпадает. Ожидалось: {email}, но получено: {db_email}"
        assert db_nds == nds, f"НДС не совпадает. Ожидалось: {nds}, но получено: {db_nds}"


    @allure.step("Проверка state оператора на фронте")
    def check_operator_legal_state_front(self, page: Page, state: str, timeout_seconds: int = 120, check_interval_seconds: int = 5):
        state_xpath = LOC_SELLER_COMPANY_DATA['STATE Юр.лица в данных компании']
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


    @allure.step("Проверка, что поля у Юридического лица неактивны")
    def check_operator_legal_inactive_fields(self, locator):
        with allure.step("Проверка, что поле 'Юр ОПФ' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр ОПФ'])
        with allure.step("Проверка, что поле 'Юр Полное наименование' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр Полное наименование'])
        with allure.step("Проверка, что поле 'Юр Краткое наименование' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр Краткое наименование'])
        with allure.step("Проверка, что поле 'Юр Юр. адрес' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр Юр. адрес'])
        with allure.step("Проверка, что поле 'Юр КПП' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр КПП'])
        with allure.step("Проверка, что поле 'Юр ОГРН' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр ОГРН'])
        with allure.step("Проверка, что поле 'Юр Р. / счёт' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр Р. / счёт'])
        with allure.step("Проверка, что поле 'Юр БИК' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр БИК'])
        with allure.step("Проверка, что поле 'Юр Банк' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр Банк'])
        with allure.step("Проверка, что поле 'Юр ФИО ген. директора' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Юр ФИО ген. директора'])
        with allure.step("Проверка, что поле 'Тип НДС, %' неактивно"):
            self.check_element_class_starts_with(f'Юр все НДС{locator} блокировка', 'p-disabled')  
        with allure.step("Проверка, что поле 'Контактная информация Факт. адрес' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Контактная информация Факт. адрес'])
        with allure.step("Проверка, что поле 'Контактная информация Телефон' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Контактная информация Телефон'])
        with allure.step("Проверка, что поле 'Контактная информация E-mail' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Контактная информация E-mail'])
        with allure.step("Проверка, что поле 'Инфо организатора имя' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Инфо организатора имя'])
        with allure.step("Проверка, что поле 'Инфо организатора лет на рынке' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Инфо организатора лет на рынке'])
        with allure.step("Проверка, что поле 'Инфо организатора проведенных туров' неактивно"):
            self.check_element_disabled_by_xpath(ALL_LOCATORS['Инфо организатора проведенных туров'])
        with allure.step("Проверка, что поле 'Инфо организатора описание' неактивно"):
            self.check_element_class_starts_with('Инфо организатора описание активен или нет', '_disabled') 

        
    @allure.step("Проверка, что поля у Юридического лица активны")
    def check_operator_legal_active_fields(self, locator):
        with allure.step("Проверка, что поле 'Правовая форма' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Правовая форма'])
        with allure.step("Проверка, что поле 'Юр ИНН' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр ИНН'])
        with allure.step("Проверка, что поле 'Юр ОПФ' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр ОПФ'])
        with allure.step("Проверка, что поле 'Юр Полное наименование' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр Полное наименование'])
        with allure.step("Проверка, что поле 'Юр Краткое наименование' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр Краткое наименование'])
        with allure.step("Проверка, что поле 'Юр Юр. адрес' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр Юр. адрес'])
        with allure.step("Проверка, что поле 'Юр КПП' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр КПП'])
        with allure.step("Проверка, что поле 'Юр ОГРН' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр ОГРН'])
        with allure.step("Проверка, что поле 'Юр Р. / счёт' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр Р. / счёт'])
        with allure.step("Проверка, что поле 'Юр БИК' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр БИК'])
        with allure.step("Проверка, что поле 'Юр Банк' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр Банк'])
        with allure.step("Проверка, что поле 'Юр ФИО ген. директора' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Юр ФИО ген. директора'])
        with allure.step("Проверка, что поле 'Тип НДС, %' активно"):
            self.check_element_class_not_starts_with(f'Юр все НДС{locator} блокировка', 'p-disabled')
        with allure.step("Проверка, что поле 'Контактная информация Факт. адрес' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Контактная информация Факт. адрес'])
        with allure.step("Проверка, что поле 'Контактная информация Телефон граница красная' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Контактная информация Телефон'])
        with allure.step("Проверка, что поле 'Контактная информация E-mail' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Контактная информация E-mail'])
        with allure.step("Проверка, что поле 'Инфо организатора имя' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора имя'])
        with allure.step("Проверка, что поле 'Инфо организатора лет на рынке' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора лет на рынке'])
        with allure.step("Проверка, что поле 'Инфо организатора проведенных туров' неактивно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора проведенных туров'])
        with allure.step("Проверка, что поле 'Инфо организатора описание' неактивно"):
            self.check_element_class_not_starts_with('Инфо организатора описание активен или нет', '_disabled') 


    @allure.step("Проверка, что поля у Юридического лица содержат переданный текст из дадата")
    def check_operator_legal_fields_with_text(self, opf, full_name, short_name, address, kpp, ogrn):
        with allure.step("Проверка 'Юр ОПФ'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ОПФ'], opf)
        with allure.step("Проверка 'Юр Полное наименование'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Полное наименование'], full_name)
        with allure.step("Проверка 'Юр Краткое наименование'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Краткое наименование'], short_name)
        with allure.step("Проверка 'Юр Юр. адрес'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Юр. адрес'], address)
        with allure.step("Проверка 'Юр КПП'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр КПП'], kpp)
        with allure.step("Проверка 'Юр ОГРН'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ОГРН'], ogrn)


    @allure.step("Проверка, что все поля у Юридического лица содержат переданный текст ")
    def check_operator_legal_all_fields_with_text(self, inn, opf, fullname, shortname, legal_address, kpp, ogrn, bill, bic, bank, director, fact_address, phone, email):
        with allure.step("Проверка 'Юр ИНН'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ИНН'], inn)
        with allure.step("Проверка 'Юр ОПФ'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ОПФ'], opf)
        with allure.step("Проверка 'Юр Полное наименование'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Полное наименование'], fullname)
        with allure.step("Проверка 'Юр Краткое наименование'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Краткое наименование'], shortname)
        with allure.step("Проверка 'Юр Юр. адрес'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Юр. адрес'], legal_address)
        with allure.step("Проверка 'Юр КПП'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр КПП'], kpp)
        with allure.step("Проверка 'Юр ОГРН'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ОГРН'], ogrn)
        with allure.step("Проверка 'Юр Р. / счёт'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Р. / счёт'], bill)
        with allure.step("Проверка 'Юр БИК'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр БИК'], bic)
        with allure.step("Проверка 'Юр Банк'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр Банк'], bank)
        with allure.step("Проверка 'Юр ФИО ген. директора'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Юр ФИО ген. директора'], director)
        with allure.step("Проверка 'Контактная информация Факт. адрес'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Контактная информация Факт. адрес'], fact_address)
        with allure.step("Проверка 'Контактная информация Телефон'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Контактная информация Телефон'], phone)
        with allure.step("Проверка 'Контактная информация E-mail'"):
            self.check_input_value_by_xpath(ALL_LOCATORS['Контактная информация E-mail'], email)


    @allure.step("Проверка, что информация организатора сохранились")
    def check_operator_info_in_db(self, db_connection, login: str, operator_full_name: str, how_many_years_market, number_tours_conducted, short_description: str):
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
                query_operator_data = "SELECT operator_full_name, how_many_years_market, number_tours_conducted, short_description FROM operators WHERE admin_id = %s"
                cursor.execute(query_operator_data, (user_id,))
                operator_data = cursor.fetchone()
                cursor.close()
                if operator_data is None:
                    time.sleep(interval)
                    elapsed += interval
                    continue
                (db_operator_full_name, db_how_many_years_market, db_number_tours_conducted, db_short_description) = operator_data
                check_name = db_operator_full_name == operator_full_name
                check_years = (db_how_many_years_market == how_many_years_market) if how_many_years_market is None else (db_how_many_years_market == int(how_many_years_market))
                check_tours = (db_number_tours_conducted == number_tours_conducted) if number_tours_conducted is None else (db_number_tours_conducted == int(number_tours_conducted))
                check_desc = db_short_description == short_description
                if check_name and check_years and check_tours and check_desc:
                    return      
            except Exception:
                pass 
            time.sleep(interval)
            elapsed += interval
        assert False, f"Данные оператора не совпадают. Полное имя: ожидалось {operator_full_name}, получено {db_operator_full_name}. Лет на рынке: ожидалось {how_many_years_market}, получено {db_how_many_years_market}. Проведено туров: ожидалось {number_tours_conducted}, получено {db_number_tours_conducted}. Описание: ожидалось {short_description}, получено {db_short_description}"


    @allure.step("Проверка, что поля 'Инфо организатора' активны")
    def check_operator_info_fields_active(self):
        with allure.step("Проверка, что поле 'Инфо организатора имя' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора имя'])
        with allure.step("Проверка, что поле 'Инфо организатора лет на рынке' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора лет на рынке'])
        with allure.step("Проверка, что поле 'Инфо организатора проведенных туров' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора проведенных туров'])
        with allure.step("Проверка, что поле 'Инфо организатора описание' активно"):
            self.check_element_enabled_by_xpath(ALL_LOCATORS['Инфо организатора описание'])


    @allure.step("Проверка, что поля у Инфо организатора содержат переданный текст")
    def check_operator_org_info_fields_with_text(self, name, years, tours, description):
        timeout = 30
        interval = 2
        elapsed = 0  
        while elapsed < timeout:
            try:
                with allure.step("Проверка 'Инфо организатора имя'"):
                    self.check_field_value_from_locator('Инфо организатора имя', name)
                with allure.step("Проверка 'Инфо организатора лет на рынке'"):
                    self.check_field_value_from_locator('Инфо организатора лет на рынке', years)
                with allure.step("Проверка 'Инфо организатора проведенных туров'"):
                    self.check_field_value_from_locator('Инфо организатора проведенных туров', tours)
                with allure.step("Проверка 'Инфо организатора описание'"):
                    self.check_field_value_from_locator('Инфо организатора описание', description)
                return
            except AssertionError:
                if elapsed + interval >= timeout:
                    raise
                time.sleep(interval)
                elapsed += interval
        raise AssertionError(f"Поля Инфо организатора не содержат ожидаемый текст после {timeout} секунд ожидания")
    

    @allure.step("Проверка, что поля не выделенны красным")
    def check_operator_legal_fields_border_normal(self):
        self.check_element_class_not_starts_with('Юр.лицо граница', '_inputError')
        self.check_element_class_not_starts_with('Юр ИНН граница', '_inputError')
        self.check_element_class_not_starts_with('Юр ОПФ граница', '_inputError')
        self.check_element_class_not_starts_with('Юр Полное наименование граница', '_inputError')
        self.check_element_class_not_starts_with('Юр Краткое наименование граница', '_inputError')
        self.check_element_class_not_starts_with('Юр Юр. адрес граница', '_inputError')
        self.check_element_class_not_starts_with('Юр КПП граница', '_inputError')
        self.check_element_class_not_starts_with('Юр ОГРН граница', '_inputError')
        self.check_element_class_not_starts_with('Юр Р. / счёт граница', '_inputError')
        self.check_element_class_not_starts_with('Юр БИК граница', '_inputError')
        self.check_element_class_not_starts_with('Юр Банк граница', '_inputError')
        self.check_element_class_not_starts_with('Юр ФИО ген. директора граница', '_inputError')
        self.check_element_class_not_starts_with('Юр все НДС1 граница', '_inputError')
        self.check_element_class_not_starts_with('Контактная информация Факт. адрес граница', '_inputError')
        self.check_element_class_not_starts_with('Контактная информация Телефон граница', '_inputError')
        self.check_element_class_not_starts_with('Контактная информация E-mail граница', '_inputError')
        self.check_element_class_not_starts_with('Инфо организатора имя граница', '_inputError')
        self.check_element_class_not_starts_with('Инфо организатора лет на рынке граница', '_inputError')
        self.check_element_class_not_starts_with('Инфо организатора проведенных туров граница', '_inputError')
        self.check_element_class_not_starts_with('Инфо организатора описание граница', '_inputError')
        

    @allure.step("Проверка, что поля выделенны красным неполная")
    def check_operator_legal_fields_border_short_red(self):
        self.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        self.check_element_class_starts_with('Юр ОПФ граница', '_inputError')
        self.check_element_class_starts_with('Юр Юр. адрес граница', '_inputError')
        self.check_element_class_starts_with('Юр КПП граница', '_inputError')
        self.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        self.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        self.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        self.check_element_class_starts_with('Юр Банк граница красная', '_inputError')
        self.check_element_class_starts_with('Юр ФИО ген. директора граница', '_inputError')
        self.check_element_class_starts_with('Контактная информация Факт. адрес граница красная', '_inputError')
        self.check_element_class_starts_with('Инфо организатора имя граница', '_errorName')
        self.check_element_class_starts_with('Инфо организатора описание граница красная', '_errorDescription')


    @allure.step("Проверка, что поля выделенны красным полная")
    def check_operator_legal_fields_border_full_red(self):
        self.check_element_class_starts_with('Юр ИНН граница', '_inputError')
        self.check_element_class_starts_with('Юр ОПФ граница', '_inputError')
        self.check_element_class_starts_with('Юр Полное наименование граница красная', '_inputError')
        self.check_element_class_starts_with('Юр Краткое наименование граница' , '_inputError')
        self.check_element_class_starts_with('Юр Юр. адрес граница', '_inputError')
        self.check_element_class_starts_with('Юр КПП граница', '_inputError')
        self.check_element_class_starts_with('Юр ОГРН граница красная', '_inputError')
        self.check_element_class_starts_with('Юр Р. / счёт граница', '_inputError')
        self.check_element_class_starts_with('Юр БИК граница красная', '_inputError')
        self.check_element_class_starts_with('Юр Банк граница красная', '_inputError')
        self.check_element_class_starts_with('Юр ФИО ген. директора граница', '_inputError')
        self.check_element_class_starts_with('Контактная информация Факт. адрес граница красная', '_inputError')
        self.check_element_class_starts_with('Контактная информация Телефон граница красная', '_inputError')
        self.check_element_class_starts_with('Контактная информация E-mail граница красная', '_inputError')
        self.check_element_class_starts_with('Инфо организатора имя граница', '_errorName')
        self.check_element_class_starts_with('Инфо организатора описание граница красная', '_errorDescription')
 

    @allure.step("Проверка, вывода ошибок неполная")
    def check_operator_legal_fields_errors_short(self):
        self.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING1)
        self.check_field_value_from_locator('Юр ИНН предепреждение2', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING2)
        self.check_field_value_from_locator('Юр ОПФ предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр Юр. адрес предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING4)
        self.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING5)
        self.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING6)
        self.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING7)
        self.check_field_value_from_locator('Юр Банк предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр ФИО ген. директора предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Контактная информация Факт. адрес предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Инфо организатора имя предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10)
        self.check_field_value_from_locator('Инфо организатора описание предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10)


    @allure.step("Проверка, вывода ошибок полная")
    def check_operator_legal_fields_errors_full(self):
        self.check_field_value_from_locator('Юр ИНН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING2)
        self.check_field_value_from_locator('Юр ОПФ предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр Полное наименование предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр Краткое наименование предепреждение2', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр Юр. адрес предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр КПП предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING4)
        self.check_field_value_from_locator('Юр ОГРН предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING5)
        self.check_field_value_from_locator('Юр Р. / счёт предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING6)
        self.check_field_value_from_locator('Юр БИК предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING7)
        self.check_field_value_from_locator('Юр Банк предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Юр ФИО ген. директора предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Контактная информация Факт. адрес предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Контактная информация Телефон предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING8)
        self.check_field_value_from_locator('Контактная информация E-mail предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING3)
        self.check_field_value_from_locator('Инфо организатора имя предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10)
        self.check_field_value_from_locator('Инфо организатора описание предепреждение1', С_SELLER_INPUT_COMPANY_LEGAL_INN_WARNING10)


