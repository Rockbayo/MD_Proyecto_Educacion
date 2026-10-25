# app.py
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# -------------------------------------------------------------
# RUTAS PRINCIPALES DEL PORTAL (EXISTENTES)
# -------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/problema')
def problema():
    return render_template('problema.html')

@app.route('/proposito')
def proposito():
    return render_template('proposito.html')

@app.route('/fuentes')
def fuentes():
    return render_template('fuentes.html')

@app.route('/diccionario')
def diccionario():
    return render_template('diccionario.html')

@app.route('/perfilamiento')
def perfilamiento():
    return render_template('perfilamiento.html')

@app.route('/integracion')
def integracion():
    return render_template('integracion.html')

@app.route('/calidad')
def calidad():
    return render_template('calidad.html')

@app.route('/informe')
def informe():
    return render_template('informe.html')

@app.route('/arquitectura')
def arquitectura():
    return render_template('arquitectura.html')

@app.route('/flujos')
def flujos():
    return render_template('flujos.html')

@app.route('/iteraciones')
def iteraciones():
    return render_template('iteraciones.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

@app.route('/informe_etapa3')
def informe_etapa3():
    return render_template('informe_etapa3.html')


# -------------------------------------------------------------
# RUTAS DE ETAPA 4: CONOCIMIENTO EVIDENTE (POWER BI)
# -------------------------------------------------------------

@app.route('/etapa4')
def etapa4_index():
    """Vista principal de la Etapa 4: Conocimiento Evidente."""
    return render_template('etapa4/index.html')

@app.route('/etapa4/preguntas')
def preguntas_etapa4():
    """Vista de las 4 preguntas de análisis con indicadores y visualizaciones."""
    return render_template('etapa4/preguntas.html')

@app.route('/etapa4/conocimientos')
def conocimientos():
    """Vista de los 12 conocimientos evidentes documentados con sus 8 elementos."""
    return render_template('etapa4/conocimientos.html')

@app.route('/etapa4/dashboard')
def dashboard():
    """Vista del tablero interactivo Power BI embebido y visor del informe técnico."""
    return render_template('etapa4/dashboard.html')

@app.route('/api/v1/etapa4/resumen')
def api_etapa4_resumen():
    """Endpoint JSON con estadísticas globales del dataset curado y tableros Power BI."""
    resumen = {
        "dataset": "Saber 11 ICFES — EduMetrics Colombia",
        "fuente": "ICFES (Instituto Colombiano para la Evaluación de la Educación)",
        "url_fuente": "https://www.icfes.gov.co/data-icfes",
        "periodo_cobertura": "2019-1 a 2025-2",
        "total_evaluados_modelo": 4000000,
        "variables_analizadas": [
            "fami_tieneinternet", "fami_estratovivienda", "fami_tienecomputador",
            "fami_educacionpadre", "cole_naturaleza", "cole_area_ubicacion",
            "cole_depto_ubicacion", "cole_mcpio_ubicacion", "periodo", "punt_global"
        ],
        "unidad_analisis": "Evaluación o participación individual de un estudiante en la prueba Saber 11",
        "preguntas_analisis": [
            {
                "id": "T1",
                "titulo": "Composición y Brecha Digital",
                "pregunta": "¿Qué proporción de estudiantes cuenta con internet y cómo interactúa con el estrato y el computador?",
                "indicadores_dax": ["Total_Evaluados (4M)", "%_Con_Internet (67%)", "%_Con_PC (53%)"],
                "filtros": ["periodo", "cole_naturaleza"]
            },
            {
                "id": "T2",
                "titulo": "Comparación Territorial",
                "pregunta": "¿Existe una diferencia empírica en el desempeño global entre colegios urbanos y rurales y qué relación guarda la cobertura de conectividad municipal?",
                "indicadores_dax": ["Promedio_Urbano (256)", "Promedio_Rural (231)", "Brecha_Urbano_Rural (24.02)"],
                "filtros": ["cole_depto_ubicacion", "fami_tieneinternet"]
            },
            {
                "id": "T3",
                "titulo": "Comportamiento Temporal y Pandemia",
                "pregunta": "¿Cómo varió el rendimiento académico general y la tenencia de herramientas tecnológicas en los hogares antes, durante y después del confinamiento (2019–2025)?",
                "indicadores_dax": ["Promedio_Global (251.52)", "%_Con_PC (53%)", "Maximo_Puntaje (500)"],
                "filtros": ["cole_area_ubicacion", "fami_estratovivienda"]
            },
            {
                "id": "T4",
                "titulo": "Análisis Multivariado",
                "pregunta": "¿De qué manera interactúan el nivel formativo de los padres, la tenencia de computador en el hogar y la naturaleza institucional del colegio sobre el rendimiento?",
                "indicadores_dax": ["Eval_Alto_Rendimiento (78 mil)", "%_Alto_Rendimiento (15%)", "Promedio_Global (248.11)"],
                "filtros": ["periodo (20202)", "cole_area_ubicacion"]
            }
        ],
        "conocimientos_evidentes": 12,
        "tableros_power_bi": 4
    }
    return jsonify(resumen)

if __name__ == '__main__':
    app.run(debug=True)
