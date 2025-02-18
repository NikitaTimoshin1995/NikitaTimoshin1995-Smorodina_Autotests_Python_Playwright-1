# conftest.py
from playwright.sync_api import sync_playwright

def pytest_configure(config):
    if config.getoption("--headed"):
        config.option.headless = False