import allure
from Assertions.client.client_auth_and_registration.assert_client_auth_and_registration import AssertionsClientAuthRegistration
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS


class AssertionsClientTourCard(AssertionsClientAuthRegistration):

    #Авторизован
    @allure.step("Проверка количества участников в нераскрытом поле карточки тура клиента")
    def check_number_participants_rolled(self, number_participants: str):
        self.check_field_value_from_locator('Количество участников в карточке тура клиента', number_participants)


    @allure.step("Проверка количества участников в нераскрытом поле карточки тура клиента бронирование")
    def check_number_participants_rolled_booking(self, number_participants: str):
        self.check_field_value_from_locator('Количество участников в карточке тура клиента бронирование', number_participants)


    @allure.step("Проверка даты в датапикере карточки тура клиента")
    def check_data_datapicker_tourcard(self, date: str):
        self.check_field_value_from_locator('Дата в датапикере в карточке тура клиента', date)

    @allure.step("Проверка даты в датапикере карточки тура клиента бронирование")
    def check_data_datapicker_tourcard_booking(self, date: str):
        self.check_field_value_from_locator('Дата в датапикере в карточке тура клиента бронирование', date)


    @allure.step("Проверка категорий возрастов в карточке тура клиента персонального")
    def check_data_participants_ages_tourcard(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в карточке тура клиента', category1)
        self.check_field_value_from_locator('Цена возраст1 в карточке тура клиента', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в карточке тура клиента', ages1)
        self.check_field_value_from_locator('Название возраст2 в карточке тура клиента', category2)
        self.check_field_value_from_locator('Цена возраст2 в карточке тура клиента', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в карточке тура клиента', ages2)
        self.check_field_value_from_locator('Название возраст3 в карточке тура клиента', category3)
        self.check_field_value_from_locator('Цена возраст3 в карточке тура клиента', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в карточке тура клиента', ages3)
        self.check_field_value_from_locator('Название возраст4 в карточке тура клиента', category4)
        self.check_field_value_from_locator('Цена возраст4 в карточке тура клиента', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в карточке тура клиента', ages4)
        self.check_field_value_from_locator('Название возраст5 в карточке тура клиента', category5)
        self.check_field_value_from_locator('Цена возраст5 в карточке тура клиента', price5)


    @allure.step("Проверка категорий возрастов в карточке тура клиента персонального бронирование")
    def check_data_participants_ages_tourcard_booking(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в карточке тура клиента бронирование', category1)
        self.check_field_value_from_locator('Цена возраст1 в карточке тура клиента бронирование', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в карточке тура клиента бронирование', ages1)
        self.check_field_value_from_locator('Название возраст2 в карточке тура клиента бронирование', category2)
        self.check_field_value_from_locator('Цена возраст2 в карточке тура клиента бронирование', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в карточке тура клиента бронирование', ages2)
        self.check_field_value_from_locator('Название возраст3 в карточке тура клиента бронирование', category3)
        self.check_field_value_from_locator('Цена возраст3 в карточке тура клиента бронирование', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в карточке тура клиента бронирование', ages3)
        self.check_field_value_from_locator('Название возраст4 в карточке тура клиента бронирование', category4)
        self.check_field_value_from_locator('Цена возраст4 в карточке тура клиента бронирование', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в карточке тура клиента бронирование', ages4)
        self.check_field_value_from_locator('Название возраст5 в карточке тура клиента бронирование', category5)
        self.check_field_value_from_locator('Цена возраст5 в карточке тура клиента бронирование', price5)


    @allure.step("Проверка количества участников разных возрастов в карточке тура клиента персонального")
    def check_data_participants_amount_tourcard(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в карточке тура клиента', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в карточке тура клиента', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в карточке тура клиента', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в карточке тура клиента', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в карточке тура клиента', participants_number5)


    @allure.step("Проверка количества участников разных возрастов в карточке тура клиента персонального бронирование")
    def check_data_participants_amount_tourcard_booking(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в карточке тура клиента бронирование', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в карточке тура клиента бронирование', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в карточке тура клиента бронирование', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в карточке тура клиента бронирование', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в карточке тура клиента бронирование', participants_number5)

    @allure.step("Проверка количества участников в карточке группового тура клиента")
    def check_data_participants_amount_tourcard_group(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в карточке тура клиента', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в карточке тура клиента', participants_number)


    @allure.step("Проверка количества участников в карточке группового тура клиента бронирование")
    def check_data_participants_amount_tourcard_group_booking(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в карточке тура клиента бронирование', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в карточке тура клиента бронирование', participants_number)


    #НЕАВТОРИЗОВАН
    @allure.step("Проверка количества участников в нераскрытом поле карточки тура клиента")
    def check_number_participants_rolled_no_auth(self, number_participants: str):
        self.check_field_value_from_locator('Количество участников в карточке тура клиента неавторизован', number_participants)


    @allure.step("Проверка количества участников в нераскрытом поле карточки тура клиента бронирование")
    def check_number_participants_rolled_no_auth_booking(self, number_participants: str):
        self.check_field_value_from_locator('Количество участников в карточке тура клиента неавторизован бронирование', number_participants)


    @allure.step("Проверка даты в датапикере карточки тура клиента")
    def check_data_datapicker_tourcard_no_auth(self, date: str):
        self.check_field_value_from_locator('Дата в датапикере в карточке тура клиента неавторизован', date)


    @allure.step("Проверка даты в датапикере карточки тура клиента бронирование")
    def check_data_datapicker_tourcard_no_auth_booking(self, date: str):
        self.check_field_value_from_locator('Дата в датапикере в карточке тура клиента неавторизован бронирование', date)


    @allure.step("Проверка категорий возрастов в карточке тура клиента персонального")
    def check_data_participants_ages_tourcard_no_auth(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в карточке тура клиента неавторизован', category1)
        self.check_field_value_from_locator('Цена возраст1 в карточке тура клиента неавторизован', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в карточке тура клиента неавторизован', ages1)
        self.check_field_value_from_locator('Название возраст2 в карточке тура клиента неавторизован', category2)
        self.check_field_value_from_locator('Цена возраст2 в карточке тура клиента неавторизован', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в карточке тура клиента неавторизован', ages2)
        self.check_field_value_from_locator('Название возраст3 в карточке тура клиента неавторизован', category3)
        self.check_field_value_from_locator('Цена возраст3 в карточке тура клиента неавторизован', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в карточке тура клиента неавторизован', ages3)
        self.check_field_value_from_locator('Название возраст4 в карточке тура клиента неавторизован', category4)
        self.check_field_value_from_locator('Цена возраст4 в карточке тура клиента неавторизован', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в карточке тура клиента неавторизован', ages4)
        self.check_field_value_from_locator('Название возраст5 в карточке тура клиента неавторизован', category5)
        self.check_field_value_from_locator('Цена возраст5 в карточке тура клиента неавторизован', price5)


    @allure.step("Проверка категорий возрастов в карточке тура клиента персонального бронирование")
    def check_data_participants_ages_tourcard_no_auth_booking(self, category1: str, price1: str, ages1: str, category2: str, price2: str, ages2: str,
                                               category3: str, price3: str, ages3: str, category4: str, price4: str, ages4: str,
                                                category5: str, price5: str):
        self.check_field_value_from_locator('Название возраст1 в карточке тура клиента неавторизован бронирование', category1)
        self.check_field_value_from_locator('Цена возраст1 в карточке тура клиента неавторизован бронирование', price1)
        self.check_field_value_from_locator('Диапазон возраст1 в карточке тура клиента неавторизован бронирование', ages1)
        self.check_field_value_from_locator('Название возраст2 в карточке тура клиента неавторизован бронирование', category2)
        self.check_field_value_from_locator('Цена возраст2 в карточке тура клиента неавторизован бронирование', price2)
        self.check_field_value_from_locator('Диапазон возраст2 в карточке тура клиента неавторизован бронирование', ages2)
        self.check_field_value_from_locator('Название возраст3 в карточке тура клиента неавторизован бронирование', category3)
        self.check_field_value_from_locator('Цена возраст3 в карточке тура клиента неавторизован бронирование', price3)
        self.check_field_value_from_locator('Диапазон возраст3 в карточке тура клиента неавторизован бронирование', ages3)
        self.check_field_value_from_locator('Название возраст4 в карточке тура клиента неавторизован бронирование', category4)
        self.check_field_value_from_locator('Цена возраст4 в карточке тура клиента неавторизован бронирование', price4)
        self.check_field_value_from_locator('Диапазон возраст4 в карточке тура клиента неавторизован бронирование', ages4)
        self.check_field_value_from_locator('Название возраст5 в карточке тура клиента неавторизован бронирование', category5)
        self.check_field_value_from_locator('Цена возраст5 в карточке тура клиента неавторизован бронирование', price5)


    @allure.step("Проверка количества участников разных возрастов в карточке тура клиента персонального")
    def check_data_participants_amount_tourcard_no_auth(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в карточке тура клиента неавторизован', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в карточке тура клиента неавторизован', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в карточке тура клиента неавторизован', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в карточке тура клиента неавторизован', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в карточке тура клиента неавторизован', participants_number5)


    @allure.step("Проверка количества участников разных возрастов в карточке тура клиента персонального бронирование")
    def check_data_participants_amount_tourcard_no_auth_booking(self, participants_number1: str, participants_number2: str, participants_number3: str,
                                               participants_number4: str, participants_number5: str):
        self.check_field_value_from_locator('Количество возраст1 в карточке тура клиента неавторизован бронирование', participants_number1)
        self.check_field_value_from_locator('Количество возраст2 в карточке тура клиента неавторизован бронирование', participants_number2)
        self.check_field_value_from_locator('Количество возраст3 в карточке тура клиента неавторизован бронирование', participants_number3)
        self.check_field_value_from_locator('Количество возраст4 в карточке тура клиента неавторизован бронирование', participants_number4)
        self.check_field_value_from_locator('Количество возраст5 в карточке тура клиента неавторизован бронирование', participants_number5)


    @allure.step("Проверка количества участников в карточке группового тура клиента")
    def check_data_participants_amount_tourcard_group_no_auth(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в карточке тура клиента неавторизован', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в карточке тура клиента неавторизован', participants_number)


    @allure.step("Проверка количества участников в карточке группового тура клиента бронирование")
    def check_data_participants_amount_tourcard_group_no_auth_booking(self, participants_name: str, participants_number: str):
        self.check_field_value_from_locator('Участники название групповое в карточке тура клиента неавторизован бронирование', participants_name)
        self.check_field_value_from_locator('Участники количество групповое в карточке тура клиента неавторизован бронирование', participants_number)