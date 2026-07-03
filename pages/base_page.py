from __future__ import annotations

import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def open(self, url: str) -> None:
        self.logger.info("Abriendo URL: %s", url)
        self.driver.get(url)

    def type(self, locator: tuple[str, str], text: str) -> None:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def click(self, locator: tuple[str, str]) -> None:
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def upload_file(self, locator: tuple[str, str], absolute_path: str) -> None:
        self.logger.info("Subiendo archivo: %s", absolute_path)
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.send_keys(absolute_path)

    def text_of(self, locator: tuple[str, str]) -> str:
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text.strip()
