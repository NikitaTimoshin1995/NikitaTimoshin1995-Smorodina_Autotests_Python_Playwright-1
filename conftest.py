import pytest
from playwright.sync_api import Page

@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_viewport_size({"width": 1500, "height": 874})
    yield page
    page.close()