import allure
from playwright.sync_api import Page, TimeoutError
from Locators.loc_all_directories import ALL_LOCATORS
import json
import time
from pathlib import Path


class BasePage:
    def __init__(self, page: Page):
        self.page = page


    @allure.step("Открытие страницы {url}")
    def open_page(self, url: str):
        self.page.goto(url)
        # self.wait_for_full_load() На удаление


    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_full_load(self):
        try:
            self.page.wait_for_load_state('networkidle', timeout=30000)
        except TimeoutError:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_on_timeout",
                attachment_type=allure.attachment_type.PNG
            )
            print("Предупреждение: Время ожидания загрузки страницы истекло. Продолжаем выполнение теста.")


    @allure.step("Кликнуть на элемент '{element_name}'")
    def click_element(self, element_name: str):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            raise ValueError(f"Элемент '{element_name}' не найден.")

        locator = self.page.locator(f'xpath={xpath}')
        try:
            locator.click()
        except TimeoutError as e:
            error_message = str(e)
            if 'subtree intercepts pointer events' in error_message:
                print(f"Клик по элементу '{element_name}' заблокирован оверлеем. Попытка закрыть подписку и повторить.")
                self.close_subscription_if_present()
                locator.click()
            else:
                raise

    @allure.step("Кликнуть на элемент с текстом '{text}'")
    def click_element_by_text(self, text: str, exact_match: bool = False, timeout: int = 30000, nth: int = None):
        try:
            if exact_match:
                locator = self.page.get_by_text(text, exact=True)
            else:
                locator = self.page.get_by_text(text)
            if nth is not None:
                locator = locator.nth(nth)        
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
        except TimeoutError:
            raise TimeoutError(f"Элемент с текстом '{text}' не найден в течение {timeout}ms")
    
    
    @allure.step("Заполнить элемент '{element_name}' значением '{value}'")
    def fill_element(self, element_name: str, value: str):
        xpath = ALL_LOCATORS.get(element_name)
        if xpath:
            self.page.locator(f'xpath={xpath}').fill(value)
        else:
            raise ValueError(f"Элемент '{element_name}' не найден.")


    @allure.step("Очистить элемент '{element_name}'")
    def clear_element(self, element_name: str):
        xpath = ALL_LOCATORS.get(element_name)
        if xpath:
            self.page.locator(f'xpath={xpath}').clear()
        else:
            raise ValueError(f"Элемент '{element_name}' не найден.")
        

    @allure.step("Переключиться на новую вкладку")
    def switch_to_new_tab(self, timeout=30000):
        # Ждем появления новой вкладки
        new_page = self.page.context.wait_for_event('page', timeout=timeout)
        # Переключаемся на новую вкладку
        new_page.bring_to_front()
        return new_page


    @allure.step("Загрузить фото через клик и выбор файлов в создании тура")
    def upload_photos_via_click(self, element_name: str, number_photo: int, *file_paths):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            raise ValueError(f"Элемент '{element_name}' не найден в справочнике локаторов.")
        if not file_paths:
            raise ValueError("Не указаны пути к файлам для загрузки.")
        try:
            upload_element = self.page.locator(f'xpath={xpath}')
            with self.page.expect_file_chooser(timeout=60000) as fc_info:
                upload_element.click()
            file_chooser = fc_info.value
            file_chooser.set_files(list(file_paths))
            self.page.wait_for_selector(
                f"text=Загружено {number_photo} из 10 фото",
                timeout=30000
            ) 
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_upload_failed",
                attachment_type=allure.attachment_type.PNG
            )
            raise Exception(f"Ошибка при загрузке файлов: {str(e)}")
        

    @allure.step("Навести курсор на элемент '{element_name}'")
    def hover_element(self, element_name: str):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            raise ValueError(f"Элемент '{element_name}' не найден в справочнике локаторов.") 
        try:
            element = self.page.locator(f'xpath={xpath}')
            element.hover()
            self.page.wait_for_timeout(1000)
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"hover_failed_{element_name}",
                attachment_type=allure.attachment_type.PNG
            )
            raise Exception(f"Ошибка при наведении на элемент '{element_name}': {str(e)}")
        

    @allure.step("Загрузить фото через клик и выбор файлов в создании тура")
    def upload_photos_via_click_general(self, element_name: str, number_photo: int, *file_paths):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            raise ValueError(f"Элемент '{element_name}' не найден в справочнике локаторов.")
        if not file_paths:
            raise ValueError("Не указаны пути к файлам для загрузки.")
        try:
            upload_element = self.page.locator(f'xpath={xpath}')
            with self.page.expect_file_chooser(timeout=60000) as fc_info:
                upload_element.click()
            file_chooser = fc_info.value
            file_chooser.set_files(list(file_paths))
            self.page.wait_for_selector(
                f"text=Загружено {number_photo} из 5 фото",
                timeout=30000
            ) 
        except Exception as e:
            allure.attach(
                self.page.screenshot(full_page=True),
                name="screenshot_upload_failed",
                attachment_type=allure.attachment_type.PNG
            )
            raise Exception(f"Ошибка при загрузке файлов: {str(e)}")
        

    @allure.step("Разрешить доступ к местоположению и установить координаты")
    def allow_location_access(self, latitude: float = 55.7558, longitude: float = 37.6173, accuracy: float = 50):
        try:
            # Разрешаем доступ к геолокации
            self.page.context.grant_permissions(['geolocation'])
            # Устанавливаем конкретные координаты
            self.page.context.set_geolocation({
                'latitude': latitude,
                'longitude': longitude,
                'accuracy': accuracy
            })
            # Обрабатываем возможные диалоги автоматически
            self.page.on('dialog', lambda dialog: dialog.accept())
            print(f"Доступ к местоположению разрешен. Координаты: ({latitude}, {longitude})")
        except Exception as e:
            print(f"Ошибка при настройке геолокации: {e}")


    @allure.step("Кликнуть на элемент '{element_name}' если он присутствует")
    def click_element_if_present(self, element_name: str, timeout: int = 1000):
        xpath = ALL_LOCATORS.get(element_name)
        if not xpath:
            print(f"Предупреждение: Ключ '{element_name}' не найден в справочнике локаторов")
            return
        try:
            # Используем wait_for с состоянием visible
            locator = self.page.locator(f'xpath={xpath}')
            locator.wait_for(state="visible", timeout=timeout)
            locator.click()
            print(f"Элемент '{element_name}' найден и кликнут")
        except TimeoutError:
            print(f"Элемент '{element_name}' не стал видимым в течение {timeout}ms")
            # Дополнительная проверка: может элемент есть, но скрыт?
            if locator.count() > 0:
                print(f"Элемент '{element_name}' присутствует в DOM, но не видим")
        except Exception as e:
            print(f"Ошибка при работе с элементом '{element_name}': {str(e)}")


    @allure.step("Закрыть виджет чата, если он открыт")
    def close_livechat_if_present(self):
        selectors = [
            "button.header-close-btn",
            "button.invitation-close",
            ".livechat-window.dark button.header-close-btn",
            ".livechat-window.light button.header-close-btn",
            ".livechat-button.open",
        ]
        for selector in selectors:
            locator = self.page.locator(selector).first
            try:
                if locator.count() > 0:
                    locator.click(force=True, timeout=5000)
                    print(f"Livechat закрыт селектором: {selector}")
                    return True
            except Exception:
                continue
        return False


    def close_subscription_if_present(self, timeout: int = 7000):
        selectors = [
            "button[aria-label='Закрыть']",
            "._container_hygv5_1 button",
            "[aria-label='Подписка на рассылку'] button",
            "div[role='dialog'][aria-label='Подписка на рассылку'] button",
            "[aria-label*='закр']",
        ]
        dialog_selector = "div[role='dialog'][aria-label='Подписка на рассылку'], ._container_hygv5_1"
        end_time = time.time() + timeout / 1000

        while time.time() < end_time:
            for selector in selectors:
                locator = self.page.locator(selector).first
                try:
                    if locator.count() > 0:
                        locator.click(force=True, timeout=5000)
                        print(f"Диалог подписки закрыт селектором: {selector}")
                        self.page.wait_for_timeout(500)
                        return True
                except Exception:
                    continue

            if self.page.locator(dialog_selector).count() == 0:
                return True

            self.page.wait_for_timeout(300)

        try:
            self.page.evaluate(
                "document.querySelectorAll('div[role=\'dialog\'][aria-label=\'Подписка на рассылку\'], ._container_hygv5_1').forEach(el => { el.style.display = 'none'; el.remove(); });"
            )
            print("Диалог подписки скрыт через JS")
            return True
        except Exception as e:
            print(f"Не удалось скрыть диалог подписки через JS: {e}")

        return self.page.locator(dialog_selector).count() == 0


    @allure.step("Кликнуть на элемент с классом, содержащим '{class_part}'")
    def click_element_by_class_part(self, class_part: str, element_type: str = "*", 
                               match_type: str = "contains", timeout: int = 30000,
                               nth: int = 0):
        try:
            if match_type == "starts":
                css_selector = f"{element_type}[class^='{class_part}']"
            elif match_type == "contains":
                css_selector = f"{element_type}[class*='{class_part}']"
            elif match_type == "ends":
                css_selector = f"{element_type}[class$='{class_part}']"
            else:
                raise ValueError("match_type должен быть 'starts', 'contains' или 'ends'")
            locator = self.page.locator(css_selector).nth(nth)
            locator.wait_for(state="visible", timeout=timeout)
            locator.scroll_into_view_if_needed()
            is_disabled = locator.get_attribute("disabled")
            if is_disabled:
                raise Exception(f"Элемент с классом '{class_part}' заблокирован (disabled)")
            locator.click(timeout=timeout)

            allure.attach(
                f"Успешно кликнули на {element_type} с классом, который {match_type} на '{class_part}' (индекс {nth})",
                name="Click Success"
            )
        except TimeoutError:
            error_msg = f"Элемент {element_type} с классом, который {match_type} на '{class_part}' не найден в течение {timeout}ms"
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"screenshot_class_{match_type}_{class_part}",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(error_msg, name="Error Message")
            raise TimeoutError(error_msg)
        except Exception as e:
            error_msg = f"Ошибка при клике на элемент: {str(e)}"
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"screenshot_error_{class_part}",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(error_msg, name="Unexpected Error")
            raise


    @allure.step("Сохранить cookies авторизации")
    def save_auth_cookies(self, page: Page, filename: str = "auth_cookies.json"):
        cookies = page.context.cookies()
        Path(filename).write_text(json.dumps(cookies))
        print(f"Cookies сохранены в {filename}")


    @allure.step("Очистить cookies авторизации")
    def clear_auth_cookies(self, page: Page):
        page.context.clear_cookies()
        print("Cookies авторизации очищены")
        page.evaluate("() => localStorage.clear()")
        page.evaluate("() => sessionStorage.clear()")
        print("LocalStorage и sessionStorage очищены")