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

    # Настройка перехвата запросов
    def log_request(request):
        # Проверяем, начинается ли URL с указанного префикса
        if request.url.startswith("https://ff.kis.v2.scr.kaspersky-labs.com/"):
            return  # Пропускаем этот запрос

        # Записываем время и URL запроса
        log_time = time.strftime('%H:%M:%S')
        print(f"{log_time} - Запрос: {request.method} {request.url}")  # Логируем метод и URL

        requests.append(request)

    # Применяем перехватчик запросов к странице
    page.on("request", log_request)

    # Отдаем управление тесту
    yield requests

    # Очищаем список после завершения теста
    requests.clear()