import pytest
from playwright.sync_api import Page
from fixtures.all import intercept_requests, db_connection  
from Locators.loc_all_directories import ALL_LOCATORS
import allure
from entities.tour.eni_tour import TourAPI

# @allure.feature('Клиент')
# @allure.story('Карточка тура')
# @pytest.mark.all
# @pytest.mark.client
# class TestClientTourCard:
#     @allure.title('Смена статуса тура')
#     def test_client_tour_card1(self):
#         tour_api = TourAPI()
#         response = tour_api.patch_company_start(925, 5)

       