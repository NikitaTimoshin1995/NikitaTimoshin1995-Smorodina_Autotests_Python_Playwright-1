import allure

class BasePage:
    def __init__(self, page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def goto(self, url):
        self.page.goto(url)