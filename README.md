# entrega-automation-testing-tobias-ezequiel-tempra

Framework de automatizacion de pruebas hibrido (UI + API) construido en Python para validar flujos funcionales criticos con enfoque en calidad, trazabilidad y mantenibilidad.

## 1. Proposito del Proyecto

Este repositorio implementa una solucion de automatizacion integral para pruebas de interfaz y servicios HTTP, alineada con una estrategia de validacion end-to-end en dos capas:

1. Capa UI (Selenium + Pytest + POM): valida el flujo completo de registro y carga de CV, incluyendo escenarios positivos y negativos con datos externos parametrizados.
2. Capa API (Requests + Pytest): valida operaciones REST con metodos GET, POST y DELETE, aserciones de estado y contenido JSON, y encadenamiento dinamico de datos entre requests.

La arquitectura fue diseniada para soportar crecimiento del proyecto, con separacion de responsabilidades, reutilizacion de componentes y ejecucion independiente de cada caso de prueba.

| Objetivo | Implementacion en la suite |
|---|---|
| Independencia de pruebas | Cada test crea su propio contexto y no depende del resultado de otro |
| Escalabilidad | Estructura por capas: pages, tests, data, conftest |
| Trazabilidad | Logging en tests y Page Objects + reportes HTML |
| Evidencia de fallos | Capturas automaticas con timestamp y adjunto en reporte |
| Cobertura funcional | UI parametrizada (5 casos) + API independiente (3 casos) |

## 2. Tecnologias Utilizadas

- Python
	- Lenguaje base para implementar framework, tests, fixtures y utilidades.
- Pytest
	- Runner principal de pruebas, parametrizacion, aserciones y hooks de ejecucion.
- Selenium WebDriver
	- Automatizacion de navegador para pruebas funcionales de interfaz.
- Requests
	- Ejecucion de pruebas API sobre endpoints HTTP con validaciones de status y payload.
- pytest-html
	- Generacion de reporte visual HTML para auditoria de corrida.
- webdriver-manager
	- Gestion automatizada del driver de Chrome para simplificar setup.

| Componente | Rol tecnico |
|---|---|
| Pytest | Orquestacion de la suite, fixtures, hooks, reporte |
| Selenium | Interaccion con elementos UI, validacion de comportamiento visual/funcional |
| Requests | Validacion de contratos basicos API y flujo de datos encadenado |
| POM | Encapsulacion de localizadores y acciones de negocio |
| JSON externo | Separacion de datos de prueba vs logica de test |

## 3. Estructura del Proyecto

Arbol de directorios con descripcion funcional:

~~~text
entrega-automation-testing-tobias-ezequiel-tempra/
├─ conftest.py
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ ui_test_data.json
│  └─ cv_samples/
│     ├─ cv_ok.pdf
│     ├─ cv_ok.docx
│     └─ cv_invalido.txt
├─ pages/
│  ├─ __init__.py
│  ├─ base_page.py
│  └─ postulacion_page.py
├─ reports/
│  ├─ reporte.html
│  ├─ reporte_es.html
│  ├─ execution.log
│  └─ screenshots/
│     └─ YYYYMMDD/
├─ tests/
│  ├─ test_saucedemo.py
│  └─ test_api.py
├─ ui_demo/
│  └─ index.html
└─ utils/
	 └─ helpers.py
~~~

Detalle por carpeta/archivo clave:

| Ruta | Funcion |
|---|---|
| conftest.py | Configuracion global de pytest, fixture de navegador, logging y captura automatica en fallos |
| pages/ | Implementacion de Page Object Model |
| pages/base_page.py | Acciones reutilizables (abrir, click, type, upload, lectura de texto) |
| pages/postulacion_page.py | Modelo de la pagina de registro/carga de CV con metodos de negocio |
| tests/test_saucedemo.py | Suite UI parametrizada con 5 casos independientes |
| tests/test_api.py | Suite API con GET, POST, DELETE y encadenamiento por id dinamico |
| data/ui_test_data.json | Fuente externa de datos para casos UI |
| data/cv_samples/ | Archivos de ejemplo para validar formatos permitidos/no permitidos |
| ui_demo/index.html | Aplicacion local controlada para pruebas UI del flujo de postulacion |
| reports/ | Evidencias de ejecucion: reporte HTML, log consolidado y capturas |
| utils/helpers.py | Utilidades de apoyo y compatibilidad de funciones auxiliares |

