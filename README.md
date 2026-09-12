# Proyecto de Minería de Datos: Educación, Acceso y Desempeño Académico

## Descripción del Proyecto
Análisis del impacto de la brecha digital en los resultados de las pruebas estandarizadas Saber 11 (ICFES) en Colombia. Este proyecto aplica la metodología **CRISP-DM** para evaluar cómo la infraestructura tecnológica (internet, computador) y factores socioeconómicos determinan el rendimiento académico, integrando datos a nivel global, nacional y regional.

## Estructura del Repositorio
El proyecto está estructurado modularmente separando el backend analítico de la visualización en Flask:

*   `/data/`: Contiene los archivos `.gitkeep` para mantener la estructura de datos locales (raw, processed, reports). *Nota: Los microdatos del ICFES no se suben al repositorio por su volumen (+4.5M de registros).*
*   `/scripts/`: Pipeline ETL en Python.
    *   `01_extraccion.py`: Consolidación de microdatos.
    *   `02_perfilamiento.py`: Análisis estadístico descriptivo.
    *   `03_dimensiones.py`: Evaluación matemática de calidad (Completitud, Unicidad, Validez, Consistencia).
*   `/templates/` y `/static/`: Interfaz gráfica web en Flask utilizando Tailwind CSS (Dark Mode).
*   `app.py`: Archivo principal de enrutamiento web.
*   `requirements.txt`: Dependencias del proyecto.

## Instrucciones de Ejecución
1. Clonar el repositorio: `git clone https://github.com/Rockbayo/MD_Proyecto_Educacion.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Descargar los microdatos desde el [Portal de Datos Abiertos - ICFES Saber 11](https://www.datos.gov.co/) y ubicarlos en `/data/raw/`.
4. Ejecutar el pipeline analítico secuencialmente desde la carpeta `/scripts/`.
5. Levantar el entorno web: `python app.py`

## Autores
*   **Oscar Giovanni Robayo Olaya**
*   **Oscar Felipe Delgado**
*   *Universidad de Cundinamarca - Ingeniería de Sistemas y Computación (Semestre 2026-II)*