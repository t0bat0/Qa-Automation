# pre-entrega-automation-testing-tobias-ezequiel-tempra

Proyecto de automatizacion de pruebas web para [www.saucedemo.com](https://www.saucedemo.com/) utilizando Python, Selenium WebDriver y Pytest.

## Proposito

Validar funcionalidades criticas del flujo de compra inicial en SauceDemo:

- Login exitoso.
- Visualizacion del catalogo de productos.
- Agregado de producto al carrito.

La suite esta disenada con pruebas independientes entre si: cada test inicializa su propio navegador y no depende del resultado de otro.

## Tecnologias utilizadas

- Python 3.10+
- Selenium WebDriver
- Pytest
- pytest-html
- webdriver-manager

## Estructura del proyecto

- `tests/test_saucedemo.py`: Casos de prueba requeridos.
- `utils/helpers.py`: Helpers reutilizables y localizadores.
- `conftest.py`: Fixtures de setup/teardown y captura automatica en fallos.
- `requirements.txt`: Dependencias del proyecto.
- `reports/`: Reportes HTML y capturas de pantalla en caso de fallo.

## Instalacion paso a paso

1. Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd pre-entrega-automation-testing-tobias-ezequiel-tempra
```

2. Crear y activar entorno virtual:

### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecucion de pruebas

Comando para ejecutar pruebas y generar reporte HTML de pytest-html:

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html
```

Comando recomendado para un reporte embebido (mejor visualizacion en VS Code):

```bash
pytest tests/test_saucedemo.py -v --html=reports/reporte.html --self-contained-html
```

Adicionalmente, al finalizar cada corrida se genera un reporte en espanol en:

- `reports/reporte_es.html`

## Evidencias de fallo

Si un test falla, `conftest.py` guarda automaticamente una captura en `reports/` con nombre que incluye test y timestamp.
