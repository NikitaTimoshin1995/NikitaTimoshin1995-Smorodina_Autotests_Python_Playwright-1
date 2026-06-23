import allure
from Assertions.assertions import Assertions
from playwright.sync_api import Page
from Locators.loc_all_directories import ALL_LOCATORS
import time
import json

class AssertionsClientAuthRegistration(Assertions):

    @allure.step("Проверка, что кнопка 'Продолжить' в авторизации клиента неактивна")
    def check_client_auth_button_inactive(self, timeout=30):
        start_time = time.time()
        xpath = ALL_LOCATORS['Кнопка Продолжить в модалке авторизации клиента']
        while time.time() - start_time < timeout:
            try:
                self.check_element_disabled_by_xpath(xpath)
                return  
            except AssertionError:
                time.sleep(1)
        raise AssertionError("Кнопка 'Сохранить' осталась активной после ожидания 30 секунд.")
    
    @allure.step("Проверка, что кнопка 'Продолжить' в авторизации клиента активна")
    def check_client_auth_button_active(self):
        self.check_element_enabled_by_xpath(ALL_LOCATORS['Кнопка Продолжить в модалке авторизации клиента'])

