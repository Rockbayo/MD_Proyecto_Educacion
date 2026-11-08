# Proyecto de Minería de Datos: Educación, Acceso y Desempeño Académico

## Descripción del Proyecto
Investigación analítica orientada a medir y caracterizar el impacto de la brecha digital y los determinantes socioeconómicos en los resultados del examen de Estado Saber 11 (ICFES) en Colombia. Basado en la metodología **CRISP-DM**, el proyecto procesa e integra más de **4.5 millones de microdatos estudiantiles** en una ventana temporal de 14 semestres continuos (**2019-1 a 2025-2**), transitando desde el aseguramiento de calidad y pipelines ETL automatizados en SSIS, pasando por tableros DAX en Power BI, hasta la consolidación de un **Data Warehouse relacional con modelo estrella OLAP** y visualizaciones analíticas interactivas en Flask.

---

## Fases del Ciclo de Vida Metodológico

| Fase | Enfoque Metodológico | Descripción Técnica y Entregables |
| :--- | :--- | :--- |
| **Fase 1** | Comprensión del Negocio y Datos | Formulación del problema, justificación, diccionario de variables, matriz de necesidades de información y preguntas de investigación. |
| **Fase 2** | Diagnóstico y Calidad de Datos | Perfilamiento estadístico descriptivo, homologación estructural y evaluación de dimensiones de calidad (completitud, validez, consistencia y unicidad). |
| **Fase 3** | Transformación y Pipeline ETL | Pipeline automatizado e idempotente en **SQL Server Integration Services (SSIS)**: limpieza de cadenas Unicode, conversión de tipos, deduplicación y cruce referencial con el DUE. |
| **Fase 4** | Descubrimiento de Conocimiento Evidente | Tableros interactivos en **Power BI Desktop**, formulación de medidas DAX complejas y documentación rigurosa de 12 conocimientos evidentes bajo 8 elementos metodológicos. |
| **Fase 5** | Análisis Multidimensional / OLAP | **Esquema en Estrella Relacional** en SQLite (`edumetrics_olap.db`), operaciones dinámicas (*Drill-Down, Roll-Up, Slice, Dice, Pivot*) y 4 vistas analíticas de desagregación en Flask. |

---

## Arquitectura Dimensional y Modelo Estrella OLAP (Fase 5)
Para superar las limitaciones del análisis bidimensional plano y garantizar cálculos aditivos exactos sin duplicación de métricas, se diseñó un modelo en estrella bajo principios de Ralph Kimball:

```
+-----------------------------------+        +-----------------------------------------+
|            dim_tiempo             |        |              dim_geografia              |
+-----------------------------------+        +-----------------------------------------+
| PK id_tiempo (INTEGER)            |        | PK id_geografia (INTEGER)               |
|    periodo (INT) [20191-20252]    |        |    region_dane (TEXT) [8 Regiones]      |
|    anio (INT) [2019-2025]         |        |    cole_depto_ubicacion (TEXT) [33 Dept]|
|    semestre_num (INT) [1, 2]      |        |    cole_area_ubicacion (TEXT) [URB/RUR] |
|    semestre_etiqueta (TEXT)       |        |    cole_naturaleza (TEXT) [OFIC/NO OFIC]|
|    etapa_pandemia (TEXT)          |        |    cole_calendario (TEXT) [A, B]        |
+-----------------------------------+        +-----------------------------------------+
                  \                                    /
                   \                                  /
            +------------------------------------------------+
            |            fact_resultados_saber11             |
            +------------------------------------------------+
            | PK id_hecho (INTEGER)                          |
            | FK id_tiempo (INTEGER)                         |
            | FK id_geografia (INTEGER)                      |
            | FK id_digital (INTEGER)                        |
            | FK id_socioeconomico (INTEGER)                 |
            |    num_evaluados (INT)                         |
            |    suma_punt_global (INT)                      |
            |    suma_matematicas (INT)                      |
            |    suma_lectura_critica (INT)                  |
            |    suma_c_naturales (INT)                      |
            |    suma_sociales_ciudadanas (INT)              |
            |    suma_ingles (INT)                           |
            |    eval_ingles_presente (INT)                  |
            |    eval_alto_rendimiento (INT) [Punt >= 300]   |
            |    eval_riesgo_bajo (INT)      [Punt < 220]    |
            |    eval_ingles_bilingue (INT)  [Nivel B1/B+]   |
            +------------------------------------------------+
                   /                                  \
                  /                                    \
+-----------------------------------+        +-----------------------------------------+
|        dim_acceso_digital         |        |           dim_socioeconomica            |
+-----------------------------------+        +-----------------------------------------+
| PK id_digital (INTEGER)           |        | PK id_socioeconomico (INTEGER)          |
|    perfil_acceso_tic (TEXT)       |        |    grupo_estrato (TEXT) [Bajo/Med/Alto] |
|    fami_tieneinternet (TEXT)      |        |    fami_estratovivienda (TEXT)          |
|    fami_tienecomputador (TEXT)    |        |    grupo_educacion_padre (TEXT)         |
|    estu_dedicacioninternet (TEXT) |        |    fami_educacionpadre (TEXT)           |
+-----------------------------------+        |    estu_genero (TEXT) [F, M]            |
                                             +-----------------------------------------+
```

### Catálogo de Jerarquías y Navegación Dimensional
1. **Jerarquía Territorial:** Región DANE (8 regiones macro) $\to$ Departamento (33 entidades territoriales) $\to$ Zona de Sede (Urbano / Rural).
2. **Jerarquía Temporal:** Etapa Epidemiológica (Pre-pandemia 2019, Confinamiento 2020-2021, Post-pandemia 2022-2025) $\to$ Año $\to$ Periodo Semestral.
3. **Jerarquía de Capital Cultural:** Grupo Nivel Educativo (Básica Primaria, Secundaria, Superior) $\to$ Grado de Escolaridad Específico del Padre.
4. **Jerarquía de Estratificación y Acceso TIC:** Grupo Estrato (Bajo [1-2], Medio [3-4], Alto [5-6]) $\to$ Perfil de Equipamiento Digital (Exclusión Total, Solo Conexión Móvil, Plena Disponibilidad de Hardware y Red).

