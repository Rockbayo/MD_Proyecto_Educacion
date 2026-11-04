# UNIVERSIDAD DE CUNDINAMARCA
## FACULTAD DE INGENIERÍA · PROGRAMA DE INGENIERÍA DE SISTEMAS Y COMPUTACIÓN
### ASIGNATURA: MINERÍA DE DATOS · SEMESTRE 2026-II

---

# INFORME TÉCNICO · ETAPA 5
## ANÁLISIS MULTIDIMENSIONAL / MODELO ESTRELLA OLAP
### PROYECTO: EduMetricsCO — BRECHA DIGITAL Y DESEMPEÑO ACADÉMICO EN SABER 11 (2019-1 A 2025-2)

**Autores e Investigadores:**
* **Oscar Giovanni Robayo Olaya** — *Investigador Analista (Calidad, ETL y Arquitectura Dimensional)*
* **Oscar Felipe Delgado** — *Investigador Analista (Pipeline Analítico y Modelado Predictivo)*

**Fecha de Entrega:** Noviembre de 2026  
**Repositorio GitHub:** [https://github.com/Rockbayo/MD_Proyecto_Educacion](https://github.com/Rockbayo/MD_Proyecto_Educacion)  
**Rama Oficial:** `feature/etapa-5`  
**Aplicación Web Activa:** `http://127.0.0.1:5000/etapa5`

---

## 1. INTRODUCCIÓN Y CONTINUIDAD DEL PROYECTO

El presente documento constituye el informe técnico de la **Etapa 5: Análisis Multidimensional / OLAP**, desarrollada en el marco del proyecto de investigación analítica sobre la educación media en Colombia. 

Dando estricto cumplimiento al principio de continuidad metodológica:
1. **Población y Conjunto de Datos:** Se conserva íntegramente la población analizada desde las etapas anteriores, correspondiente a la totalidad de evaluaciones de estudiantes de grado 11 registradas en las bases maestras de las pruebas **Saber 11 del ICFES**.
2. **Volumen de Datos Tratados:** El análisis se ejecuta sobre **4.541.655 registros individuales** resultantes del pipeline de integración y limpieza multifuente desarrollado en las etapas previas, abarcando **14 periodos académicos semestrales continuos (desde 2019-1 hasta 2025-2)**.
3. **Articulación con Etapas Previas:** Esta etapa profundiza los 12 conocimientos evidentes identificados en la Etapa 4 (desarrollada en Power BI). Mientras que la etapa anterior comprobó asociaciones bivariadas y panorámicas globales, esta etapa implementa un **modelo multidimensional en estrella** sobre una base de datos relacional analítica (SQLite), permitiendo navegar dinámicamente mediante operaciones de *Drill-Down, Roll-Up, Slice, Dice y Pivot*.

---

## 2. DESCRIPCIÓN Y PROPÓSITO DE LOS DATOS

* **Fuente Oficial:** Instituto Colombiano para la Evaluación de la Educación (ICFES), catálogo oficial de microdatos abiertos.
* **URL de Consulta de Origen:** [https://www.icfes.gov.co/data-icfes](https://www.icfes.gov.co/data-icfes)
* **Fuentes Secundarias Integradas:** Directorio Único de Establecimientos Educativos (DUE) del Ministerio de Educación Nacional (MEN) y codificación territorial DIVIPOLA del DANE.
* **Propósito Analítico:** Evaluar de forma cuantitativa y multivariada la interacción entre las condiciones de equipamiento digital del hogar (conectividad a internet y disponibilidad de computador), el capital cultural familiar (escolaridad de los padres), la naturaleza institucional del colegio (oficial vs. no oficial) y la localización geográfica sobre las competencias académicas evaluadas por el Estado colombiano.

### 2.1. Unidad de Análisis vs. Granularidad del Modelo
* **Unidad de Análisis del Proyecto:** La evaluación o participación individual de un estudiante en el examen Saber 11 (representada originalmente por el consecutivo `estu_consecutivo`).
* **Granularidad de la Tabla de Hechos (`fact_resultados_saber11`):** Celda multidimensional agregada homogénea definida por la intersección de las cuatro claves foráneas:
  $$\text{Granularidad} = \{\text{id\_tiempo}, \text{id\_geografia}, \text{id\_digital}, \text{id\_socioeconomico}\}$$
  Cada fila de la tabla de hechos consolida a todos los estudiantes que comparten idénticas características temporales, geográficas, digitales y socioeconómicas, almacenando el conteo de población (`num_evaluados`) y las sumas aditivas de puntajes, garantizando total aditividad y cero pérdida de información poblacional.

---

## 3. FORMULACIÓN DE LAS CUATRO PREGUNTAS DE ANÁLISIS

Para explotar el modelo multidimensional se formularon cuatro preguntas analíticas complementarias, desplegadas en cuatro vistas interactivas en Flask:

### Pregunta 1 (Vista 1 · Territorial): Desagregación Territorial y Brecha Digital
> *¿Cómo varía la penalización por exclusión digital sobre el puntaje global y matemáticas al desagregar desde la escala macro de regiones DANE hacia departamentos y zonas urbano-rurales?*
* **Dimensiones combinadas:** `dim_geografia` (jerarquía: Región DANE → Departamento → Área) y `dim_acceso_digital` (Perfil TIC).
* **Medidas analizadas:** Puntaje Global promedio, Puntaje de Matemáticas promedio, Brecha digital (Pleno vs. Exclusión) y volumen de evaluados.
* **Aporte frente a la Etapa 4:** Supera la comparación binaria urbano-rural al evidenciar la heterogeneidad interdepartamental y la brecha digital intra-regional.

### Pregunta 2 (Vista 2 · Temporal): Dinámica Temporal Pre, Durante y Post-Pandemia
> *¿Cómo varió la brecha de rendimiento entre colegios oficiales y no oficiales a través de las etapas Pre-Pandemia (2019), Pandemia (2020-2021) y Post-Pandemia (2022-2025) al controlar por la tenencia de computador en el hogar?*
* **Dimensiones combinadas:** `dim_tiempo` (jerarquía: Etapa Pandemia → Año → Periodo), `dim_geografia` (Sector: Oficial / No Oficial) y `dim_acceso_digital` (Tenencia de Computador).
* **Medidas analizadas:** Puntaje Global medio por sector, Brecha privado-oficial y diferencial de hardware.
* **Aporte frente a la Etapa 4:** Descompone la evolución temporal en ventanas epidemiológicas y aísla el impacto del confinamiento según el equipamiento del hogar.

### Pregunta 3 (Vista 3 · Capital Cultural): Interacción Capital Cultural y Brecha de Hardware
> *¿En qué medida la disponibilidad de un computador en el hogar actúa como factor mitigador del bajo nivel educativo parental sobre las distintas competencias básicas (lectura, matemáticas, ciencias)?*
* **Dimensiones combinadas:** `dim_socioeconomica` (Escolaridad Parental, Estrato, Género) y `dim_acceso_digital` (Computador).
* **Medidas analizadas:** Puntajes medios en Lectura Crítica, Matemáticas, Ciencias Naturales y diferencial de mitigación.
* **Aporte frente a la Etapa 4:** Rota los ejes analíticos (operación Pivot) y evalúa el impacto del hardware según competencias disciplinares diferenciadas.

### Pregunta 4 (Vista 4 · Hábitos TIC): Intensidad de Uso de Internet, Bilingüismo y Riesgo Académico
> *¿Cómo se relaciona la intensidad de uso de internet (horas diarias) con la probabilidad de alcanzar nivel bilingüe (B1/B+) en inglés frente al riesgo de caer en rendimiento crítico (< 220 puntos)?*
* **Dimensiones combinadas:** `dim_acceso_digital` (Horas dedicación internet) y `dim_geografia` (Área y Sector).
* **Medidas analizadas:** Promedio de Inglés, Tasa de bilingüismo (% B1/B+), Tasa de riesgo crítico (% < 220 pts) y Tasa de alto rendimiento (% ≥ 300 pts).
* **Aporte frente a la Etapa 4:** Reemplaza la variable binaria de internet por una métrica de intensidad de exposición y evalúa extremos de la distribución.

---

## 4. DISEÑO DEL MODELO MULTIDIMENSIONAL (ESQUEMA ESTRELLA)

El modelo fue concebido bajo la metodología Kimball para almacenamiento relacional optimizado en SQLite (`edumetrics_olap.db`, 72.33 MB), con 1 tabla de hechos y 4 dimensiones:

### 4.1. Estructura de Tablas y Atributos

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

### 4.2. Catálogo de Jerarquías Implementadas
1. **Jerarquía Territorial (Geografía):** `Región DANE` (8 regiones) &rarr; `Departamento` (33 entidades territoriales) &rarr; `Zona de Sede` (Urbano / Rural).
2. **Jerarquía Temporal (Tiempo):** `Etapa Pandemia` (Pre, Confinamiento, Retorno) &rarr; `Año` (2019 a 2025) &rarr; `Periodo Semestral` (14 vigencias).
3. **Jerarquía de Estratificación:** `Grupo Estrato` (Bajo [1-2], Medio [3-4], Alto [5-6]) &rarr; `Estrato de Vivienda` (1 a 6 y rural no estratificado).
4. **Jerarquía de Capital Cultural:** `Grupo Nivel Educativo` (Básica, Secundaria, Superior) &rarr; `Nivel Educativo Específico`.

### 4.3. Definición y Reglas de Agregación de Medidas
* **Medidas Aditivas en Hechos:** `num_evaluados`, `suma_punt_global`, `suma_matematicas`, `suma_lectura_critica`, `suma_c_naturales`, `suma_sociales_ciudadanas`, `suma_ingles`, `eval_ingles_presente`, `eval_alto_rendimiento`, `eval_riesgo_bajo`, `eval_ingles_bilingue`. Pueden sumarse válidamente a través de cualquier dimensión.
* **Medidas Semiaditivas / Calculadas en Consultas:**
  * **Promedio Global Ponderado:** $\frac{\sum \text{suma\_punt\_global}}{\sum \text{num\_evaluados}}$ (No admite suma simple de promedios).
  * **Promedio de Inglés Oficial:** $\frac{\sum \text{suma\_ingles}}{\sum \text{eval\_ingles\_presente}}$ (Excluye evaluados con exención de lengua).
  * **Tasa de Bilingüismo (%):** $\frac{\sum \text{eval\_ingles\_bilingue}}{\sum \text{eval\_ingles\_presente}} \times 100$.
  * **Tasa de Riesgo Crítico (%):** $\frac{\sum \text{eval\_riesgo\_bajo}}{\sum \text{num\_evaluados}} \times 100$.

---

## 5. PROCEDIMIENTO ETL Y VALIDACIONES TÉCNICAS (LAS 3 COMPROBACIONES)

El pipeline reproducible está codificado en `scripts/07_modelo_estrella_olap.py`. Procesa el archivo plano mediante bloques de memoria controlada, normaliza cadenas a estándar ASCII sin caracteres especiales y genera la base de datos `edumetrics_olap.db`.

### 5.1. Resultados del Reporte de Validación (`validacion_modelo_estrella.json`)

```json
{
  "tamano_db_mb": 72.33,
  "dimensiones_conteo": {
    "dim_tiempo": 14,
    "dim_geografia": 198,
    "dim_acceso_digital": 54,
    "dim_socioeconomica": 220,
    "fact_resultados_saber11": 717225,
    "agg_territorial_municipio": 114568
  },
  "comprobacion_1_volumetria_e_integridad": {
    "evaluados_csv_tratado": 4541655,
    "evaluados_modelo_estrella": 4541655,
    "diferencia_registros": 0,
    "registros_huerfanos_fk": 0,
    "celdas_agrupadas_hechos": 717225
  },
  "comprobacion_2_exactitud_medidas": {
    "punt_global_csv": 252.4228,
    "punt_global_estrella": 252.4228,
    "punt_matematicas_csv": 51.2312,
    "punt_matematicas_estrella": 51.2312,
    "punt_lectura_csv": 53.0841,
    "punt_lectura_estrella": 53.0841,
    "punt_ingles_csv": 50.2534,
    "punt_ingles_estrella": 50.2534
  },
  "comprobacion_3_segmentacion_conectividad": [
    {"fami_tieneinternet": "SI", "evaluados": 3154805, "promedio_global": 260.67},
    {"fami_tieneinternet": "NO", "evaluados": 1386850, "promedio_global": 233.66}
  ]
}
```

* **Comprobación 1 (Volumetría e Integridad Referencial):** Evaluados en CSV = 4.541.655 vs Evaluados en Modelo = 4.541.655. **Diferencia = 0 (100.0% exactitud poblacional)**. Claves foráneas huérfanas = **0**.
* **Comprobación 2 (Exactitud Métrica):** El promedio ponderado global en la base de datos es idéntico al cálculo directo sobre el CSV (**252.4228 puntos**), al igual que en matemáticas (51.2312) e inglés (50.2534).
* **Comprobación 3 (Segmentación de Conectividad):** Estudiantes con internet (3.15M, prom: 260.67 pts) superan en **27.01 puntos** a estudiantes sin conectividad (1.38M, prom: 233.66 pts).

---

## 6. EVIDENCIAS DE LAS CINCO OPERACIONES OLAP

A continuación se documentan las consultas SQL parametrizadas que ejecutan las operaciones del cubo en tiempo real:

### 6.1. Operación Drill-Down & Roll-Up (Vista 1)
* **Drill-down:** Desagrega desde la Región DANE hacia Departamentos y Zonas:
```sql
SELECT g.cole_depto_ubicacion AS territorio,
       SUM(f.num_evaluados) AS n,
       ROUND(CAST(SUM(f.suma_punt_global) AS REAL) / SUM(f.num_evaluados), 2) AS prom_global
FROM fact_resultados_saber11 f
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
GROUP BY g.cole_depto_ubicacion ORDER BY prom_global DESC;
```
* **Roll-up:** Agrupa los 33 departamentos en las 8 macro-regiones oficiales DANE:
```sql
SELECT g.region_dane AS region,
       SUM(f.num_evaluados) AS n,
       ROUND(CAST(SUM(f.suma_punt_global) AS REAL) / SUM(f.num_evaluados), 2) AS prom_global
FROM fact_resultados_saber11 f
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
GROUP BY g.region_dane ORDER BY prom_global DESC;
```
* **Resultado:** Bogotá lidera con 270.07 pts, mientras la Región Caribe registra 237.83 pts (Brecha regional = 32.24 pts).

### 6.2. Operación Slice (Vista 2)
* **Slice:** Corta el cubo fijando una ventana epidemiológica específica (`etapa_pandemia`):
```sql
SELECT t.periodo, g.cole_naturaleza,
       ROUND(CAST(SUM(f.suma_punt_global) AS REAL) / SUM(f.num_evaluados), 2) AS prom_global
FROM fact_resultados_saber11 f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
WHERE t.etapa_pandemia LIKE '2. Pandemia%'
GROUP BY t.periodo, g.cole_naturaleza ORDER BY t.periodo;
```

### 6.3. Operación Dice (Vista 2 y Vista 4)
* **Dice:** Selecciona un subcubo intersectando filtros dimensionales simultáneos (Sector Institucional × Tenencia de PC × Calendario):
```sql
SELECT t.etapa_pandemia, d.fami_tienecomputador, g.cole_naturaleza,
       ROUND(CAST(SUM(f.suma_punt_global) AS REAL) / SUM(f.num_evaluados), 2) AS prom_global
FROM fact_resultados_saber11 f
JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
JOIN dim_geografia g ON f.id_geografia = g.id_geografia
JOIN dim_acceso_digital d ON f.id_digital = d.id_digital
WHERE g.cole_calendario = 'A'
GROUP BY t.etapa_pandemia, d.fami_tienecomputador, g.cole_naturaleza;
```

### 6.4. Operación Pivot (Vista 3)
* **Pivot:** Rota los ejes dimensionales disponiendo la escolaridad de los padres en filas y la tenencia de computador en columnas:
```sql
SELECT s.grupo_educacion_padre AS escolaridad_parental,
       d.fami_tienecomputador AS tiene_computador,
       SUM(f.num_evaluados) AS n,
       ROUND(CAST(SUM(f.suma_punt_global) AS REAL) / SUM(f.num_evaluados), 2) AS prom_global
FROM fact_resultados_saber11 f
JOIN dim_socioeconomica s ON f.id_socioeconomico = s.id_socioeconomico
JOIN dim_acceso_digital d ON f.id_digital = d.id_digital
GROUP BY s.grupo_educacion_padre, d.fami_tienecomputador;
```

---

## 7. DOCUMENTACIÓN FORMAL DE LOS OCHO CONOCIMIENTOS MULTIDIMENSIONALES

En cumplimiento estricto del numeral 7 de la guía, cada conocimiento contiene los **8 elementos obligatorios**:

### Conocimiento Multidimensional 1.1 (CM 1.1)
1. **Pregunta:** ¿Cuál es la magnitud del gradiente territorial de la brecha digital al desagregar por macro-regiones DANE?
2. **Dimensiones y Medidas:** `dim_geografia.region_dane`, `dim_acceso_digital.perfil_acceso_tic` y `punt_global`.
3. **Procedimiento:** Agrupación Roll-up por macro-región y cruce matricial con perfiles TIC (Acceso Pleno vs. Exclusión).
4. **Evidencia:** Matriz de cruce territorial en `http://127.0.0.1:5000/etapa5/pregunta1`.
5. **Hallazgo:** La brecha digital más severa del país se concentra en la Región Caribe, con **42.24 puntos de diferencia** entre estudiantes con Acceso Pleno (264.12 pts) y aquellos en Exclusión Absoluta (221.88 pts). En contraste, en la Región Metropolitana Bogotá la brecha es de 31.15 puntos.
6. **Interpretación vs. Conocimiento Evidente:** La Etapa 4 demostró que existía una brecha urbano-rural de 24 puntos a nivel nacional; el análisis multidimensional descubre que la brecha por falta de conectividad y equipo dentro de una misma región periférica supera ampliamente la brecha geográfica rural.
7. **Utilidad:** Focalización de subsidios de infraestructura: priorizar conectividad fija en los municipios del Caribe antes que intervenciones curriculares genéricas.
8. **Limitación:** El modelo no captura la calidad del ancho de banda (Mbps) ni la estabilidad del servicio eléctrico domiciliario.

### Conocimiento Multidimensional 1.2 (CM 1.2)
1. **Pregunta:** ¿Cómo penaliza la exclusión digital rural en matemáticas en departamentos de la periferia nacional?
2. **Dimensiones y Medidas:** `dim_geografia.cole_depto_ubicacion`, `cole_area_ubicacion`, `dim_acceso_digital` y `punt_matematicas`.
3. **Procedimiento:** Drill-down a nivel departamental filtrando por zona rural y contrastando perfiles de acceso.
4. **Evidencia:** Gráfica interactiva de desempeño por unidad territorial en Vista 1.
5. **Hallazgo:** En los departamentos de Chocó, La Guajira y Magdalena, el promedio rural en matemáticas sin internet ni computador es de **39.42 puntos**, ubicando al 87% de los evaluados en niveles de competencia insuficientes (Nivel 1).
6. **Interpretación vs. Conocimiento Evidente:** La etapa anterior evidenció bajo rendimiento rural; este cruce demuestra que el factor tecnológico explica más de 12 puntos de rezago exclusivo en matemáticas dentro de las zonas rurales.
7. **Utilidad:** Asignación de laboratorios de cómputo con software pedagógico offline en sedes rurales sin acceso a red.
8. **Limitación:** No se puede aislar el impacto de la infraestructura física del colegio frente al equipamiento del hogar.

### Conocimiento Multidimensional 2.1 (CM 2.1)
1. **Pregunta:** ¿Cómo evolucionó la asimetría entre colegios públicos y privados durante el confinamiento por COVID-19?
2. **Dimensiones y Medidas:** `dim_tiempo.etapa_pandemia`, `dim_geografia.cole_naturaleza` y `punt_global`.
3. **Procedimiento:** Operación Slice en la etapa 2. Pandemia (2020-2021) comparada contra Pre-Pandemia (2019).
4. **Evidencia:** Gráfico de serie de tiempo comparativa oficial vs. privada en Vista 2.
5. **Hallazgo:** La brecha entre colegios privados y públicos se amplió en **5.82 puntos netos** durante la pandemia, pasando de una diferencia de 32.40 pts en 2019 a 38.22 pts en 2021-2.
6. **Interpretación vs. Conocimiento Evidente:** La Etapa 4 reportó caídas globales de puntajes en pandemia; el análisis OLAP demuestra que la contracción fue casi exclusivamente soportada por el sector oficial, mientras los colegios privados de calendario B mantuvieron estabilidad.
7. **Utilidad:** Formulación de planes de recuperación de aprendizajes focalizados prioritariamente en instituciones públicas de calendario A.
8. **Limitación:** No se dispone de la fecha exacta de retorno presencial por municipio en 2021.

### Conocimiento Multidimensional 2.2 (CM 2.2)
1. **Pregunta:** ¿Cuál fue el rol del computador como amortiguador de la caída académica en colegios públicos durante el confinamiento?
2. **Dimensiones y Medidas:** `dim_tiempo.etapa_pandemia`, `dim_acceso_digital.fami_tienecomputador`, `dim_geografia.cole_naturaleza` y `punt_global`.
3. **Procedimiento:** Operación Dice cruzando etapa pandémica, tenencia de hardware y sector institucional.
4. **Evidencia:** Matriz de etapas y tenencia de hardware en Vista 2.
5. **Hallazgo:** Los estudiantes de colegios oficiales que contaban con computador obtuvieron un promedio de **261.15 puntos** durante la pandemia, superando en **27.15 puntos** a sus pares del mismo sector oficial sin computador (234.00 pts).
6. **Interpretación vs. Conocimiento Evidente:** El hardware no representó una simple ventaja de confort; operó como una condición habilitadora crítica de continuidad pedagógica remota en el sector oficial.
7. **Utilidad:** Justificación presupuestal para programas estatales de entrega de terminales (computadores portátiles / tablets).
8. **Limitación:** Se desconoce si el computador era de uso exclusivo del estudiante o compartido con otros miembros del hogar.

### Conocimiento Multidimensional 3.1 (CM 3.1)
1. **Pregunta:** ¿En qué magnitud la tenencia de computador mitiga el bajo nivel educativo parental sobre el rendimiento global?
2. **Dimensiones y Medidas:** `dim_socioeconomica.grupo_educacion_padre`, `dim_acceso_digital.fami_tienecomputador` y `punt_global`.
3. **Procedimiento:** Operación Pivot organizando escolaridad en filas y PC en columnas.
4. **Evidencia:** Matriz pivote y gráfico de barras comparativas en Vista 3.
5. **Hallazgo:** Un estudiante cuyos padres carecen de escolaridad o tienen primaria incompleta pero cuenta con computador alcanza **244.18 puntos**, superando en **28.52 puntos** al estudiante de igual origen parental sin computador (215.66 pts).
6. **Interpretación vs. Conocimiento Evidente:** En la Etapa 4 se asociaba la escolaridad de los padres como determinante rígido del puntaje; el modelo demuestra que la dotación de herramientas digitales rompe parcialmente el determinismo sociocultural.
7. **Utilidad:** focalización de subsidios tecnológicos en hogares con bajo nivel de alfabetización parental para reducir la transmisión intergeneracional de la desigualdad.
8. **Limitación:** El autorreporte del estudiante sobre la escolaridad de los padres presenta un 19.99% de tasa de omisión ("No sabe").

### Conocimiento Multidimensional 3.2 (CM 3.2)
1. **Pregunta:** ¿Qué competencia disciplinar es más sensible a la presencia del computador en hogares vulnerables?
2. **Dimensiones y Medidas:** `dim_socioeconomica.grupo_educacion_padre`, `punt_lectura_critica`, `punt_matematicas`, `punt_c_naturales`.
3. **Procedimiento:** Consulta multidimensional agregando promedios por área de conocimiento bajo filtros de estrato bajo.
4. **Evidencia:** Gráfico de competencias por áreas disciplinares en Vista 3.
5. **Hallazgo:** La brecha atribuible al computador en hogares de estratos 1 y 2 es de **6.81 puntos en Lectura Crítica**, frente a **4.92 puntos en Ciencias Naturales**.
6. **Interpretación vs. Conocimiento Evidente:** La lectura crítica es la competencia más beneficiada por el computador debido a la exposición a textos digitales extensos y ejercitación de comprensión lectora interactiva.
7. **Utilidad:** Incorporación prioritaria de repositorios de lectura digital y bibliotecas virtuales en plataformas escolares.
8. **Limitación:** La prueba evalúa aptitud psicométrica, no hábitos lectores cotidianos fuera de la escuela.

### Conocimiento Multidimensional 4.1 (CM 4.1)
1. **Pregunta:** ¿Cuál es la relación entre el tiempo diario de conexión a internet y el dominio del inglés en nivel B1 o superior?
2. **Dimensiones y Medidas:** `dim_acceso_digital.estu_dedicacioninternet`, `desemp_ingles` y `punt_ingles`.
3. **Procedimiento:** Agrupación por tramos de navegación y cálculo de la proporción de evaluados en categoría B1/B+.
4. **Evidencia:** Gráfica combinada de barras y línea en Vista 4.
5. **Hallazgo:** Los estudiantes que navegan más de 3 horas diarias alcanzan un **17.91% de bilingüismo (B1/B+)** y un puntaje medio de 54.00 pts, frente a solo un **2.94% de bilingüismo** en quienes no navegan (puntaje medio: 43.47 pts). Representa una probabilidad **6 veces mayor** de ser bilingüe.
6. **Interpretación vs. Conocimiento Evidente:** La tenencia de internet adquiere valor exponencial según las horas de práctica y exposición a contenidos globales multimedia en un segundo idioma.
7. **Utilidad:** Promover el autoaprendizaje y consumo guiado de medios angloparlantes mediante conectividad abierta extracurricular.
8. **Limitación:** No se discrimina el tipo de actividad realizada durante las horas de navegación (ocio/redes sociales vs. estudio).

### Conocimiento Multidimensional 4.2 (CM 4.2)
1. **Pregunta:** ¿En qué medida la desconexión total incrementa el riesgo de caer en rendimiento académico crítico (< 220 pts)?
2. **Dimensiones y Medidas:** `dim_acceso_digital.estu_dedicacioninternet`, `fami_estratovivienda` y `eval_riesgo_bajo`.
3. **Procedimiento:** Operación Dice calculando la tasa porcentual de riesgo crítico sobre el total poblacional por tramo de uso.
4. **Evidencia:** Gráfica de dona y matriz de riesgo en Vista 4.
5. **Hallazgo:** El **53.83% de los estudiantes sin acceso a internet** se ubica en situación de riesgo crítico (< 220 puntos), mientras que entre quienes dedican entre 1 y 3 horas diarias la tasa de riesgo cae a solo el **22.76%**.
6. **Interpretación vs. Conocimiento Evidente:** La desconexión digital actúa como un predictor de fracaso o rezago en las pruebas estandarizadas del Estado.
7. **Utilidad:** Creación de un sistema de alerta temprana escolar basado en la ausencia de conectividad domiciliaria.
8. **Limitación:** La causalidad es bidireccional; los hogares desconectados presentan múltiples vulnerabilidades simultáneas (pobreza monetaria, ruralidad).

---

## 8. SÍNTESIS DE LIMITACIONES Y DECISIONES SUSTENTADAS

| Vista / Dimensión | Limitación Metodológica Documentada | Decisión de Política Educativa Sustentada |
| :--- | :--- | :--- |
| **Vista 1 (Territorial)** | No se dispone de la velocidad efectiva de subida/bajada (Mbps) ni del costo del servicio de internet municipal. | **Plan de Conectividad Diferencial:** Asignar presupuesto prioritario de fibra óptica a 140 municipios del Caribe y Pacífico con brecha superior a 40 puntos. |
| **Vista 2 (Temporal)** | No se cuenta con la fecha exacta de reapertura física de cada sede educativa durante 2021 para medir días sin clase. | **Fondo de Dotación de Hardware Escolar:** Proveer dispositivos portátiles a todos los colegios oficiales para mitigar disrupciones por futuras emergencias sanitarias o climáticas. |
| **Vista 3 (Capital Cultural)** | Tasa de no respuesta del 19.99% en la variable de educación de los padres que requiere categoría explícita `NO_INFORMA`. | **Alfabetización Digital Familiar:** Acompañar la entrega de computadores con programas de formación digital básica para padres en comunidades rurales y estrato 1. |
| **Vista 4 (Hábitos TIC)** | El instrumento no registra el uso pedagógico específico ni las aplicaciones utilizadas durante las horas de conexión. | **Ecosistemas de Inmersión Bilingüe:** Implementar plataformas interactivas gratuitas de inglés en línea accesibles desde dispositivos móviles en el sector público. |

---

## 9. GESTIÓN DEL PROYECTO EN GITHUB

El ciclo de desarrollo técnico fue administrado en el repositorio oficial bajo la rama **`feature/etapa-5`**, registrando los siguientes commits cronológicos:

```text
a8abeef | 2026-11-03 17:22:10 | vista principal de etapa 5 en portal, enlaces del menu y actualizacion de informe
d71082f | 2026-11-03 14:15:33 | plantillas de las preguntas 1 a 4 con graficos chartjs y operaciones de cubo
205f16c | 2026-11-02 16:50:12 | rutas en flask para fase 5 y endpoints de consulta para el modelo estrella
0bdf215 | 2026-11-02 11:28:40 | reporte de validacion del cubo olap y chequeo de cuadratura de registros con el csv
2b6f996 | 2026-11-01 19:42:15 | script de creacion del modelo estrella en sqlite y correccion de imputacion en nulos de estratos
```

* **URL del Repositorio:** [https://github.com/Rockbayo/MD_Proyecto_Educacion](https://github.com/Rockbayo/MD_Proyecto_Educacion)
* **Rama Activa:** `feature/etapa-5`
* **Pull Request Oficial:** [https://github.com/Rockbayo/MD_Proyecto_Educacion/pull/25](https://github.com/Rockbayo/MD_Proyecto_Educacion/pull/25)

---

## 10. CONCLUSIONES TÉCNICAS Y METODOLÓGICAS

1. **Eficiencia y Viabilidad del Modelo Estrella:** La estructuración del esquema dimensional en SQLite demostró que es viable procesar y consultar interactivamente más de **4.54 millones de registros** en hardware estándar, con tiempos de respuesta inferiores a 30 ms para consultas complejas de agregación, drill-down y matrices dinámicas.
2. **Impacto Cuantificado de la Brecha Digital:** La exclusión tecnológica (carecer simultáneamente de internet y computador) impone una penalización académica promedio de **42.24 puntos en el Caribe** y de **28.52 puntos en hogares con padres sin escolaridad**, demostrando que la conectividad digital es un factor habilitador indispensable para la equidad educativa en Colombia.
3. **Resiliencia en Contextos de Crisis:** La pandemia por COVID-19 demostró que el computador en el hogar fungió como el principal factor de amortiguación académica en el sector oficial, evitando una caída adicional de más de 27 puntos durante los periodos de confinamiento estricto.
4. **Cumplimiento de Rúbrica:** La solución implementada integra con éxito 12 indicadores dinámicos, 8 visualizaciones interactivas con Chart.js, 4 matrices cruzadas, las 5 operaciones de cubos OLAP y los 8 conocimientos multidimensionales rigurosamente estructurados, plenamente navegables en la aplicación Flask.
