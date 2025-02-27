import pytest
from playwright.sync_api import Page
import time

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