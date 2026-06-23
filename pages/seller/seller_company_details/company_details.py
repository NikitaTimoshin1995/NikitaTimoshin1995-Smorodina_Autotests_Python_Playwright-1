import allure
import pytest
import psycopg2
import requests
from psycopg2 import Error
from playwright.sync_api import Page, expect
from pages.seller.seller_auth_and_registration import SellerAuthRegistration
from Locators.loc_all_directories import ALL_LOCATORS
from Assertions.assertions import Assertions
from fixtures.all import intercept_requests, db_connection  
from playwright.sync_api import Page
from fixtures.all import db_connection
from Constants.seller.seller_settings.seller_company_data.const_company_data import (
    SELLER_COMPANY_DETAILS_URL
)
from Constants.seller.seller_auth.const_seller_auth import EXPECTED_URL_AFTER_LOGIN_SELLER
from Constants.admin.admin_auth.const_admin_auth import (
    ADMINN_LOGIN_REQUEST_URL,
    ADMIN_LOGIN1,
    ADMMIN_PASSWORD1
)
from Constants.admin.company.company_card.const_admin_company_card import ADMIN_COMPANY_DETAILS_PATCH
from Constants.seller.seller_registration.const_seller_registration import (
    SELLER_REGISTRATION_EMAIL4_COMPANY,
    SELLER_REGISTRATION_PASSWORD1,
    SELLER_REGISTRATION_NAME_COMPANY2,
    SELLER_REGISTRATION_PHONE2_COMPANY,
    SELLER_REGISTRATION_REPEAT_PASSWORD1
)