## 4. Instalacion de Dependencias

### 4.1 Clonado del repositorio (nombre definitivo)

~~~bash
git clone https://github.com/<TU_USUARIO>/entrega-automation-testing-tobias-ezequiel-tempra.git
cd entrega-automation-testing-tobias-ezequiel-tempra
~~~

### 4.2 Crear y activar entorno virtual

Windows PowerShell:

~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

Linux/macOS:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

### 4.3 Instalar dependencias

~~~bash
pip install -r requirements.txt
~~~

### 4.4 Validacion rapida del entorno

~~~bash
pytest --version
~~~

## 5. Ejecucion de las Pruebas

### 5.1 Ejecutar suite completa (UI + API)

~~~bash
pytest -v --html=reports/reporte.html --self-contained-html
~~~

### 5.2 Ejecutar solo suite UI

Incluye 5 casos parametrizados desde el archivo JSON externo:

1. registro_cv_ok_pdf
2. registro_cv_ok_docx
3. email_duplicado
4. email_formato_invalido
5. cv_formato_invalido

~~~bash
pytest -v tests/test_saucedemo.py --html=reports/reporte_ui.html --self-contained-html
~~~

### 5.3 Ejecutar solo suite API

Incluye 3 casos independientes:

1. GET de recurso existente y validacion de JSON
2. POST de creacion y validacion de estructura
3. POST + DELETE encadenado con id dinamico retornado por la API

~~~bash
pytest -v tests/test_api.py --html=reports/reporte_api.html --self-contained-html
~~~

### 5.4 Comandos utiles de depuracion

~~~bash
pytest -v -s
pytest -v --maxfail=1
pytest -v -k "api"
pytest -v -k "registro"
~~~

## 6. Interpretacion de Reportes y Logs

### 6.1 Reporte visual HTML de Pytest

Al finalizar una corrida con pytest-html se genera un reporte principal en:

~~~text
reports/reporte.html
~~~

Como abrirlo:

1. Desde VS Code: abrir el archivo directamente.
2. Desde explorador del sistema: doble click en el archivo HTML.

Que revisar en el reporte:

- Total de casos ejecutados, aprobados, fallidos y omitidos.
- Duracion por test.
- Traza de error cuando un caso falla.
- Adjuntos de captura si hubo error en UI.

### 6.2 Capturas automaticas al fallar

Las capturas se guardan automaticamente con fecha y timestamp en:

~~~text
reports/screenshots/YYYYMMDD/
~~~

Formato de nombre:

~~~text
YYYYMMDD_HHMMSS_<nodeid_del_test>.png
~~~

Estas imagenes tambien quedan adjuntas al reporte HTML para acelerar el analisis de causa raiz.

### 6.3 Log de ejecucion para debugging

El log consolidado de la corrida se guarda en:

~~~text
reports/execution.log
~~~

Incluye:

- Inicio y fin de acciones relevantes en tests y Page Objects.
- Detalle de pasos funcionales (navegacion, carga de datos, llamados API).
- Contexto temporal para reconstruir secuencia de falla.

Consulta rapida de ultimas lineas:

Windows PowerShell:

~~~powershell
Get-Content reports/execution.log -Tail 80
~~~

Linux/macOS:

~~~bash
tail -n 80 reports/execution.log
~~~

## Criterios de Cumplimiento Cubiertos

| Requisito de consigna | Estado |
|---|---|
| Framework Python con Pytest + Selenium + POM | Cumplido |
| 5 casos UI independientes con positivos y negativos | Cumplido |
| Datos UI externos (JSON/CSV) | Cumplido (JSON) |
| Capturas automaticas y adjunto al HTML | Cumplido |
| Pruebas API con requests (GET, POST, DELETE, JSON, id dinamico) | Cumplido |
| Logging integrado en Pages y tests | Cumplido |

## Autor

Proyecto desarrollado para el Trabajo Final Integrador de Automatizacion de Pruebas.
