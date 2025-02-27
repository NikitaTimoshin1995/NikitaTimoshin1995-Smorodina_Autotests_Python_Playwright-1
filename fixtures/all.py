import pytest
from playwright.sync_api import Page

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

        requests.append(request)

    # Применяем перехватчик запросов к странице
    page.on("request", log_request)

    # Отдаем управление тесту
    yield requests

    # Очищаем список после завершения теста
    requests.clear()