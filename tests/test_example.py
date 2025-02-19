from playwright.sync_api import sync_playwright

def test_example():
    with sync_playwright() as p:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = browser_type.launch(headless=False)
            page = browser.new_page()
            page.goto("https://example.com")
            print(f"{browser_type.name}: {page.title()}")
            assert page.title() == "Example Domain"
            browser.close()