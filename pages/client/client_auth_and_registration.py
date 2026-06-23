import allure
from pages.base import BasePage
from Constants.const_general import URL
from playwright.sync_api import Page


class ClientAuthRegistration(BasePage):

    @allure.step("Открыли авторизацию/регистрацию клиента через кнопку Войти")
    def client_go_to_auth(self):
        self.open_page(URL) 
        self.wait_for_full_load()
        self.allow_location_access()  # Разрешаем доступ к местоположению 
        self.close_livechat_if_present()
        self.click_element_if_present('кнопка закрыть поппап') 
        self.close_subscription_if_present()
        self.page.wait_for_timeout(2500)  # Ждем закрытия попапа
        self.click_element('Кнопка Принять куки')
        self.page.wait_for_timeout(1500)  # Ждем принятия куки
        self.click_element('кнопка Вход')  
        self.page.locator('xpath=/html/body/div[3]/div/div[2]/div/div/div[1]/input').wait_for(state="visible")  # Ждем открытия модального окна авторизации  


    @allure.step("В авторизации/регистрации клиента заполнить телефон")
    def client_fill_phone(self, phone):
        self.click_element('Поле с телефоном в авторизации/регистрации клиент')  # Кликаем на поле, чтобы активировать
        self.fill_element('Поле с телефоном в авторизации/регистрации клиент', phone )


    @allure.step("Кликнуть на кнопку Продолжить в авторизации клиента")
    def client_click_enter(self):
        self.click_element('Кнопка Продолжить в модалке авторизации клиента')


    @allure.step("Подтверждение телефона")
    def client_confirm_phone(self, db_connection, phone):
        cursor = db_connection.cursor()
        try:
            cursor.execute("SELECT confirmation_code FROM users_phone_temp WHERE phone = %s order by created_at desc", (phone,))
            result = cursor.fetchone()  # Извлекаем результат
            if result is None:
                raise ValueError(f"Код подтверждения не найден для: {phone}")
            confirmation_code = result[0]  # Получаем код подтверждения
            digits = list(str(confirmation_code))  # Преобразуем код в список цифр
            # Вводим каждую цифру кода подтверждения
            self.fill_element('Первая цифра у клиента', digits[0])
            self.fill_element('Вторая цифра у клиента', digits[1])
            self.fill_element('Третья цифра у клиента', digits[2])
            self.fill_element('Четвертая цифра у клиента', digits[3])
        finally:
            cursor.close()


    @allure.step("Подтверждение телефона при авторизации из карточки тура")
    def client_confirm_phone_tourcard(self, db_connection, phone):
        cursor = db_connection.cursor()
        cursor.execute("SELECT confirmation_code FROM users_phone_temp WHERE phone = %s order by created_at desc", (phone,))
        result = cursor.fetchone()  # Извлекаем результат
        if result is None:
            raise ValueError(f"Код подтверждения не найден для: {phone}")
        confirmation_code = result[0]  # Получаем код подтверждения
        digits = list(str(confirmation_code))  # Преобразуем код в список цифр
        # Вводим каждую цифру кода подтверждения
        self.fill_element('Первая цифра у клиента из карточки тура', digits[0])
        self.fill_element('Вторая цифра у клиента из карточки тура', digits[1])
        self.fill_element('Третья цифра у клиента из карточки тура', digits[2])
        self.fill_element('Четвертая цифра у клиента из карточки тура', digits[3])


    @allure.step("Ввод кода из смс")
    def client_enter_sms_code(self, first, second, third, fouth):
        self.fill_element('Первая цифра у клиента', first)
        self.fill_element('Вторая цифра у клиента', second)
        self.fill_element('Третья цифра у клиента', third)
        self.fill_element('Четвертая цифра у клиента', fouth)


    @allure.step("Авторизация клиента без ввода кода")
    def client_auth_short(self,db_connection, phone: str):
        self.client_go_to_auth()
        self.client_fill_phone(phone)
        self.client_click_enter()


    @allure.step("Авторизация клиента выбор всех согласий")
    def choose_all_agreements(self):
        self.click_element('Чекбокс согласия на обработку данных в авторизации клиента')
        self.click_element('Чекбокс согласия с пользовательским соглашением в авторизации клиента')
        self.click_element('Чекбокс согласия с политикой обработки данных в авторизации клиента')

    @allure.step("Авторизация клиента")
    def client_auth(self,db_connection, phone: str):
        self.client_go_to_auth()
        self.client_fill_phone(phone)
        self.choose_all_agreements()
        self.client_click_enter()
        self.page.wait_for_timeout(1000) 
        self.client_confirm_phone(db_connection, phone)


    @allure.step("Авторизация клиента из карточки тура")
    def client_auth_tour_card(self,db_connection, phone: str):
        self.fill_element('Поле с телефоном в авторизации/регистрации клиент из карточки тура', phone )
        self.click_element('Кнопка Продолжить в модалке авторизации клиента из карточки тура')
        self.page.wait_for_timeout(3000)
        self.client_confirm_phone_tourcard(db_connection, phone)


    @allure.step("Кликнуть на ссылку 'Политикой обработки данных")
    def client_click_a_data_policy(self):
        self.click_element('Ссылка Политика обработки данных в авторизации клиента')
        # self.switch_to_new_tab() # Просто переключаемся на новую вкладку
        return self.switch_to_new_tab()  # Возвращаем новую вкладку
    

    @allure.step("Кликнуть на ссылку 'Пользовательское соглашение")
    def client_click_a_agreement(self):
        self.click_element('Ссылка Пользовательское соглашение в авторизации клиента')
        return self.switch_to_new_tab()
    

    @allure.step("Кликнуть на ссылку 'обработку персональных данных")
    def client_click_a_personal_data(self):
        self.click_element('Ссылка Обработку персональных данных в авторизации клиента')
        return self.switch_to_new_tab()
    


   



    
