import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect


@pytest.fixture(scope="session")
def browsers():
    with sync_playwright() as p:
        chromium = p.chromium.launch(headless=False)
        firefox = p.firefox.launch(headless=False)
        webkit = p.webkit.launch(headless=False)
        yield {"chromium": chromium, "firefox": firefox, "webkit": webkit}
        chromium.close()
        firefox.close()
        webkit.close()


@pytest.fixture
def pages(browsers):
    pages = {}
    for browser_name, browser in browsers.items():
        pages[browser_name] = browser.new_page()
    yield pages
    for page in pages.values():
        page.close()


def test_smorodina_flow(pages):
    url = "https://dev.smorodina.ru/"
    button_class = "custom-btn bright btn-greetings large"
    login_button_text = "Войти"
    organizer_button_text = "Организатор туров"

    for browser_name, page in pages.items():
        page.goto(url)
        # Ждем кнопку и кликаем
        page.locator(f".{button_class}").wait_for(state="visible", timeout=10000)
        page.locator(f".{button_class}").click()

        # Ждем кнопку Войти и кликаем
        page.locator(f"text={login_button_text}").wait_for(state="visible", timeout=10000)
        page.locator(f"text={login_button_text}").click()

        # Ждем кнопку Организатор туров и кликаем
        page.locator(f"text={organizer_button_text}").wait_for(state="visible", timeout=10000)
        page.locator(f"text={organizer_button_text}").click()

        # Дополнительная проверка (например, что мы на нужной странице)
        expect(page).to_have_url(url)  # или какой-то другой URL, характерный для шага "Организатор туров"
        # Или проверка, что появился элемент на странице
        # expect(page.locator("...")).to_be_visible()
        page.screenshot(path=f"smorodina_{browser_name}.png")  # Скриншот для отладки