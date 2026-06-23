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

class CompanyDetailsIp(CompanyDetails):

#Индивидуальный предприниматель
    @allure.step('Выбор формы организации ИП')
    def open_company_details_choice_form_ip(self):
        self.click_element('Правовая форма')
        self.click_element('Индивидуальный предприниматель')
    

    @allure.step('Ввод инн ИП')
    def company_details_choice_fill_inn_ip(self,ip_inn):
        self.fill_element('ИП ИНН', ip_inn)


    @allure.step('Выбор НДС ИП')
    def company_details_choice_fill_nds_ip(self, nds: int, locator: int):
        if nds == 0:
            return
        self.click_element(f'ИП все НДС{locator}')
        self.click_element(f'ИП НДС{nds}')

    @allure.step('Заполнение данных компании ИП')
    def fill_company_details_ip(self, inn, fio, ogrn, bill, bic, bank, nds, locator):
        self.fill_element('ИП ИНН', inn)
        self.fill_element('ИП ФИО', fio)
        self.fill_element('ИП ОГРН', ogrn)
        self.fill_element('ИП Р. / счёт', bill)
        self.fill_element('ИП БИК', bic)
        self.fill_element('ИП Банк', bank)
        self.company_details_choice_fill_nds_ip(nds, locator)