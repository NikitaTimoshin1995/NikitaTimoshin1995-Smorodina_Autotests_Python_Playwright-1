import pytest
import psycopg2
from playwright.sync_api import Page
import time
from config import host, user, password, db_name

@pytest.fixture
def db_connection():
    """Фикстура для подключения к базе данных."""
    try:
        # Установите соединение с базой данных
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name
        )
        print("(ИНФО) Соединение с PostgreSQL успешно установлено.")
        yield connection  # Возвращаем соединение для использования в тестах
    except Exception as ex:
        print("(ИНФО) Проблема с подключением к PostgreSQL:", ex)
        yield None  # Если соединение не удалось, возвращаем None
    finally:
        if connection:
            connection.close()
            print("(ИНФО) Закрыли соединение с PostgreSQL")

@pytest.fixture
def intercept_requests(page: Page):
    """Фикстура для перехвата запросов."""
    
    # Список для хранения информации о перехваченных запросах
    requests = []
    active_requests_count = 0  # Счетчик активных запросов

    # Настройка перехвата запросов
    def log_request(request):
        nonlocal active_requests_count
        # Проверяем, начинается ли URL с указанного префикса
        if request.url.startswith("https://ff.kis.v2.scr.kaspersky-labs.com/"):
            return  # Пропускаем этот запрос

        # Записываем время и URL запроса
        log_time = time.strftime('%H:%M:%S')
        print(f"{log_time} - Запрос: {request.method} {request.url}")  # Логируем метод и URL
        
        requests.append(request)
        active_requests_count += 1  # Увеличиваем счетчик активных запросов
        
        # Выводим текущий статус активных запросов
        print(f"(ИНФО) Активные запросы: {active_requests_count}, URL: {[req.url for req in requests]}")

    # Настройка обработчика окончаний запросов
    def log_response(response):
        nonlocal active_requests_count
        active_requests_count -= 1  # Уменьшаем счетчик активных запросов
        if active_requests_count < 0:  # Защита на случай, если счетчик выйдет за границы
            active_requests_count = 0
        
        # Выводим текущий статус активных запросов
        print(f"(ИНФО) Активные запросы: {active_requests_count}")

    # Применяем перехватчик запросов и ответов к странице
    page.on("request", log_request)
    page.on("response", log_response)

    # Отдаем управление тесту
    yield requests

    # Очищаем список после завершения теста
    requests.clear()