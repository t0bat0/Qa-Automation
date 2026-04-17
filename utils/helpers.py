from __future__ import annotations

from typing import Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL_BASE = "https://www.saucedemo.com/"


class LocalizadoresSauceDemo:
    INPUT_USUARIO = (By.ID, "user-name")
    INPUT_CONTRASENA = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")

    TITULO_PAGINA = (By.CSS_SELECTOR, "span.title")
    LOGO_APP = (By.CSS_SELECTOR, "div.app_logo")

    ITEMS_INVENTARIO = (By.CSS_SELECTOR, "div.inventory_item")
    NOMBRE_PRIMER_PRODUCTO = (By.CSS_SELECTOR, "div.inventory_item:first-child div.inventory_item_name")
    PRECIO_PRIMER_PRODUCTO = (By.CSS_SELECTOR, "div.inventory_item:first-child div.inventory_item_price")
    BOTON_AGREGAR_PRIMER_PRODUCTO = (By.CSS_SELECTOR, "div.inventory_item:first-child button.btn_inventory")

    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    SELECT_ORDENAMIENTO = (By.CSS_SELECTOR, "select.product_sort_container")
    LINK_CARRITO = (By.CSS_SELECTOR, "a.shopping_cart_link")
    CONTADOR_CARRITO = (By.CSS_SELECTOR, "span.shopping_cart_badge")

    NOMBRES_ITEMS_CARRITO = (By.CSS_SELECTOR, "div.cart_item div.inventory_item_name")


def abrir_pagina_login(driver: WebDriver, espera: WebDriverWait) -> None:
    driver.get(URL_BASE)
    espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.INPUT_USUARIO))


def iniciar_sesion(driver: WebDriver, espera: WebDriverWait, usuario: str, contrasena: str) -> None:
    input_usuario = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.INPUT_USUARIO))
    input_contrasena = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.INPUT_CONTRASENA))
    boton_login = espera.until(EC.element_to_be_clickable(LocalizadoresSauceDemo.BOTON_LOGIN))

    input_usuario.clear()
    input_usuario.send_keys(usuario)
    input_contrasena.clear()
    input_contrasena.send_keys(contrasena)
    boton_login.click()


def esperar_pagina_inventario(espera: WebDriverWait) -> str:
    titulo = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.TITULO_PAGINA))
    espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.LOGO_APP))
    return titulo.text.strip()


def obtener_items_inventario_visibles(espera: WebDriverWait):
    espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.ITEMS_INVENTARIO))
    return espera.until(EC.visibility_of_all_elements_located(LocalizadoresSauceDemo.ITEMS_INVENTARIO))


def obtener_nombre_y_precio_primer_producto(espera: WebDriverWait) -> Tuple[str, str]:
    nombre_producto = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.NOMBRE_PRIMER_PRODUCTO)).text.strip()
    precio_producto = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.PRECIO_PRIMER_PRODUCTO)).text.strip()
    return nombre_producto, precio_producto


def agregar_primer_producto_al_carrito(espera: WebDriverWait) -> None:
    boton_agregar = espera.until(EC.element_to_be_clickable(LocalizadoresSauceDemo.BOTON_AGREGAR_PRIMER_PRODUCTO))
    boton_agregar.click()
