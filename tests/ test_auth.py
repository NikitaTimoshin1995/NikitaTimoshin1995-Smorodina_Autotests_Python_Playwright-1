import pytest
from playwright.sync_api import sync_playwright

def test_slow_navigation_and_h1_check():
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=2000)  # Замедление выполнения в браузере (в миллисекундах)
        page = browser.new_page()

        # Переход на целевую страницу
        page.goto("https://www.example.com") # Замените на URL целевой страницы

        # Проверка заголовка h1
        h1_text = page.locator("h1").inner_text()
        assert h1_text == "Example Domain", "Заголовок h1 не соответствует ожидаемому"

        browser.close()


    

