from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class PostulacionPage(BasePage):
    INPUT_NOMBRE = (By.ID, "nombre")
    INPUT_EMAIL = (By.ID, "email")
    INPUT_CV = (By.ID, "cvFile")
    BTN_ENVIAR = (By.ID, "submitBtn")
    MSG_RESULTADO = (By.ID, "resultMessage")

    def open_local_demo(self) -> None:
        project_root = Path(__file__).resolve().parent.parent
        demo_path = project_root / "ui_demo" / "index.html"
        self.open(demo_path.as_uri())

    def reset_registry(self) -> None:
        self.logger.info("Reseteando datos locales de la demo")
        self.driver.execute_script("window.qaDemoApi.resetData();")

    def crear_postulacion(self, nombre: str, email: str, cv_path: str) -> None:
        self.logger.info("Completando postulacion para: %s", email)
        self.type(self.INPUT_NOMBRE, nombre)
        self.type(self.INPUT_EMAIL, email)
        self.upload_file(self.INPUT_CV, cv_path)
        self.click(self.BTN_ENVIAR)

    def mensaje_resultado(self) -> str:
        return self.text_of(self.MSG_RESULTADO)

    def total_postulaciones(self) -> int:
        total = self.driver.execute_script("return window.qaDemoApi.getTotal();")
        return int(total)