---

## Formulación de las 4 Preguntas Analíticas y Operaciones de Cubo

*   **Vista 1 · Desagregación Territorial y Brecha Digital:**
    *   *Pregunta:* ¿Cómo varía la penalización por exclusión digital sobre el puntaje global y matemáticas al desagregar desde la escala regional macro hacia departamentos y zonas urbano-rurales?
    *   *Operaciones:* **Drill-Down / Roll-Up** sobre `dim_geografia` cruzada con `dim_acceso_digital`.
*   **Vista 2 · Dinámica Temporal Pre, Durante y Post-Pandemia:**
    *   *Pregunta:* ¿Cómo varió la brecha de rendimiento entre colegios oficiales y privados a través de las etapas pre-pandemia (2019), confinamiento (2020-2021) y post-pandemia (2022-2025) al controlar por la tenencia de computador en el hogar?
    *   *Operaciones:* **Slice** sobre `dim_tiempo` controlando por sector y tenencia de hardware.
*   **Vista 3 · Mitigación del Capital Cultural Frente a la Carencia Digital:**
    *   *Pregunta:* ¿En qué medida la disponibilidad de computador mitiga el rezago asociado al bajo nivel educativo de los padres en competencias clave (matemáticas, lectura y ciencias)?
    *   *Operaciones:* **Pivot & Slice** rotando matrices de contingencia multidimensionales.
*   **Vista 4 · Intensidad de Uso de Internet, Bilingüismo y Riesgo Crítico:**
    *   *Pregunta:* ¿Cómo se relaciona la dedicación horaria a internet con la tasa de bilingüismo en inglés frente a la probabilidad de caer en rendimiento crítico (< 220 puntos)?
    *   *Operaciones:* **Dice** focalizado en percentiles extremos de la distribución académica.

---

## Estructura del Repositorio
```
MD_Proyecto_Educacion/
├── app.py                              # Servidor Flask y API RESTful analítica para consultas al Data Warehouse
├── requirements.txt                    # Dependencias del entorno de producción
├── data/
│   ├── processed/
│   │   └── edumetrics_olap.db         # Data Warehouse relacional SQLite con modelo estrella cargado (72.3 MB)
│   └── reports/
│       ├── EduMetrics_Etapa5_Informe_Tecnico.pdf
│       ├── Informe_Tecnico_Etapa5_Analisis_Multidimensional.md
│       └── validacion_modelo_estrella.json
├── scripts/
│   ├── 01_extraccion.py               # Extracción y consolidación de microdatos
│   ├── 02_perfilamiento.py            # Análisis estadístico descriptivo
│   ├── 03_dimensiones.py              # Evaluación matemática de calidad de datos
│   ├── crear_modelo_estrella_olap.py  # Creador y cargador del modelo dimensional
│   ├── compilar_informe_pdf.py        # Generador automatizado de informe técnico en PDF
│   └── generar_informe_word.py        # Generador de documentación en DOCX
├── templates/                          # Vistas web modulares en Jinja2 / HTML5
│   ├── base.html                      # Layout maestro con navegación responsiva y modo oscuro
│   ├── etapa1/ a etapa4/              # Vistas documentales de entregables previos
│   └── etapa5/                        # Vistas interactivas de las 4 preguntas analíticas del modelo OLAP
└── static/                            # Activos estáticos, hojas de estilo CSS y librerías frontend (Chart.js)
```

---

## Instrucciones de Instalación y Ejecución Local
1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Rockbayo/MD_Proyecto_Educacion.git
   cd MD_Proyecto_Educacion
   ```
2. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # Linux / macOS:
   source .venv/bin/activate
   ```
3. **Instalar dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Verificación del Modelo Estrella OLAP:**
   La base analítica `data/processed/edumetrics_olap.db` se encuentra incluida y lista para consultar. Para verificar la cuadratura de registros con el dataset maestro o regenerar el esquema:
   ```bash
   python scripts/crear_modelo_estrella_olap.py
   ```
5. **Ejecutar la aplicación web:**
   ```bash
   python app.py
   ```
   * Portal principal: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)  
   * Módulo OLAP (Etapa 5): [http://127.0.0.1:5000/etapa5](http://127.0.0.1:5000/etapa5)

---

## Despliegue en la Nube y Entregables
*   **Aplicación Web en Producción (Render):** [https://md-proyecto-educacion.onrender.com/](https://md-proyecto-educacion.onrender.com/)
*   **Informe Interactivo Power BI (Etapa 4):** [Tableros en Power BI Service](https://app.powerbi.com/groups/me/reports/e88e30a1-d605-413f-a622-3c66297fa2f8?pbi_source=desktop)
*   **Pull Request Oficial Etapa 5:** [PR #29 - Rama feature/etapa-5](https://github.com/Rockbayo/MD_Proyecto_Educacion/pull/29)

---

## Autores e Investigadores
*   **Oscar Giovanni Robayo Olaya** — *Investigador Analista (Calidad, Pipeline ETL y Arquitectura Dimensional)*
*   **Oscar Felipe Delgado** — *Investigador Analista (Pipeline Analítico y Modelado Predictivo)*
*   *Universidad de Cundinamarca - Extensión Chía*  
    *Facultad de Ingeniería · Programa de Ingeniería de Sistemas y Computación (Semestre 2026-II)*
