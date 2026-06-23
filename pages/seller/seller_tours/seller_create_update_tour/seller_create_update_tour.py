import allure
from Locators.loc_all_directories import ALL_LOCATORS
from pages.seller.seller_tours.seller_tours import SellerTours
from fixtures.all import intercept_requests, db_connection, photo_paths,  db_connection_dev_logs  
from playwright.sync_api import Page, expect
from Assertions.seller.seller_tours.seller_tour_card.assert_seller_tour_card import AssertionsTourCard
from Constants.seller.seller_auth.const_seller_auth import EXPECTED_URL_AFTER_LOGIN_SELLER
from Constants.seller.seller_tours.seller_tour_card.seller_tour_parametrs.const_seller_tour_parametrs import (SELLER_TOUR_TITLE1)
from Constants.seller.seller_tours.seller_tour_card.const_seller_tour_card import SELLER_TOUR_TOUR_PARAMETRS_BUTTON_TEXT

class SellerCreateUpdateTour(SellerTours):

    @allure.title('Переход в создание тура старого продавца')
    def seller_goto_create_tour_old(self, page: Page, login: str, password: str):
        assertions = AssertionsTourCard(page)
        self.seller_auth(page, login, password)
        assertions.check_url(EXPECTED_URL_AFTER_LOGIN_SELLER)
        self.click_element('кнопка Туры в меню продавца')
        xpath_locator = f"xpath={ALL_LOCATORS['кнопка Создать в списке туров']}"
        page.wait_for_selector(xpath_locator, state='visible', timeout=30000)
        page.wait_for_timeout(2500)
        self.seller_click_create_tour()


    @allure.title('Заполнение блока Основное')
    def seller_create_tour_fill_general(self, page: Page, title):
        self.fill_element('Название тура в параметрах тура', title)
        self.click_element('Тип автопутешествия в параметрах тура')
        self.click_element('Автопутешествие в параметрах тура')
        self.click_element('Ответственный сотрудник в параметрах тура')
        page.wait_for_timeout(500)
        self.click_element('Первый сотрудник в параметрах тура')  
        

        
    @allure.title('Удаление тура(ов)')
    def delete_tour_in_db(self, db_connection, db_connection_dev_logs, tour_title):
        cursor = db_connection.cursor()
        try:
            cursor.execute("SELECT id FROM products WHERE name=%s", (tour_title,))
            results = cursor.fetchall()            
            if not results:
                print(f"Туры с названием '{tour_title}' не найдены. Переход к следующему шагу.")
                allure.attach(f"Туры {tour_title} не найдены", name="Информация")
                return False
            product_ids = [row[0] for row in results]
            print(f"Найдено туров для удаления: {len(product_ids)}")
            for product_id in product_ids:
                print(f"Удаление данных для product_id: {product_id}")
                cursor.execute("DELETE FROM product_status_history WHERE product_id=%s", (product_id,))
                cursor.execute("DELETE FROM product_genre WHERE product_id=%s", (product_id,))
                cursor.execute("DELETE FROM product_pictures WHERE product_id=%s", (product_id,))
                cursor.execute("DELETE FROM product_suitables WHERE product_id=%s", (product_id,))
                cursor.execute("SELECT id FROM product_details WHERE product_id=%s", (product_id,))
                detail_ids = [row[0] for row in cursor.fetchall()]
                if detail_ids:
                    cursor.execute("DELETE FROM product_detail_pictures WHERE product_detail_id IN %s", 
                                (tuple(detail_ids),))
                cursor.execute("DELETE FROM product_details WHERE product_id=%s", (product_id,))
                cursor_dev_logs = db_connection_dev_logs.cursor()
                cursor_dev_logs.execute("DELETE FROM activity_logs WHERE model_id=%s", (product_id,))
                db_connection_dev_logs.commit()
                cursor_dev_logs.close()
            cursor.execute("DELETE FROM products WHERE name=%s", (tour_title,))
            db_connection.commit()
            allure.attach(f"Удалено {len(product_ids)} туров с названием '{tour_title}'", 
                        name="Успешное удаление")
            print(f"Успешно удалено {len(product_ids)} туров")
            return True
        except Exception as e:
            db_connection.rollback()
            error_msg = f"Ошибка при удалении туров: {str(e)}"
            allure.attach(error_msg, name="Ошибка")
            raise Exception(error_msg)
        finally:
            cursor.close()


    @allure.title('Заполнить весь тур, кроме маршрута')
    def fill_all_tour_without_route(self, page: Page, photo_paths, title, booking: bool, description: str, in_price: str, not_in_price: str):
        self.seller_create_tour_fill_general(page, title)
        if booking:
            self.click_element('Только предварительное бронирование тогл в параметрах тура')
        self.click_element('1й жанр в параметрах тура')
        self.click_element('1й класс в параметрах тура')
        self.click_element('На своей машине в параметрах тура')
        paths = photo_paths("1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg")
        self.upload_photos_via_click('Поле загрузки фото в создании тура продавца', 5, *paths)
        self.fill_element('Описание в создании тура продавца', description)
        self.fill_element('Что входит в стоимость в создании тура продавца', in_price)
        self.fill_element('Что не входит в стоимость в создании тура продавца', not_in_price)
        self.click_element('Кому подойдет1 в создании тура продавца')
        self.click_element('Кнопка Сохранить в создании тура продавца')


    @allure.title('Заполнить весь тур, кроме маршрута, класса и транспорта')
    def fill_all_tour_without_route_class_transport(self, page: Page, photo_paths, title, booking: bool, description: str, in_price: str, not_in_price: str):
        self.seller_create_tour_fill_general(page, title)
        if booking:
            self.click_element('Только предварительное бронирование тогл в параметрах тура')
        self.click_element('1й жанр в параметрах тура')
        paths = photo_paths("1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg")
        self.upload_photos_via_click('Поле загрузки фото в создании тура продавца', 5, *paths)
        self.fill_element('Описание в создании тура продавца', description)
        self.fill_element('Что входит в стоимость в создании тура продавца', in_price)
        self.fill_element('Что не входит в стоимость в создании тура продавца', not_in_price)
        self.click_element('Кому подойдет1 в создании тура продавца')
        self.click_element('Кнопка Сохранить в создании тура продавца')


    @allure.title('Проверка, что нет кнопки На проверку')
    def check_absence_button_on_check(self, page:Page):
        assertions = AssertionsTourCard(page)
        self.click_element('Назад в создании тура')
        # page.reload() # Убрать, как баг фиксанут
        page.wait_for_timeout(2000) 
        self.click_element_by_text(SELLER_TOUR_TITLE1)
        assertions.check_element_not_present('кнопка На проверку в карточку тура продавца')
        self.click_element_by_text(SELLER_TOUR_TOUR_PARAMETRS_BUTTON_TEXT, nth=0)

    
    @allure.title('Проверка, что есть кнопка На проверку')
    def check_presence_button_on_check(self, page:Page):
        assertions = AssertionsTourCard(page)
        self.click_element('Назад в создании тура')
        # page.reload() # Убрать, как баг фиксанут
        page.wait_for_timeout(2000) 
        self.click_element_by_text(SELLER_TOUR_TITLE1)
        assertions.check_element_present('кнопка На проверку в карточку тура продавца')
        self.click_element_by_text(SELLER_TOUR_TOUR_PARAMETRS_BUTTON_TEXT, nth=0)