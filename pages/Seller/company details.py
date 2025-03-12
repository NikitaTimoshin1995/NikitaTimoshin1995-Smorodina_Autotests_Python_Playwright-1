import allure
from pages.main_page  import MainPage
from data.constants import (SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1)


class CompanyDetails (MainPage):
    allure.step('Заполнение данных копании')
    def legal_company_fill():
        MainPage.seller_auth(SELLER_LOGIN1_REGISTR, SELLER_PASSWORD1)