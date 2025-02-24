import pytest
from playwright.sync_api import sync_playwright
from data.constants import URL

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    """Фикстура для создания новой страницы Playwright."""
    page = browser.new_page()
    page.goto(URL)
    yield page
    page.close()

@pytest.fixture
def intercept_requests(page):
    """Фикстура для перехвата запросов."""
    requests = []
    page.on("request", lambda request: requests.append(request))
    yield requests
    # Очистка или обработка запросов после выполнения теста