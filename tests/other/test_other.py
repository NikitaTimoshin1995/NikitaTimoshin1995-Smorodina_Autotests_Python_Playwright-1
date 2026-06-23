import pytest
from playwright.sync_api import Page
from Locators.loc_all_directories import ALL_LOCATORS
from pages.base import BasePage
from Assertions.assertions import Assertions
import allure
from fixtures.all import intercept_requests


@allure.feature('Другое')
@allure.story('Другое')
@pytest.mark.all
@pytest.mark.other

class TestOther:

    @allure.title('Проверка sitemap prod')
    def test_other1(self, page: Page, intercept_requests): 
        assertions = Assertions(page) 
        other = BasePage(page) 
        other.open_page('https://smorodina.ru/sitemap.xml')
        assertions.check_request_statuses(intercept_requests)
        
