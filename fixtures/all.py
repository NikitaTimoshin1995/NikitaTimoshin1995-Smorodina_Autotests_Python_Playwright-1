import pytest
from playwright.sync_api import Page

@pytest.fixture
def intercept_requests(page: Page):
    """Фикстура для перехвата запросов."""
    
    # Список для хранения информации о перехваченных запросах
    requests = []

    # Настройка перехвата запросов
    def log_request(route):
        requests.append(route)
        route.continue_()

    # Применяем перехватчик запросов к странице
    page.on("route", log_request)

    # Отдаем управление тесту
    yield requests
  