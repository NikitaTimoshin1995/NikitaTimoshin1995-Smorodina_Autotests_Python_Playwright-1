import allure
from playwright.sync_api import Page
from pages.base import BasePage
from Constants.const_general import URL
from fixtures.all import db_connection

class SellerAuthRegistration(BasePage):

    @allure.step("Авторизация продавца выбор всех согласий")
    def choose_all_agreements(self):
        self.click_element('Чекбокс согласия на обработку данных в авторизации продавца')
        self.click_element('Чекбокс согласия с пользовательским соглашением в авторизации продавца')
        self.click_element('Чекбокс согласия с политикой обработки данных в авторизации продавца')


    @allure.step("Авторизация продавца")
    def seller_auth(self, page: Page, login: str, password: str, ):
        self.allow_location_access()  # Разрешаем доступ к местоположению
        self.open_page(URL)  # Открываем главную страницу
        self.wait_for_full_load()
        self.click_element_if_present('кнопка закрыть поппап2')
        self.close_livechat_if_present()
        self.close_subscription_if_present()
        self.page.wait_for_timeout(2500)
        self.click_element('Кнопка Принять куки')
        self.page.wait_for_timeout(1500)
        self.click_element_if_present('кнопка Я здесь')
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Войти по почте')  # Нажимаем "Организатор туров"
        self.fill_element('поле Логин', login)  # Заполняем email
        self.fill_element('поле Пароль', password)  # Заполняем пароль
        self.choose_all_agreements()
        self.click_element('кнопка Вход в авторизации продавца')  # Отправляем форму входа
        page.wait_for_timeout(1000)
        self.save_auth_cookies(page)
        self.open_page('https://dev.smorodina.ru/operator/summary')
        self.wait_for_full_load()  # Ожидаем полной загрузки страницы


    allure.step("Регистрация продавца")
    def seller_registration(self, seller_company_name, seller_profile_phone, seller_profile_email, 
                            seller_password, seller_repeat_password, personal_consent=True, accept_policy=True, 
                            accept_user_agreement=True, accept_promotional_materials=True):
        self.open_page(URL)  # Открываем главную страницу
        self.allow_location_access()  # Разрешаем доступ к местоположению
        self.click_element_if_present('кнопка Я здесь')
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.click_element('кнопка Создать аккаунт организатора')  # Нажимаем "Создать аккаунт организатора"
        self.fill_element('поле Название компании',  seller_company_name),
        self.fill_element('поле Номер телефона', seller_profile_phone),
        self.fill_element('поле Email', seller_profile_email),
        self.fill_element('поле Придумайте пароль', seller_password),
        self.fill_element('поле Пароль еще раз', seller_repeat_password)
        if personal_consent:
            self.click_element('Чекбокс Обработку персональных данных в регистрации продавца')
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        if accept_promotional_materials:
            self.click_element('Соглашаюсь получать рекламные материалы')
        self.click_element('кнопка Зарегистрироваться')  
        with self.page.expect_response("https://dev.smorodina.ru/api/register/operator") as response_info:
            self.click_element('кнопка Зарегистрироваться')  # Нажимаем кнопку регистрации
       
    allure.step("Заполнение данных продавца при регистрации")
    def seller_registration_only_fill(self, seller_company_name, seller_profile_phone, seller_profile_email, 
                            seller_password, seller_repeat_password, personal_consent=True, accept_policy=True, 
                            accept_user_agreement=True, accept_promotional_materials=True):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.click_element('кнопка Создать аккаунт организатора')  # Нажимаем "Создать аккаунт организатора"
        self.fill_element('поле Название компании',  seller_company_name),
        self.fill_element('поле Номер телефона', seller_profile_phone),
        self.fill_element('поле Email', seller_profile_email),
        self.fill_element('поле Придумайте пароль', seller_password),
        self.fill_element('поле Пароль еще раз', seller_repeat_password)
        if personal_consent:
            self.click_element('Чекбокс Обработку персональных данных в регистрации продавца')
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        if accept_promotional_materials:
            self.click_element('Соглашаюсь получать рекламные материалы')
        

    @allure.step("Подтверждение телефона")
    def seller_confirm_phone(self, conn, phone):
        cursor = conn.cursor()
        cursor.execute("SELECT confirmation_code FROM users_phone_temp WHERE phone = %s", (phone,))
        result = cursor.fetchone()  # Извлекаем результат
        if result is None:
            raise ValueError(f"Код подтверждения не найден для: {phone}")
        confirmation_code = result[0]  # Получаем код подтверждения
        digits = list(str(confirmation_code))  # Преобразуем код в список цифр
        # Вводим каждую цифру кода подтверждения
        self.fill_element('Первая цифра', digits[0])
        self.fill_element('Вторая цифра', digits[1])
        self.fill_element('Третья цифра', digits[2])
        self.fill_element('Четвертая цифра', digits[3])
        

    @allure.step("Удалить продавца(ов) и связанные данные из базы данных")
    def delete_user_and_related_data(self, conn, email_or_login: str):
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id FROM users WHERE login=%s OR email=%s",
                (email_or_login, email_or_login)
            )
            results = cursor.fetchall()
            if not results:
                print(f"Пользователи с email/логином {email_or_login} не найдены. Переход к следующему шагу.")
                allure.attach(f"Пользователи {email_or_login} не найдены", name="Информация")
                return False
            user_ids = [row[0] for row in results]
            print(f"Найдено пользователей для удаления: {len(user_ids)}")
            for user_id in user_ids:
                print(f"Удаление данных для user_id: {user_id}")
                # Удаляем связанные данные
                cursor.execute("DELETE FROM operator_user_rule WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM operator_users WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM profiles WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM profiles_legal WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM users_email_temp WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM sys_users WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM sys_user_logs WHERE user_id=%s", (user_id,))
                cursor.execute("DELETE FROM operators WHERE admin_id=%s", (user_id,))
            # Удаляем основных пользователей
            cursor.execute("DELETE FROM users WHERE login=%s OR email=%s", (email_or_login, email_or_login))
            conn.commit()
            
            allure.attach(f"Удалено {len(user_ids)} пользователей с email/логином '{email_or_login}'", 
                        name="Успешное удаление")
            print(f"Успешно удалено {len(user_ids)} пользователей")
            return True
        except Exception as e:
            conn.rollback()
            error_msg = f"Ошибка при удалении пользователей: {str(e)}"
            allure.attach(error_msg, name="Ошибка")
            raise Exception(error_msg)
        finally:
            cursor.close()
    

    @allure.step("Заполнение паролей для регистрации продавца")
    def seller_registration_fill_passwords(self, password1: str, password2: str):
        self.fill_element('поле Придумайте пароль', password1)
        self.fill_element('поле Пароль еще раз', password2)
        self.click_element('кнопка Зарегистрироваться')
    
    
    @allure.step("Заполнение согласий для регистрации продавца")
    def handle_agreements(self, personal_consent, accept_policy, accept_user_agreement, accept_promotional_materials):
        if personal_consent:
            self.click_element('Чекбокс Обработку персональных данных в регистрации продавца')
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        if accept_promotional_materials:
            self.click_element('Соглашаюсь получать рекламные материалы')
