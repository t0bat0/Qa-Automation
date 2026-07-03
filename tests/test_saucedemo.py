from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest
from pages.postulacion_page import PostulacionPage

registro = logging.getLogger(__name__)
RUTA_DATA = Path(__file__).resolve().parent.parent / "data" / "ui_test_data.json"
RUTA_CVS = Path(__file__).resolve().parent.parent / "data" / "cv_samples"


def _cargar_datos() -> dict:
    with open(RUTA_DATA, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


DATOS = _cargar_datos()


@pytest.fixture(scope="function")
def pagina_postulacion(driver):
    page = PostulacionPage(driver)
    page.open_local_demo()
    page.reset_registry()
    return page


@pytest.mark.parametrize(
    "caso",
    DATOS["postulacion_ui_cases"],
    ids=[c["id"] for c in DATOS["postulacion_ui_cases"]],
)
def test_registro_y_carga_cv(pagina_postulacion: PostulacionPage, caso: dict) -> None:
    """Valida 5 escenarios UI independientes de registro y carga de CV."""
    registro.info("Ejecutando caso UI: %s", caso["id"])
    cv_absoluto = str((RUTA_CVS / caso["cv_file"]).resolve())

    if caso.get("precreate_same_email"):
        registro.info("Precondicion: crear registro previo para duplicado de email")
        pagina_postulacion.crear_postulacion(
            nombre=f"{caso['nombre']} previo",
            email=caso["email"],
            cv_path=str((RUTA_CVS / "cv_ok.pdf").resolve()),
        )
        assert pagina_postulacion.total_postulaciones() == 1

    pagina_postulacion.crear_postulacion(
        nombre=caso["nombre"],
        email=caso["email"],
        cv_path=cv_absoluto,
    )

    mensaje = pagina_postulacion.mensaje_resultado()
    assert caso["expect_message_contains"] in mensaje

    if caso["expect_status"] == "ok":
        assert "exito" in mensaje.lower() or "id generado" in mensaje.lower()
        assert pagina_postulacion.total_postulaciones() >= 1
    else:
        assert "invalido" in mensaje.lower() or "duplicado" in mensaje.lower()
