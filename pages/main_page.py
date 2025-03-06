import allure
from pages.base import BasePage
from data.constants import URL
from fixtures.all import db_connection

class MainPage(BasePage):
    @allure.step("Авторизация продавца")
    def seller_auth(self, login: str, password: str):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element('кнопка Искать туры')  # Нажимаем "Искать туры"
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.fill_element('поле Логин', login)  # Заполняем email
        self.fill_element('поле Пароль', password)  # Заполняем пароль
        self.click_element('кнопка Вход в авторизации продавца')  # Отправляем форму входа
        self.wait_for_full_load()  # Ожидаем полной загрузки страницы

    allure.step("Регистрация продавца")
    def seller_registration(self, seller_company_name, seller_profile_phone, seller_profile_email, 
                            seller_password, seller_repeat_password, accept_policy=True, 
                            accept_user_agreement=True, accept_promotional_materials=True):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element('кнопка Искать туры')  # Нажимаем "Искать туры"
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.click_element('кнопка Создать аккаунт организатора')  # Нажимаем "Создать аккаунт организатора"
        self.fill_element('поле Название компании',  seller_company_name),
        self.fill_element('поле Номер телефона', seller_profile_phone),
        self.fill_element('поле Email', seller_profile_email),
        self.fill_element('поле Придумайте пароль', seller_password),
        self.fill_element('поле Пароль еще раз', seller_repeat_password)
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        if accept_promotional_materials:
            self.click_element('Соглашаюсь получать рекламные материалы')
        self.click_element('кнопка Зарегистрироваться')  
        with self.page.expect_response("https://dev.smorodina.ru/api/register/operator") as response_info:
            self.click_element('кнопка Зарегистрироваться')  # Нажимаем кнопку регистрации
        response = response_info.value  # Получаем объект ответа
        # Далее можно добавить проверку ответа, если нужно
        assert response.status == 200, f"Запрос вернул неожидаемый статус: {response.status}"
    

    allure.step("Заполнение данных продавца при регистрации")
    def seller_registration_only_fill(self, seller_company_name, seller_profile_phone, seller_profile_email, 
                            seller_password, seller_repeat_password, accept_policy=True, 
                            accept_user_agreement=True, accept_promotional_materials=True):
        self.open_page(URL)  # Открываем главную страницу
        self.click_element('кнопка Искать туры')  # Нажимаем "Искать туры"
        self.click_element('кнопка Вход')  # Нажимаем "Войти"
        self.click_element('кнопка Организатор туров')  # Нажимаем "Организатор туров"
        self.click_element('кнопка Создать аккаунт организатора')  # Нажимаем "Создать аккаунт организатора"
        self.fill_element('поле Название компании',  seller_company_name),
        self.fill_element('поле Номер телефона', seller_profile_phone),
        self.fill_element('поле Email', seller_profile_email),
        self.fill_element('поле Придумайте пароль', seller_password),
        self.fill_element('поле Пароль еще раз', seller_repeat_password)
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        
        

        
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
        


    @allure.step("Удалить пользователя и связанные данные из базы данных")
    def delete_user_and_related_data(self, conn, email_or_login: str, company_name: str):
        cursor = conn.cursor()

        # Получаем user_id
        cursor.execute(
            "SELECT id FROM users WHERE login=%s OR email=%s",
            (email_or_login, email_or_login)
        )
        result = cursor.fetchone()
        
        # Если пользователь не найден, просто завершаем выполнение метода
        if result is None:
            print(f"Пользователь с email/логином {email_or_login} не найден. Переход к следующему шагу.")
            cursor.close()
            return  # Или можно использовать "return None" для явного указания, что ничего не было сделано

        user_id = result[0]

        # Удаляем связанные данные
        cursor.execute("DELETE FROM operator_user_rule WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM operator_users WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM profiles WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM profiles_legal WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM users_email_temp WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM sys_users WHERE user_id=%s", (user_id,))
        cursor.execute("DELETE FROM sys_user_logs WHERE user_id=%s", (user_id,))

        # Удаляем основного пользователя
        cursor.execute("DELETE FROM operators WHERE name=%s", (company_name,))
        cursor.execute("DELETE FROM users WHERE login=%s OR email=%s", (email_or_login, email_or_login))
        
        conn.commit()
        cursor.close()
    

    @allure.step("Заполнение паролей")
    def seller_registration_fill_passwords(self, password1: str, password2: str):
        self.fill_element('поле Придумайте пароль', password1)
        self.fill_element('поле Пароль еще раз', password2)
        self.click_element('кнопка Зарегистрироваться')
    
    @allure.step("Заполнение согласий для регистрации продавца")
    def handle_agreements(self, accept_policy, accept_user_agreement, accept_promotional_materials):
        if accept_policy:
            self.click_element('чекбокс Соглашаюсь с политикой обработки данных')
        if accept_user_agreement:
            self.click_element('чекбокс Принимаю пользовательское соглашение')
        if accept_promotional_materials:
            self.click_element('Соглашаюсь получать рекламные материалы')