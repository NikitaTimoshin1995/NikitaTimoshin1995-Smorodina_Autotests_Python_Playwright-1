from playwright.sync_api import Page, TimeoutError, Response
from data.environment import host

class Base:
    def __init__(self, page: Page):
        self.page = page

def open(self, uri) -> Response | None:
    return self.page.goto(f"{host.get_base_url()}{uri}",
    wait_until='domcontentloaded')

def input(self, locator, data: str) -> None:
    self.page.locator(locator).fill(data)

def click(self, locator) -> None: #
    self.page.click(locator)

def get_text(self, element) -> str:  #
    return self.page.locator(element).text_content()

def click_element_by_index(self, selector: str, index: int):
    self.page.locator(selector).nth(index).click()

def input_value_by_index(self, selector: str, index: int, data: str): #вводим данные в нужные поля по индексу
    self.page.locator(selector).nth(index).fill(data)