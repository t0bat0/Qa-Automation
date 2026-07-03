# pre-entrega-automation-testing-tobias-ezequiel-tempra

Proyecto de automatizacion de pruebas con Python, Selenium WebDriver, Pytest y requests.

## Proposito

Validar de forma automatizada:

- Flujos UI de registro y carga de CV (positivos y negativos) con datos externos.
- Pruebas API independientes con metodos GET, POST y DELETE.

La suite esta disenada con pruebas independientes entre si: cada test inicializa su propio navegador y no depende del resultado de otro.

## Tecnologias utilizadas

- Python 3.10+
- Selenium WebDriver
- Pytest
- pytest-html
- webdriver-manager

## Estructura del proyecto

- `pages/base_page.py`: Base de Page Object Model con acciones reutilizables.
- `pages/postulacion_page.py`: Page Object del flujo de registro/carga de CV.
- `tests/test_saucedemo.py`: Suite UI parametrizada (5 casos de registro/cv).
- `tests/test_api.py`: Suite API con requests (GET/POST/DELETE y encadenamiento de ID).
- `data/ui_test_data.json`: Datos externos de escenarios UI.
- `data/cv_samples/`: Archivos de CV para pruebas de carga (validos e invalidos).
- `ui_demo/index.html`: Demo local para automatizar registro/carga de CV.
- `conftest.py`: Fixtures, logging y captura automatica en fallos con adjunto al reporte HTML.
- `requirements.txt`: Dependencias del proyecto.
- `reports/`: Reportes HTML, logs y capturas en caso de fallo.

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
pytest -v --html=reports/reporte.html
```

Comando recomendado para un reporte embebido (mejor visualizacion en VS Code):

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Adicionalmente, al finalizar cada corrida se genera un reporte en espanol en:

- `reports/reporte_es.html`

## Evidencias de fallo

Si un test falla, `conftest.py` guarda automaticamente una captura en `reports/screenshots/<fecha>/` con nombre que incluye test y timestamp, y la adjunta al reporte visual de pytest-html.
