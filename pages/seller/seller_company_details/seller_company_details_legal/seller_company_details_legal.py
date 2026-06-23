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

class CompanyDetailsLegal(CompanyDetails):

#ЮР.ЛИЦО
    @allure.step('Выбор формы организации ЮР.ЛИЦО')
    def open_company_details_choice_form_legal(self):
        self.click_element('Правовая форма')
        self.click_element('Юр.лицо')

    
    @allure.step('Ввод инн ЮР.ЛИЦО')
    def company_details_choice_fill_inn_legal(self, legal_inn):
        self.fill_element('Юр ИНН', legal_inn)


    @allure.step('Выбор НДС ЮР.ЛИЦО')
    def company_details_choice_fill_nds_legal(self, nds: int, locator: int):
        if nds == 0:
            return
        self.click_element(f'Юр все НДС{locator}')
        self.click_element(f'Юр НДС{nds}')


    @allure.step('Заполнение данных компании ЮР')
    def fill_company_details_legal(self, inn, opf, fullname, shortname, legal_address, kpp, ogrn, bill, bic, bank, director, nds, locator):
        self.fill_element('Юр ИНН', inn)
        self.fill_element('Юр ОПФ', opf)
        self.fill_element('Юр Полное наименование', fullname)
        self.fill_element('Юр Краткое наименование', shortname)
        self.fill_element('Юр Юр. адрес', legal_address)
        self.fill_element('Юр КПП', kpp)
        self.fill_element('Юр ОГРН', ogrn)
        self.fill_element('Юр Р. / счёт', bill)
        self.fill_element('Юр БИК', bic)
        self.fill_element('Юр Банк', bank)
        self.fill_element('Юр ФИО ген. директора', director)
        self.company_details_choice_fill_nds_legal(nds, locator)