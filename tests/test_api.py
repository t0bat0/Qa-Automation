from __future__ import annotations

import logging

import requests

logger = logging.getLogger(__name__)
BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_recurso_existente() -> None:
    """GET: valida codigo 200 y estructura del JSON para un recurso existente."""
    logger.info("Ejecutando GET de post existente")
    respuesta = requests.get(f"{BASE_URL}/posts/1", timeout=20)

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()

    assert cuerpo["id"] == 1
    assert "title" in cuerpo
    assert "body" in cuerpo
    assert "userId" in cuerpo


def test_post_crear_recurso() -> None:
    """POST: valida codigo 201 y estructura del JSON del recurso creado."""
    payload = {
        "title": "talento-lab",
        "body": "api testing",
        "userId": 1,
    }
    logger.info("Ejecutando POST de creacion de recurso con payload: %s", payload)

    respuesta = requests.post(f"{BASE_URL}/posts", json=payload, timeout=20)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()

    assert cuerpo["title"] == payload["title"]
    assert cuerpo["body"] == payload["body"]
    assert cuerpo["userId"] == payload["userId"]
    assert "id" in cuerpo


def test_delete_endpoint_204() -> None:
    """DELETE: valida explicitamente status 204 en endpoint publico de prueba."""
    logger.info("Ejecutando DELETE sobre endpoint de estado 204")
    respuesta = requests.delete("https://httpstat.us/204", timeout=20)

    assert respuesta.status_code == 204
    assert respuesta.text == ""


def test_post_y_delete_encadenado() -> None:
    """POST + DELETE: crea recurso y elimina usando id dinamico retornado (encadenamiento)."""
    payload = {
        "title": "encadenado",
        "body": "post-delete",
        "userId": 9,
    }
    logger.info("Iniciando encadenamiento POST->DELETE")

    crear = requests.post(f"{BASE_URL}/posts", json=payload, timeout=20)
    assert crear.status_code == 201

    cuerpo = crear.json()
    assert "id" in cuerpo
    resource_id = cuerpo["id"]
    logger.info("Recurso creado con id dinamico: %s", resource_id)

    eliminar = requests.delete(f"{BASE_URL}/posts/{resource_id}", timeout=20)
    assert eliminar.status_code in (200, 204)
