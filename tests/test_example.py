import pytest
from playwright.sync_api import Page, expect

def test_example(page: Page):
    page.goto('https://dev.smorodina.ru/')
    page.get_by_role('button', name='Искать туры').click()  
    expect(page.get_by_text('Автопутешествия по России')).to_be_visible()