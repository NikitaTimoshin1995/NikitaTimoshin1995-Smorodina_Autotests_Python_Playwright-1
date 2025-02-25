import allure
from pages.base import BasePage

class MainPage(BasePage):
    @allure.step("Открыть страницу {url}")
    def open(self, url):
        self.page.goto(url)
    
    @allure.step("Нажать кнопку 'Искать туры'")
    def click_search_tours(self):
        self.page.get_by_role('button', name='Искать туры').click()
    
    @allure.step("Нажать кнопку 'Войти'")
    def click_login(self):
        self.page.get_by_role('button', name='Войти').click()
    
    @allure.step("Нажать 'Организатор туров'")
    def click_tour_organizer(self):
        self.page.locator('//h4[text()="Организатор туров"]').click()
    
    @allure.step("Ввести email {email}")
    def fill_email(self, email):
        self.page.fill('input[placeholder="email"]', email)
    
    @allure.step("Ввести пароль")
    def fill_password(self, password):
        self.page.fill('input[placeholder="пароль"]', password)
    
    @allure.step("Нажать кнопку 'Войти'")
    def submit_login(self):
        self.page.click('button[type="submit"]')