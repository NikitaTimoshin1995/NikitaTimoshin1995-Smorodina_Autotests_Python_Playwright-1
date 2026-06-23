import allure
from Assertions.seller.seller_tours.assert_seller_tours import AssertionsTours
from playwright.sync_api import Page, expect
from Locators.loc_all_directories import ALL_LOCATORS
import time

class AssertionsTourCard(AssertionsTours): 


    @allure.step("Проверка, что кнопка Сохранить в создани/редактировании тура активна")
    def check_operator_tour_param_button_create_active(self):
        self.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Сохранить в создании тура продавца'])