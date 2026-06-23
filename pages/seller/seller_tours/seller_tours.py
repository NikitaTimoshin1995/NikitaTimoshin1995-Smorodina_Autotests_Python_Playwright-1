import allure
from pages.seller.seller_auth_and_registration import SellerAuthRegistration
from Locators.loc_all_directories import ALL_LOCATORS

class SellerTours(SellerAuthRegistration):

    @allure.title('Кликнуть на кнопку Создать')
    def seller_click_create_tour(self):
        self.click_element('кнопка Создать в списке туров')