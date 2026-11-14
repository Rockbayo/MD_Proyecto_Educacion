# Flujos de Trabajo en Orange Data Mining (Etapa 6)

Este directorio contiene los tres flujos de trabajo oficiales desarrollados para la **Etapa 6: Minería de Datos Avanzada, Aprendizaje Automático y Minería de Texto**:

---

## 1. `01_modelos_supervisados.ows` — Modelos Supervisados de Clasificación
- **Pregunta de predicción:** ¿En qué medida las variables de acceso a tecnología y las condiciones socioeconómicas del hogar permiten predecir el riesgo de bajo rendimiento académico (puntaje global < 220 puntos) en las pruebas Saber 11?
- **Dataset fuente:** `data/processed/saber11_orange_100k.tab` (o `.csv`).
- **Variable objetivo (Target):** `riesgo_critico` (`SI` / `NO`).
- **Modelos evaluados:**
  1. **Random Forest:** 100 árboles de decisión, profundidad máxima 12.
  2. **Regresión Logística:** Regularización L2 con balanceo de pesos para maximizar Recall.
  3. **Red Neuronal (MLP):** Perceptrón multicapa con 2 capas ocultas (64, 32 neuronas).
- **Validación:** 10-Fold Cross-Validation en el widget *Test & Score*.
- **Evaluación:** Widgets *Confusion Matrix* y *ROC Analysis*.

---

## 2. `02_clustering_kmeans.ows` — Aprendizaje No Supervisado (k-Means)
- **Pregunta de agrupamiento:** ¿Qué tipologías o perfiles de estudiantes se identifican a partir de sus niveles de conectividad digital y características socioeconómicas, sin considerar los resultados académicos?
- **Dataset fuente:** `data/processed/saber11_orange_100k.tab` (o `.csv`).
- **Tratamiento:** Selección de variables exclusivamente de entorno y brecha digital (sin puntajes ni target). Estandarización en el widget *Preprocess* (Media=0, Varianza=1).
- **Selección de k:** Evaluación de silueta comparando $k=3, 4, 5$. El valor óptimo seleccionado es **$k=3$ (Silhouette = 0.2690)**.
- **Widgets de salida:** *Silhouette Plot*, *Scatter Plot* y *Box Plot* para caracterizar los 3 grupos descubiertos:
  - *Clúster 0:* Privado Urbano con Ecosistema Digital Pleno (18.6%).
  - *Clúster 1:* Vulnerabilidad Alta y Desconexión Tecnológica Crítica (42.1%).
  - *Clúster 2:* Oficial Urbano en Transición (39.3%).

---

## 3. `03_text_mining_youtube.ows` — Extracción y Minería de Texto
- **Pregunta de análisis:** ¿Cuáles son las principales temáticas y percepciones expresadas por la comunidad en plataformas digitales respecto a la preparación y los recursos tecnológicos disponibles para las pruebas Saber 11 en Colombia?
- **Dataset fuente:** `data/processed/comentarios_youtube_limpios.csv`.
- **Procesamiento de texto:** Tokenización, minúsculas, filtrado de stopwords en español.
- **Widgets aplicados:**
  - *Corpus:* Carga estructurada de comentarios con likes y metadatos.
  - *Sentiment Analysis:* Polaridad emocional (44% crítico/negativo, 32% neutral, 24% positivo).
  - *Word Cloud:* Términos preponderantes (*internet*, *computador*, *colegio privado*, *rural*, *brecha*, *simulacros*).
  - *Topic Modeling / Hierarchical Clustering:* Agrupación de opiniones en 4 núcleos temáticos.

---

### Instrucciones de Ejecución en Orange GUI
1. Abrir **Orange Data Mining**.
2. Ir a `File -> Open` y seleccionar cualquiera de los archivos `.ows`.
3. Si Orange solicita reubicar el archivo de datos, seleccionar el archivo correspondiente en la carpeta `data/processed/`.
