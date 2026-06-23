import allure
from pages.client.client_auth_and_registration import ClientAuthRegistration
from playwright.sync_api import Page


class ClientTourCard(ClientAuthRegistration):


#АВТОРИЗОВАН
    @allure.step("Добавить пассажиров в карточке тура персональный")
    def add_passengers_to_tourcard(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка плюс возраст1 в карточке тура клиента')
        for _ in range(children1):
            self.click_element('Кнопка плюс возраст2 в карточке тура клиента')
        for _ in range(children2):
            self.click_element('Кнопка плюс возраст3 в карточке тура клиента')
        for _ in range(infants):
            self.click_element('Кнопка плюс возраст4 в карточке тура клиента')
        for _ in range(beneficiary):
            self.click_element('Кнопка плюс возраст5 в карточке тура клиента')


    @allure.step("Добавить пассажиров в карточке тура персональный бронирование")
    def add_passengers_to_tourcard_booking(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка плюс возраст1 в карточке тура клиента бронирование')
        for _ in range(children1):
            self.click_element('Кнопка плюс возраст2 в карточке тура клиента бронирование')
        for _ in range(children2):
            self.click_element('Кнопка плюс возраст3 в карточке тура клиента бронирование')
        for _ in range(infants):
            self.click_element('Кнопка плюс возраст4 в карточке тура клиента бронирование')
        for _ in range(beneficiary):
            self.click_element('Кнопка плюс возраст5 в карточке тура клиента бронирование')

    @allure.step("Добавить пассажиров в карточке тура групповая")
    def add_passengers_to_tourcard_group(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка плюс групповое в карточке тура клиента')


    @allure.step("Добавить пассажиров в карточке тура групповая бронирование")
    def add_passengers_to_tourcard_group_booking(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка плюс групповое в карточке тура клиента бронирование')


#НЕАВТОРИЗОВАН
    @allure.step("Добавить пассажиров в карточке тура персональный неавторизован")
    def add_passengers_to_tourcard_no_auth(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка плюс возраст1 в карточке тура клиента неавторизован')
        for _ in range(children1):
            self.click_element('Кнопка плюс возраст2 в карточке тура клиента неавторизован')
        for _ in range(children2):
            self.click_element('Кнопка плюс возраст3 в карточке тура клиента неавторизован')
        for _ in range(infants):
            self.click_element('Кнопка плюс возраст4 в карточке тура клиента неавторизован')
        for _ in range(beneficiary):
            self.click_element('Кнопка плюс возраст5 в карточке тура клиента неавторизован')


    @allure.step("Добавить пассажиров в карточке тура персональный неавторизован бронирование")
    def add_passengers_to_tourcard_no_auth_booking(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка плюс возраст1 в карточке тура клиента неавторизован бронирование')
        for _ in range(children1):
            self.click_element('Кнопка плюс возраст2 в карточке тура клиента неавторизован бронирование')
        for _ in range(children2):
            self.click_element('Кнопка плюс возраст3 в карточке тура клиента неавторизован бронирование')
        for _ in range(infants):
            self.click_element('Кнопка плюс возраст4 в карточке тура клиента неавторизован бронирование')
        for _ in range(beneficiary):
            self.click_element('Кнопка плюс возраст5 в карточке тура клиента неавторизован бронирование')


    @allure.step("Добавить пассажиров в карточке тура групповая неавторизован")
    def add_passengers_to_tourcard_group_no_auth(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка плюс групповое в карточке тура клиента неавторизован')


    @allure.step("Добавить пассажиров в карточке тура групповая неавторизован бронирование")
    def add_passengers_to_tourcard_group_no_auth_booking(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка плюс групповое в карточке тура клиента неавторизован бронирование')