from __future__ import annotations

import logging

import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import (
    URL_BASE,
    LocalizadoresSauceDemo,
    abrir_pagina_login,
    agregar_primer_producto_al_carrito,
    esperar_pagina_inventario,
    iniciar_sesion,
    obtener_items_inventario_visibles,
    obtener_nombre_y_precio_primer_producto,
)

registro = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def espera(driver) -> WebDriverWait:
    return WebDriverWait(driver, 10)


def test_login_exitoso(driver, espera: WebDriverWait) -> None:
    """Prueba 1: valida login exitoso con credenciales estandar."""
    abrir_pagina_login(driver, espera)
    iniciar_sesion(driver, espera, usuario="standard_user", contrasena="secret_sauce")

    titulo_inventario = esperar_pagina_inventario(espera)

    assert "/inventory.html" in driver.current_url
    assert titulo_inventario == "Products"
    assert "Swag Labs" in driver.title or "Products" in driver.page_source


def test_catalogo_inventario(driver, espera: WebDriverWait) -> None:
    """Prueba 2: valida elementos de inventario y registra datos del primer producto."""
    abrir_pagina_login(driver, espera)
    iniciar_sesion(driver, espera, usuario="standard_user", contrasena="secret_sauce")

    titulo_inventario = esperar_pagina_inventario(espera)
    items = obtener_items_inventario_visibles(espera)

    boton_menu = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.BOTON_MENU))
    selector_ordenamiento = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.SELECT_ORDENAMIENTO))

    nombre_primer_producto, precio_primer_producto = obtener_nombre_y_precio_primer_producto(espera)
    registro.info("Primer producto visible: %s - %s", nombre_primer_producto, precio_primer_producto)

    assert titulo_inventario == "Products"
    assert len(items) > 0
    assert boton_menu.is_displayed()
    assert selector_ordenamiento.is_displayed()
    assert nombre_primer_producto != ""
    assert precio_primer_producto.startswith("$")


def test_carrito_agregar_primer_producto(driver, espera: WebDriverWait) -> None:
    """Prueba 3: agrega un producto al carrito y valida su presencia."""
    abrir_pagina_login(driver, espera)
    iniciar_sesion(driver, espera, usuario="standard_user", contrasena="secret_sauce")
    esperar_pagina_inventario(espera)

    nombre_primer_producto, _ = obtener_nombre_y_precio_primer_producto(espera)
    agregar_primer_producto_al_carrito(espera)

    contador_carrito = espera.until(EC.visibility_of_element_located(LocalizadoresSauceDemo.CONTADOR_CARRITO))
    assert contador_carrito.text.strip() == "1"

    driver.get(f"{URL_BASE}cart.html")
    assert "/cart.html" in driver.current_url

    items_carrito = espera.until(EC.visibility_of_all_elements_located(LocalizadoresSauceDemo.NOMBRES_ITEMS_CARRITO))
    nombres_items_carrito = [item.text.strip() for item in items_carrito]

    assert nombre_primer_producto in nombres_items_carrito
