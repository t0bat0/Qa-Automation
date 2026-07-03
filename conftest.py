from __future__ import annotations

import html
import logging
import os
import re
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

RESULTADOS_PRUEBAS: list[dict[str, str | float]] = []


def pytest_configure(config: pytest.Config) -> None:
    """Configura logging global para consola y archivo."""
    os.makedirs("reports", exist_ok=True)
    ruta_log = os.path.join("reports", "execution.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(ruta_log, encoding="utf-8"),
        ],
        force=True,
    )


@pytest.fixture(scope="function")
def navegador() -> webdriver.Chrome:
    """Inicializa y cierra una instancia nueva del navegador por prueba."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")

    servicio = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servicio, options=opciones)
    driver.implicitly_wait(0)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def driver(navegador: webdriver.Chrome) -> webdriver.Chrome:
    """Alias de compatibilidad para tests que aun usan el nombre driver."""
    return navegador


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    """Adjunta reporte por test y guarda captura automaticamente al fallar."""
    resultado_hook = yield
    reporte = resultado_hook.get_result()
    setattr(item, f"rep_{reporte.when}", reporte)

    if reporte.when == "call":
        detalle_error = ""
        if reporte.failed and hasattr(reporte, "longreprtext"):
            detalle_error = str(reporte.longreprtext)

        RESULTADOS_PRUEBAS.append(
            {
                "nombre": item.nodeid,
                "resultado": reporte.outcome,
                "duracion": reporte.duration,
                "detalle": detalle_error,
            }
        )

    if reporte.when == "call" and reporte.failed:
        driver_actual = item.funcargs.get("navegador") or item.funcargs.get("driver")
        if driver_actual is None:
            return

        fecha = datetime.now().strftime("%Y%m%d")
        carpeta_screens = os.path.join("reports", "screenshots", fecha)
        os.makedirs(carpeta_screens, exist_ok=True)
        nombre_test_seguro = re.sub(r"[^A-Za-z0-9_.-]", "_", item.nodeid)
        marca_tiempo = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{marca_tiempo}_{nombre_test_seguro}.png"
        ruta_captura = os.path.join(carpeta_screens, nombre_archivo)

        if driver_actual.save_screenshot(ruta_captura):
            html_plugin = item.config.pluginmanager.getplugin("html")
            if html_plugin is not None:
                extras = getattr(reporte, "extras", [])
                extras.append(html_plugin.extras.image(ruta_captura, name="screenshot"))
                reporte.extras = extras


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    """Genera un reporte HTML adicional en espanol con resultados de la corrida."""
    os.makedirs("reports", exist_ok=True)

    total = len(RESULTADOS_PRUEBAS)
    aprobadas = sum(1 for r in RESULTADOS_PRUEBAS if r["resultado"] == "passed")
    fallidas = sum(1 for r in RESULTADOS_PRUEBAS if r["resultado"] == "failed")
    omitidas = sum(1 for r in RESULTADOS_PRUEBAS if r["resultado"] == "skipped")

    filas_html = []
    traduccion_estado = {
        "passed": "Aprobada",
        "failed": "Fallida",
        "skipped": "Omitida",
    }

    for resultado in RESULTADOS_PRUEBAS:
        clase_resultado = str(resultado["resultado"])
        nombre = html.escape(str(resultado["nombre"]))
        estado = html.escape(traduccion_estado.get(clase_resultado, clase_resultado))
        duracion = f"{float(resultado['duracion']):.2f}s"
        detalle = html.escape(str(resultado["detalle"]))

        if detalle:
            detalle_html = (
                f"<details><summary>Ver detalle</summary><pre>{detalle}</pre></details>"
            )
        else:
            detalle_html = "-"

        filas_html.append(
            f"<tr><td>{nombre}</td><td class='{clase_resultado}'>{estado}</td><td>{duracion}</td><td>{detalle_html}</td></tr>"
        )

    generado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    contenido_html = f"""<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='utf-8'>
  <title>Reporte de pruebas (ES)</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 24px; background: #f7f9fc; color: #1b1f24; }}
    h1 {{ margin-bottom: 8px; }}
    .resumen {{ margin: 0 0 16px; }}
    .tarjetas {{ display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 18px; }}
    .tarjeta {{ background: #fff; border-radius: 8px; padding: 10px 14px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d8dee6; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #eef2f7; }}
    .passed {{ color: #0a7b34; font-weight: 600; }}
    .failed {{ color: #b42318; font-weight: 600; }}
    .skipped {{ color: #8a6d1d; font-weight: 600; }}
    pre {{ white-space: pre-wrap; margin: 8px 0 0; }}
  </style>
</head>
<body>
  <h1>Reporte de ejecucion de pruebas</h1>
  <p class='resumen'>Generado: {generado}</p>
  <div class='tarjetas'>
    <div class='tarjeta'><strong>Total:</strong> {total}</div>
    <div class='tarjeta'><strong>Aprobadas:</strong> {aprobadas}</div>
    <div class='tarjeta'><strong>Fallidas:</strong> {fallidas}</div>
    <div class='tarjeta'><strong>Omitidas:</strong> {omitidas}</div>
    <div class='tarjeta'><strong>Exit status:</strong> {exitstatus}</div>
  </div>
  <table>
    <thead>
      <tr>
        <th>Caso de prueba</th>
        <th>Resultado</th>
        <th>Duracion</th>
        <th>Detalle</th>
      </tr>
    </thead>
    <tbody>
      {''.join(filas_html)}
    </tbody>
  </table>
</body>
</html>
"""

    with open(os.path.join("reports", "reporte_es.html"), "w", encoding="utf-8") as archivo:
        archivo.write(contenido_html)
