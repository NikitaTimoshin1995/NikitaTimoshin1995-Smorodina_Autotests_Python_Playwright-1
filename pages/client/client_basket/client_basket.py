import allure
from pages.client.client_tour_card.client_tour_card import ClientTourCard
from fixtures.all import db_connection  
from Constants.const_general import URL
import time
from playwright.sync_api import Page
from Constants.client.client_basket.const_client_basket import (
    C_CLIENT_BASKET_PAYMENT_CARD,
    C_CLIENT_BASKET_PAYMENT_CODE,
    C_CLIENT_BASKET_PAYMENT_NAME
)
from Constants.client.client_basket.const_client_basket import (
            C_CLIENT_BASKET_LASTNAME,
            C_CLIENT_BASKET_NAME,
            C_CLIENT_BASKET_PATRONYMIC,
            C_CLIENT_BASKET_PHONE,
            C_CLIENT_BASKET_EMAIL,
            C_CLIENT_BASKET_DATE_BORN
        )

class ClientBasket(ClientTourCard):


    #Общее
    @allure.step("Успешная оплата картой")
    def successful_payment(self):
        self.fill_element('Карта в твоих платежах', C_CLIENT_BASKET_PAYMENT_CARD)
        self.click_element('Месяцы в твоих платежах')
        self.click_element('8й месяц в твоих платежах')
        self.click_element('Годы в твоих платежах')
        self.click_element('2026 год в твоих платежах')
        self.fill_element('Код в твоих платежах', C_CLIENT_BASKET_PAYMENT_CODE)
        self.fill_element('Имя в твоих платежах', C_CLIENT_BASKET_PAYMENT_NAME)
        self.click_element('Кнопка оплатить в твоих платежах')


    @allure.step('Получение id и code подзаказов')
    def get_suborders_id_code(self, db_connection, product_id):
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM orders ORDER BY id DESC LIMIT 1")
        last_order = cursor.fetchone()
        assert last_order is not None, "Не найдено ни одного заказа в базе данных"
        order_id = last_order[0]
        cursor.execute("SELECT id, code FROM order_tours WHERE order_id = %s and tour_id= %s", (order_id, product_id))
        suborders = cursor.fetchall()    
        cursor.close()
        suborders_simple = []
        for suborder in suborders:
            suborders_simple.append({
                'id': suborder[0],
                'code': suborder[1]
            })
        return suborders_simple


    @allure.step("Добавить пассажиров в корзину тура1 дата1")
    def add_passengers_to_basket(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка плюс возраст1 в корзине')
        for _ in range(children1):
            self.click_element('Кнопка плюс возраст2 в корзине')
        for _ in range(children2):
            self.click_element('Кнопка плюс возраст3 в корзине')
        for _ in range(infants):
            self.click_element('Кнопка плюс возраст4 в корзине')
        for _ in range(beneficiary):
            self.click_element('Кнопка плюс возраст5 в корзине')


    @allure.step("Убавить пассажиров в корзине тура1 дата1")
    def minus_passengers_to_basket(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка минус возраст1 в корзине')
        for _ in range(children1):
            self.click_element('Кнопка минус возраст2 в корзине')
        for _ in range(children2):
            self.click_element('Кнопка минус возраст3 в корзине')
        for _ in range(infants):
            self.click_element('Кнопка минус возраст4 в корзине')
        for _ in range(beneficiary):
            self.click_element('Кнопка минус возраст5 в корзине')

    @allure.step("Убавить пассажиров в корзине тура1, когда есть ошибка")
    def minus_passengers_to_basket_with_error(self, adults: int, children1: int, children2: int, infants: int, beneficiary: int):
        for _ in range(adults):
            self.click_element('Кнопка минус возраст1 в корзине с ошибкой')
        for _ in range(children1):
            self.click_element('Кнопка минус возраст2 в корзине с ошибкой')
        for _ in range(children2):
            self.click_element('Кнопка минус возраст3 в корзине с ошибкой')
        for _ in range(infants):
            self.click_element('Кнопка минус возраст4 в корзине с ошибкой')
        for _ in range(beneficiary):
            self.click_element('Кнопка минус возраст5 в корзине с ошибкой')

    @allure.step("Добавить пассажиров в корзине тура1 дата2 групповая")
    def add_passengers_to_basket_group(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка плюс групповое в корзине')


    @allure.step("Убавить пассажиров в корзине тура1 дата2 групповая")
    def minus_passengers_to_basket_group(self, participants: int):
        for _ in range(participants):
            self.click_element('Участники кнопка минус групповое в корзине')

    #Авторизован
    @allure.step("Заполнить основного авторизованного путешественника")
    def fill_main_traveller_auth(self, lastname: str, name: str, patronymic: str, email: str, date_born: str):
        self.fill_element('Фамилия в корзине', lastname)
        self.fill_element('Имя в корзине', name)
        self.fill_element('Отчество в корзине', patronymic)
        self.fill_element('Емаил в корзине', email)
        self.fill_element('Дата рождения в корзине', date_born)


    @allure.step("Открыть корзину у авторизованного пользователя")
    def client_go_to_auth_basket(self, phone, db_connection ):
        self.client_auth(db_connection, phone)
        self.click_element('Кнопка Корзина у авторизованного пользователя c витрины')


    @allure.step("Заполнить клиента страховки")
    def client_add_client_insurance_basket(self, page: Page, lastname, name, patronymic, date_born, number_client):
        self.fill_element(f'Фамилия клиента{number_client} в страховке в туре1 в корзине', lastname)
        self.fill_element(f'Имя клиента{number_client} в страховке в туре1 в корзине', name)
        self.fill_element(f'Отчество клиента{number_client} в страховке в туре1 в корзине', patronymic)
        self.fill_element(f'Дата рождения клиента{number_client} в страховке в туре1 в корзине', date_born)
        self.click_element('Заголовок формы клиента1 в страховке в туре1 в корзине')
        self.click_element('Заголовок формы клиента1 в страховке в туре1 в корзине')


    
    #Неавторизован
    @allure.step("Заполнить основного неавторизованного путешественника")
    def fill_main_traveller_noauth(self, lastname: str, name: str, patronymic: str, phone: str, email: str, date_born: str):
        self.fill_element('Фамилия в корзине неавторизован', lastname)
        self.fill_element('Имя в корзине неавторизован', name)
        self.fill_element('Отчество в корзине неавторизован', patronymic)
        self.fill_element('Телефон в корзине неавторизован', phone)
        self.fill_element('Емаил в корзине неавторизован', email)
        self.fill_element('Дата рождения в корзине неавторизован', date_born)


    @allure.step("Добавить пассажиров в корзину неавторизованного: взрослых={adults}, детей={children}, младенцев={infants}")
    def add_passengers_to_basket_noauth(self, adults: int, children: int, infants: int):
        for _ in range(adults):
            self.click_element('Плюс взрослый в корзине неавторизованного клиента')
        for _ in range(children):
            self.click_element('Плюс дети в корзине неавторизованного клиента')
        for _ in range(infants):
            self.click_element('Плюс младенцы в корзине неавторизованного клиента')


    @allure.step("Подтверждение телефона при входе в корзине")
    def client_confirm_phone_basket_enter(self, db_connection, phone):
        confirmation_code = None
        max_wait_time = 30
        interval = 2
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            cursor = db_connection.cursor()
            cursor.execute("SELECT confirmation_code FROM users_phone_temp WHERE phone = %s", (phone,))
            result = cursor.fetchone()
            cursor.close()
            if result is not None:
                confirmation_code = result[0]
                break
            time.sleep(interval)
        if confirmation_code is None:
            raise ValueError(f"Код подтверждения не найден для: {phone} после {max_wait_time} секунд ожидания")
        digits = list(str(confirmation_code))
        self.fill_element('Код входа неавторизованного клиента1', digits[0])
        self.fill_element('Код входа неавторизованного клиента2', digits[1])
        self.fill_element('Код входа неавторизованного клиента3', digits[2])
        self.fill_element('Код входа неавторизованного клиента4', digits[3])


 