class CompanyDetails(SellerAuthRegistration):
    
    @allure.step('Переход в данные компании существующего продавца')
    def open_company_details_without_create(self, page: Page, login: str, password: str):
        assertions = Assertions(page)
        self.seller_auth(login, password)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        # Переход в настройки
        self.click_element('кнопка Настройки в меню продавца')  # Нажимаем "Настройки"
        self.click_element('кнопка Компания в меню продавца')  # Нажимаем "Компания"
        assertions.check_url(SELLER_COMPANY_DETAILS_URL)


    @allure.step('Переход в данные компании нового продавца')
    def open_company_details_with_create(self, page: Page, db_connection):
        assertions = Assertions(page)
        company_details =CompanyDetails(page)
        company_details.delete_user_and_related_data(db_connection, SELLER_REGISTRATION_EMAIL4_COMPANY)
        company_details.seller_registration(
            SELLER_REGISTRATION_NAME_COMPANY2, 
            SELLER_REGISTRATION_PHONE2_COMPANY, 
            SELLER_REGISTRATION_EMAIL4_COMPANY,
            SELLER_REGISTRATION_PASSWORD1, 
            SELLER_REGISTRATION_REPEAT_PASSWORD1, 
            True, True, True
        )
        assertions.check_user_in_db(db_connection,SELLER_REGISTRATION_EMAIL4_COMPANY, None, 2, 1)
        company_details.seller_confirm_phone(db_connection, SELLER_REGISTRATION_PHONE2_COMPANY)
        page.wait_for_timeout(2000)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        # Переход в настройки
        self.click_element('кнопка Настройки в меню продавца')  # Нажимаем "Настройки"
        self.click_element('кнопка Компания в меню продавца')  # Нажимаем "Компания"
        assertions.check_url(SELLER_COMPANY_DETAILS_URL)


    @allure.step("Заполнение контактов в данных компании продавца")
    def fill_company_details_contacts(self, fact_address, phone, email):
        # Очистка полей перед заполнением
        # self.fill_element('Контактная информация Факт. адрес', '')  # Очистка поля
        # self.fill_element('Контактная информация Телефон', '')    # Очистка поля
        # self.fill_element('Контактная информация E-mail', '')     # Очистка поля
        # Заполнение новыми значениями
        self.fill_element('Контактная информация Факт. адрес', fact_address)
        self.fill_element('Контактная информация Телефон', phone)
        self.fill_element('Контактная информация E-mail', email)
    

    @allure.step("Меняем статус оператора и проверяем изменение")
    def update_operator_status(self, db_connection, login: str, new_status: int):
        cursor = db_connection.cursor()
        try:
            # Проверяем текущий статус в новом соединении
            with db_connection.cursor() as check_cursor:
                check_cursor.execute("SELECT status FROM operators WHERE email = %s", (login,))
                current_status = check_cursor.fetchone()[0]
                print(f"Реальный текущий статус: {current_status}")
            # Обновляем статус
            update_query = "UPDATE operators SET status = %s WHERE email = %s"
            cursor.execute(update_query, (new_status, login))
            db_connection.commit()  # Явный коммит
            # Проверяем в новом соединении
            with db_connection.cursor() as verify_cursor:
                verify_cursor.execute("SELECT status FROM operators WHERE email = %s", (login,))
                updated_status = verify_cursor.fetchone()[0]
                print(f"Реальный новый статус: {updated_status}")
            if updated_status != new_status:
                raise ValueError(f"Статус не изменился в БД! Ожидалось: {new_status}, Фактически: {updated_status}")
            return True
        except Exception as e:
            db_connection.rollback()
            raise
        finally:
            cursor.close()
    

    @allure.step('Сохранение как было после регистрации')
    def patch_company_start(self):
        auth_url = ADMINN_LOGIN_REQUEST_URL
        auth_payload = {
            "login": ADMIN_LOGIN1,
            "password": ADMMIN_PASSWORD1
        }   
        auth_response = requests.post(auth_url, json=auth_payload) 
        if auth_response.status_code != 200:
            error_msg = f"Ошибка аутентификации"
            raise ValueError(error_msg)
        token = auth_response.json().get('token')
        if not token:
            raise ValueError("Токен не получен в ответе на аутентификацию")
        # Основной запрос
        url = ADMIN_COMPANY_DETAILS_PATCH
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload = {
            "type_company": "LEGAL",
            "state": "",
            "full_name": "Крокодилов Крокодил Крокодилович",
            "short_name": "Крокодилов Крокодил Крокодилович",
            "management_fio": None,
            "kpp": None,
            "ogrn": None,
            "inn": None,
            "opf_full": None,
            "address_legal": None,
            "bank_title": None,
            "bic": None,
            "payment_account": None,
            "address": None,
            "phone": "71234323423",
            "email": "avtotestsellersmorodina3@gmail.com",
            "manager": None,
            "vat_type_id": 10
        }    
        allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)      
        response = requests.patch(url, headers=headers, json=payload)        
        print("\n=== Response JSON ===")
        print(response.json())
        print("===================\n")      
        allure.attach(str(response.json()), name="Response JSON", attachment_type=allure.attachment_type.JSON)        
        if response.status_code != 200:
            error_msg = f"Ошибка при обновлении данных компании: {response.status_code}, {response.text}"
            allure.attach(error_msg, name="Error Response")
            raise ValueError(error_msg)          
        return response.json()
   

    @allure.step("Заполнение Информация для путешественников продавца")
    def fill_company_info(self, name, years, tours, description):
        self.fill_element('Инфо организатора имя', name)
        self.fill_element('Инфо организатора лет на рынке', years)
        self.fill_element('Инфо организатора проведенных туров', tours)
        self.fill_element('Инфо организатора описание', description)
   

    @allure.step("Обнуляем поля оператора и удаляем изображения")
    def delete_operator_info(self, db_connection, operator_id: int):
        cursor = db_connection.cursor()
        try:
            update_query = """
                UPDATE operators 
                SET logo = NULL, 
                    operator_full_name = NULL, 
                    how_many_years_market = NULL, 
                    number_tours_conducted = NULL, 
                    short_description = NULL 
                WHERE id = %s
            """
            cursor.execute(update_query, (operator_id,))
            delete_images_query = "DELETE FROM operator_images WHERE operator_id = %s"
            cursor.execute(delete_images_query, (operator_id,))
            db_connection.commit()
        except Exception as e:
            db_connection.rollback()
            raise
        finally:
            cursor.close()


    @allure.step("Загрузить фото в данных компании")
    def upload_photos_company(self, element_name: str, *file_paths, success_text: str = None):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            raise ValueError(f"Элемент '{element_name}' не найден в справочнике локаторов.")
        if not file_paths:
            raise ValueError("Не указаны пути к файлам для загрузки.")
        try:
            upload_element = self.page.locator(f'xpath={xpath}')
            with self.page.expect_file_chooser(timeout=60000) as fc_info:
                upload_element.click()
            file_chooser = fc_info.value
            file_chooser.set_files(list(file_paths))
            
            if success_text:
                self.page.wait_for_selector(
                    f"text={success_text}",
                    timeout=30000
                )
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_upload_failed",
                attachment_type=allure.attachment_type.PNG
            )
            raise Exception(f"Ошибка при загрузке файлов: {str(e)}")

    