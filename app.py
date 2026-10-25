from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/etapa1/problema')
def problema():
    return render_template('etapa1/problema.html')

@app.route('/etapa1/preguntas')
def preguntas():
    return render_template('etapa1/preguntas.html')

@app.route('/etapa1/necesidades')
def necesidades():
    return render_template('etapa1/necesidades.html')

@app.route('/etapa1/fuentes')
def fuentes():
    return render_template('etapa1/fuentes.html')

@app.route('/etapa1/dataset')
def dataset():
    return render_template('etapa1/dataset.html')

@app.route('/etapa1/diccionario')
def diccionario():
    return render_template('etapa1/diccionario.html')

@app.route('/etapa1/calidad')
def calidad():
    return render_template('etapa1/calidad.html')

@app.route('/etapa1/limitaciones')
def limitaciones():
    return render_template('etapa1/limitaciones.html')

# ==========================================
# RUTAS ETAPA 2: DIAGNÓSTICO Y CALIDAD
# ==========================================
@app.route('/etapa2/proposito')
def proposito():
    return render_template('etapa2/proposito.html')

@app.route('/etapa2/perfilamiento')
def perfilamiento():
    return render_template('etapa2/perfilamiento.html')

@app.route('/etapa2/dimensiones')
def dimensiones():
    return render_template('etapa2/dimensiones.html')

@app.route('/etapa2/integracion')
def integracion():
    return render_template('etapa2/integracion.html')

@app.route('/etapa2/informe')
def informe():
    return render_template('etapa2/informe.html')

# ==========================================
# RUTAS ETAPA 3: ETL Y TRANSFORMACIÓN (SSIS)
# ==========================================
@app.route('/etapa3/arquitectura')
def arquitectura():
    return render_template('etapa3/arquitectura.html')

@app.route('/etapa3/iteraciones')
def iteraciones():
    return render_template('etapa3/iteraciones.html')

@app.route('/etapa3/publicacion')
def publicacion():
    return render_template('etapa3/publicacion.html')

# ==========================================
# RUTAS ETAPA 4: CONOCIMIENTO EVIDENTE
# ==========================================
@app.route('/etapa4')
def etapa4_index():
    return render_template('etapa4/index.html')

@app.route('/etapa4/preguntas')
def preguntas_etapa4():
    return render_template('etapa4/preguntas.html')

@app.route('/etapa4/conocimientos')
def conocimientos():
    return render_template('etapa4/conocimientos.html')

@app.route('/etapa4/dashboard')
def dashboard():
    return render_template('etapa4/dashboard.html')

@app.route('/api/v1/etapa4/resumen')
def api_etapa4_resumen():
    """Endpoint JSON con estadísticas globales del dataset curado post-ETL."""
    resumen = {
        "dataset": "Saber 11 ICFES — EduMetrics Colombia",
        "fuente": "ICFES (Instituto Colombiano para la Evaluación de la Educación)",
        "url_fuente": "https://www.icfes.gov.co/data-icfes",
        "periodo_cobertura": "2019-1 a 2025-2",
        "registros_post_etl": 761173,
        "registros_muestra_5pct": 227084,
        "variables_totales": 93,
        "tratamiento_etl": {
            "herramienta": "SQL Server Integration Services (SSIS)",
            "pasos": [
                "Truncate de tablas en Staging",
                "Limpieza de caracteres Unicode",
                "Conversión de tipos de datos",
                "Cruce con dimensión DUE",
                "Auditoría de duplicados (0 encontrados)"
            ]
        },
        "preguntas_analisis": [
            {"id": "P1", "titulo": "Composición y Distribución",
             "pregunta": "¿Cómo se distribuyen los estudiantes según NSE, género y departamento?"},
            {"id": "P2", "titulo": "Comparación Territorial",
             "pregunta": "¿Existen diferencias de desempeño entre departamentos y zonas urbano-rural?"},
            {"id": "P3", "titulo": "Comportamiento Temporal",
             "pregunta": "¿Cómo evolucionó el desempeño en matemáticas y lectura crítica 2019-2025?"},
            {"id": "P4", "titulo": "Análisis Multivariado",
             "pregunta": "¿Qué combinación de NSE, tipo de colegio e internet predice el mayor puntaje?"}
        ],
        "conocimientos_evidentes": 12,
        "tableros_power_bi": 4
    }
    return jsonify(resumen)

if __name__ == '__main__':
    app.run(debug=True)
