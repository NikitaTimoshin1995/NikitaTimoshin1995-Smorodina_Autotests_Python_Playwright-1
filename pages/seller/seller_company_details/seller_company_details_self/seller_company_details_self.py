import allure
import pytest
import psycopg2
import requests
from psycopg2 import Error
from playwright.sync_api import Page, expect
from pages.seller.seller_company_details.company_details import CompanyDetails
from Locators.loc_all_directories import ALL_LOCATORS
from Assertions.assertions import Assertions
from fixtures.all import intercept_requests, db_connection  
from playwright.sync_api import Page

class CompanyDetailsSelf(CompanyDetails):

 #САМОЗАНЯТЫЙ
    @allure.step('Выбор формы организации Самозанятый')
    def open_company_details_choice_form_self(self):
        self.click_element('Правовая форма')
        self.click_element('Самозанятый')
 
        
    @allure.step("Заполнение данных самозанятого")
    def fill_company_details_self(self, self_inn, self_surname, self_name, self_patronymic, 
                                    self_bill, self_bic, self_bank, self_reference):
        self.fill_element('Самозанятый ИНН', self_inn)
        self.fill_element('Самозанятый Фамилия', self_surname)
        self.fill_element('Самозанятый Имя', self_name)
        self.fill_element('Самозанятый Отчество', self_patronymic)
        self.fill_element('Самозанятый Р. / счёт', self_bill)
        self.fill_element('Самозанятый БИК', self_bic)
        self.fill_element('Самозанятый Банк', self_bank)
        self.fill_element('Самозанятый Номер справки', self_reference)
    

    @allure.step('Ввод инн Самозанятый')
    def company_details_choice_fill_inn_self(self, self_inn):
        self.fill_element('Самозанятый ИНН', self_inn)

    @allure.step("Проверка статуса оператора на фронте")
    def check_operator_self_state_hidden(self, page):
        state_xpath = ALL_LOCATORS['STATE самозанятого в данных компании']
        state_element = page.locator(f'xpath={state_xpath}')    
        # Ожидаем, пока элемент исчезнет
        state_element.wait_for(state="hidden", timeout=120000)


    