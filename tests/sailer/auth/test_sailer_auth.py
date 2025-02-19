import pytest
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from fixtures.main import browsers, pages  # Импортируем фикстуры

#Переменные
url = "https://dev.smorodina.ru/"
button_class = "custom-btn bright btn-greetings large"
login_button_text = "Войти"
organizer_button_text = "Организатор туров"


def test_smorodina_flow(pages):
    for browser_name, page in pages.items():
        page.goto(url)
        # Ждем кнопку и кликаем
        
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