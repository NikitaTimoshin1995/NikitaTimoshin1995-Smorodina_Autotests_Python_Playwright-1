import allure
from Locators.loc_all_directories import ALL_LOCATORS
from pages.seller.seller_tours.seller_create_update_tour.seller_create_update_tour import SellerCreateUpdateTour
from playwright.sync_api import Page, expect
from Assertions.assertions import Assertions
from Constants.seller.seller_auth.const_seller_auth import (
    SELLER_LOGIN4_TOURS,
    SELLER_PASSWORD1
)
from Constants.seller.seller_tours.seller_tour_card.seller_tour_parametrs.const_seller_tour_parametrs import (
    SELLER_TOUR_TITLE1
)


class SellerCreateUpdateTourWaypoints(SellerCreateUpdateTour):

    @allure.title('Переход в создание точек маршрута старого продавца')
    def seller_goto_create_tour_waypoints_old(self, page: Page):
        self.seller_goto_create_tour_old(page, SELLER_LOGIN4_TOURS, SELLER_PASSWORD1)
        self.seller_create_tour_fill_general(page, SELLER_TOUR_TITLE1 )
        self.click_element( 'Кнопка Настроить маршрут в создании тура продавца')


    @allure.title('Заполнить точку сбора в создании тура')
    def seller_waypoints_fill_collection_point(self, page: Page, photo_paths, address: str, time: str, title: str, description: str ):
        self.click_element('Кнопка Настроить маршрут в создании тура продавца')
        self.click_element('Точка сбора в маршруте в создании тура продавца')
        self.fill_element('Адрес в точке сбора в создании тура продавца', 'Ульяновск, улица Робеспьера, 28') # Лишнее. Из-за бага
        page.wait_for_timeout(1000) # Лишнее. Из-за бага
        self.fill_element('Адрес в точке сбора в создании тура продавца', address)
        self.click_element('Первый предложенный адрес в точке сбора в создании тура продавца')
        page.wait_for_timeout(1000)
        self.fill_element('Время в точке сбора в создании тура продавца', time)
        self.fill_element('Название в точке сбора в создании тура продавца', title)
        self.fill_element('Описание в точке сбора в создании тура продавца', description)
        paths = photo_paths("1.jpg")
        self.upload_photos_via_click_general('Загрузка фото в точке сбора в создании тура продавца ', 1, *paths)
        self.click_element('Кнопка Сохранить в точке сбора в создании тура продавца')
        page.wait_for_timeout(3000)
        self.click_element('Крестик в маршруте в создании тура продавца')