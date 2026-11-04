import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_OUTPUT = os.path.join(BASE_DIR, 'data', 'reports', 'EduMetrics_Etapa5_Informe_Tecnico.pdf')

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748b"))
            
            # Header
            self.drawString(54, 750, "Universidad de Cundinamarca · Minería de Datos 2026-II · Etapa 5 (OLAP)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Footer
            self.line(54, 45, 558, 45)
            self.drawString(54, 32, "EduMetricsCO — Proyecto Saber 11 (4.54M Registros)")
            page_text = f"Página {self._pageNumber} de {page_count}"
            self.drawRightString(558, 32, page_text)
            self.restoreState()


def generar_pdf():
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    c_primary = colors.HexColor("#0f172a") # Dark Slate
    c_accent = colors.HexColor("#0284c7")  # Deep Sky Blue
    c_text = colors.HexColor("#334155")
    c_border = colors.HexColor("#e2e8f0")
    c_bg_light = colors.HexColor("#f8fafc")

    style_title = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=1
    )

    style_subtitle = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_accent,
        alignment=1
    )

    style_h1 = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    style_h2 = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        spaceAfter=5
    )

    style_code = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=4,
        spaceAfter=5
    )

    style_kpi = ParagraphStyle(
        'KPI_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=c_accent,
        alignment=1
    )

    story = []

    # =========================================================
    # PORTADA
    # =========================================================
    story.append(Spacer(1, 30))
    story.append(Paragraph("UNIVERSIDAD DE CUNDINAMARCA", style_title))
    story.append(Spacer(1, 6))
    story.append(Paragraph("FACULTAD DE INGENIERÍA · PROGRAMA DE INGENIERÍA DE SISTEMAS", style_subtitle))
    story.append(Paragraph("ESPACIO ACADÉMICO: MINERÍA DE DATOS · SEMESTRE 2026-II", style_subtitle))
    
    story.append(Spacer(1, 35))
    story.append(HRFlowable(width="100%", thickness=2, color=c_accent, spaceBefore=5, spaceAfter=20))
    
    story.append(Paragraph("INFORME TÉCNICO · ETAPA 5", ParagraphStyle('CoverH', parent=style_title, fontSize=16, leading=20)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("ANÁLISIS MULTIDIMENSIONAL / MODELO ESTRELLA OLAP", style_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Efecto de la Brecha Digital sobre el Rendimiento Académico en Saber 11 (2019-1 a 2025-2)", style_subtitle))
    
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=20, spaceAfter=30))
    story.append(Spacer(1, 20))

    # Tabla de metadatos de portada
    datos_portada = [
        [Paragraph("<b>Proyecto:</b>", style_body), Paragraph("EduMetricsCO — Plataforma Analítica Multidimensional", style_body)],
        [Paragraph("<b>Población:</b>", style_body), Paragraph("4,541,655 Evaluaciones Saber 11 (14 Semestres Académicos)", style_body)],
        [Paragraph("<b>Integrantes:</b>", style_body), Paragraph("Oscar Giovanni Robayo Olaya &amp; Oscar Felipe Delgado", style_body)],
        [Paragraph("<b>Docente:</b>", style_body), Paragraph("Evaluador de Minería de Datos", style_body)],
        [Paragraph("<b>Repositorio GitHub:</b>", style_body), Paragraph("https://github.com/Rockbayo/MD_Proyecto_Educacion", style_body)],
        [Paragraph("<b>Rama Oficial:</b>", style_body), Paragraph("feature/etapa-5", style_body)],
        [Paragraph("<b>Aplicación Web:</b>", style_body), Paragraph("http://127.0.0.1:5000/etapa5", style_body)],
        [Paragraph("<b>Fecha:</b>", style_body), Paragraph("Noviembre de 2026", style_body)]
    ]
    t_portada = Table(datos_portada, colWidths=[130, 374])
    t_portada.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_portada)
    story.append(PageBreak())

    # =========================================================
    # 1. RESUMEN EJECUTIVO Y CONTINUIDAD
    # =========================================================
    story.append(Paragraph("1. Resumen Ejecutivo y Continuidad del Proyecto", style_h1))
    story.append(Paragraph(
        "El presente informe documenta el desarrollo e implementación del <b>modelo multidimensional (esquema estrella)</b> "
        "para el proyecto EduMetricsCO. Se mantiene la continuidad estricta sobre el conjunto de datos de las etapas previas: "
        "<b>4,541,655 registros reales</b> correspondientes a 14 periodos continuos de las pruebas Saber 11 (2019-1 a 2025-2). "
        "La investigación profundiza en los 12 conocimientos evidentes de la Etapa 4 mediante consultas analíticas relacionales en SQLite "
        "y cuatro vistas interactivas en Flask provistas de operaciones OLAP (Drill-down, Roll-up, Slice, Dice y Pivot).",
        style_body
    ))
    story.append(Paragraph(
        "<b>Unidad de Análisis vs. Granularidad:</b> La unidad de análisis corresponde a la evaluación individual de un estudiante. "
        "La granularidad de la tabla de hechos (<code>fact_resultados_saber11</code>) representa una celda multidimensional agregada que consolida "
        "a los evaluados con idéntica combinación de dimensiones (Tiempo × Geografía × Perfil Digital × Socioeconómico), garantizando aditividad matemática perfecta.",
        style_body
    ))

    # =========================================================
    # 2. CUATRO PREGUNTAS ANALÍTICAS
    # =========================================================
    story.append(Spacer(1, 6))
    story.append(Paragraph("2. Formulación de las Cuatro Preguntas de Investigación", style_h1))
    
    preguntas_tabla = [
        [Paragraph("<b>Vista / Pregunta</b>", style_body), Paragraph("<b>Dimensiones y Jerarquías</b>", style_body), Paragraph("<b>Medidas Clave</b>", style_body)],
        [
            Paragraph("<b>P1 (Territorial):</b> ¿Cómo varía la penalización por exclusión digital sobre el puntaje global y matemáticas al desagregar desde regiones macro hacia departamentos y zonas?", style_body),
            Paragraph("dim_geografia (Región &rarr; Depto &rarr; Zona)<br/>dim_acceso_digital (Perfil TIC)", style_body),
            Paragraph("Promedio Global, Promedio Matemáticas, Brecha Digital (pts)", style_body)
        ],
        [
            Paragraph("<b>P2 (Temporal):</b> ¿Cómo varió la brecha público-privada a través de las etapas Pre-Pandemia, Pandemia y Post-Pandemia al controlar por tenencia de computador?", style_body),
            Paragraph("dim_tiempo (Etapa &rarr; Año &rarr; Periodo)<br/>dim_geografia (Sector Oficial/Privado)<br/>dim_acceso_digital (PC)", style_body),
            Paragraph("Promedio Global por sector, Diferencial de hardware, Brecha Privado-Público", style_body)
        ],
        [
            Paragraph("<b>P3 (Capital Cultural):</b> ¿En qué magnitud el computador en el hogar mitiga el bajo nivel educativo parental sobre lectura crítica, matemáticas y ciencias?", style_body),
            Paragraph("dim_socioeconomica (Escolaridad, Estrato)<br/>dim_acceso_digital (PC)", style_body),
            Paragraph("Promedios disciplinares (Lectura, Matemáticas, Ciencias), Ventaja mitigadora", style_body)
        ],
        [
            Paragraph("<b>P4 (Hábitos TIC):</b> ¿Cómo se relaciona la intensidad horaria de internet con el nivel B1/B+ de inglés frente al riesgo de caer en puntaje crítico (&lt; 220)?", style_body),
            Paragraph("dim_acceso_digital (Horas dedicación)<br/>dim_geografia (Zona, Sector)", style_body),
            Paragraph("Promedio Inglés, % Bilingüe (B1/B+), % Riesgo Crítico (&lt;220 pts)", style_body)
        ]
    ]
    t_preguntas = Table(preguntas_tabla, colWidths=[180, 160, 164])
    t_preguntas.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_preguntas)

    # =========================================================
    # 3. DISEÑO DEL MODELO ESTRELLA
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("3. Arquitectura del Modelo Estrella y Diccionario", style_h1))
    story.append(Paragraph(
        "El modelo se almacena en SQLite (<code>data/processed/edumetrics_olap.db</code>, 72.33 MB), optimizado con índices compuestos en claves foráneas. "
        "Estructura 1 tabla de hechos y 4 dimensiones:",
        style_body
    ))

    modelo_info = [
        [Paragraph("<b>Tabla</b>", style_body), Paragraph("<b>Rol / Tipo</b>", style_body), Paragraph("<b>Claves</b>", style_body), Paragraph("<b>Atributos Principales y Granularidad</b>", style_body)],
        [
            Paragraph("<b>fact_resultados_saber11</b>", style_body), Paragraph("Hechos", style_body),
            Paragraph("PK id_hecho<br/>FKs: id_tiempo, id_geografia, id_digital, id_socioeconomico", style_body),
            Paragraph("717,225 celdas agregadas. Medidas: num_evaluados, suma_punt_global, suma_matematicas, suma_ingles, eval_riesgo_bajo, eval_ingles_bilingue.", style_body)
        ],
        [
            Paragraph("<b>dim_tiempo</b>", style_body), Paragraph("Dimensión", style_body), Paragraph("PK id_tiempo", style_body),
            Paragraph("14 registros. periodo (20191-20252), anio, semestre_num, semestre_etiqueta, etapa_pandemia (Pre, Pandemia, Post).", style_body)
        ],
        [
            Paragraph("<b>dim_geografia</b>", style_body), Paragraph("Dimensión", style_body), Paragraph("PK id_geografia", style_body),
            Paragraph("198 combinaciones. region_dane (8 macro-regiones), cole_depto_ubicacion (33 entidades), cole_area_ubicacion, cole_naturaleza, cole_calendario.", style_body)
        ],
        [
            Paragraph("<b>dim_acceso_digital</b>", style_body), Paragraph("Dimensión", style_body), Paragraph("PK id_digital", style_body),
            Paragraph("54 combinaciones. perfil_acceso_tic (Pleno, Movil, Offline, Exclusion), fami_tieneinternet, fami_tienecomputador, estu_dedicacioninternet.", style_body)
        ],
        [
            Paragraph("<b>dim_socioeconomica</b>", style_body), Paragraph("Dimensión", style_body), Paragraph("PK id_socioeconomico", style_body),
            Paragraph("220 combinaciones. grupo_estrato (Bajo, Medio, Alto), fami_estratovivienda, grupo_educacion_padre (Primaria a Posgrado), estu_genero.", style_body)
        ]
    ]
    t_modelo = Table(modelo_info, colWidths=[120, 60, 110, 214])
    t_modelo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_modelo)

    # =========================================================
    # 4. COMPROBACIONES TÉCNICAS
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Comprobaciones de Calidad y Validación del Modelo", style_h1))
    story.append(Paragraph(
        "Se ejecutó el protocolo de verificación automática comparando la base relacional contra el archivo plano de 4.54M de registros (reporte en <code>validacion_modelo_estrella.json</code>):",
        style_body
    ))

    val_info = [
        [Paragraph("<b>Comprobación</b>", style_body), Paragraph("<b>Resultado CSV Origen</b>", style_body), Paragraph("<b>Resultado Modelo Estrella</b>", style_body), Paragraph("<b>Estado y Justificación</b>", style_body)],
        [
            Paragraph("<b>1. Volumetría e Integridad</b>", style_body),
            Paragraph("4,541,655 evaluados", style_body),
            Paragraph("4,541,655 evaluados<br/>0 foráneas huérfanas", style_body),
            Paragraph("<b>Aprobado (Diferencia: 0).</b> Cuadratura poblacional exacta al 100%.", style_body)
        ],
        [
            Paragraph("<b>2. Paridad Métrica</b>", style_body),
            Paragraph("Puntaje Global: 252.4228<br/>Matemáticas: 51.2312<br/>Inglés: 50.2534", style_body),
            Paragraph("Puntaje Global: 252.4228<br/>Matemáticas: 51.2312<br/>Inglés: 50.2534", style_body),
            Paragraph("<b>Aprobado.</b> Tolerancia matemática absoluta (0.0000 de desviación en medidas aditivas).", style_body)
        ],
        [
            Paragraph("<b>3. Segmentación TIC</b>", style_body),
            Paragraph("Con internet: 3,154,805 (260.67)<br/>Sin internet: 1,386,850 (233.66)", style_body),
            Paragraph("Con internet: 3,154,805 (260.67)<br/>Sin internet: 1,386,850 (233.66)", style_body),
            Paragraph("<b>Aprobado.</b> Concordancia idéntica en agregaciones bivariadas y segmentación de conectividad.", style_body)
        ]
    ]
    t_val = Table(val_info, colWidths=[120, 120, 120, 144])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_val)
    story.append(PageBreak())

    # =========================================================
    # 5. EVIDENCIAS DE LAS 5 OPERACIONES OLAP
    # =========================================================
    story.append(Paragraph("5. Evidencias de las Cinco Operaciones OLAP", style_h1))
    
    story.append(Paragraph("<b>5.1. Operación Drill-Down &amp; Roll-Up (Jerarquía Territorial · Vista 1)</b>", style_h2))
    story.append(Paragraph(
        "Permite alternar entre la visión macro-regional (Roll-up a 8 regiones DANE) y la exploración departamental (Drill-down a 33 entidades y zonas).",
        style_body
    ))
    story.append(Paragraph(
        "<code>SELECT g.region_dane, SUM(f.num_evaluados) AS n, ROUND(CAST(SUM(f.suma_punt_global) AS REAL)/SUM(f.num_evaluados),2) AS prom FROM fact_resultados_saber11 f JOIN dim_geografia g ON f.id_geografia = g.id_geografia GROUP BY g.region_dane ORDER BY prom DESC;</code>",
        style_code
    ))

    story.append(Paragraph("<b>5.2. Operación Slice (Corte Temporal · Vista 2)</b>", style_h2))
    story.append(Paragraph(
        "Aísla el subconjunto correspondiente a la etapa de pandemia (2020-2021) para estudiar el comportamiento escolar bajo confinamiento.",
        style_body
    ))
    story.append(Paragraph(
        "<code>SELECT t.periodo, g.cole_naturaleza, ROUND(CAST(SUM(f.suma_punt_global) AS REAL)/SUM(f.num_evaluados),2) AS prom FROM fact_resultados_saber11 f JOIN dim_tiempo t ON f.id_tiempo=t.id_tiempo JOIN dim_geografia g ON f.id_geografia=g.id_geografia WHERE t.etapa_pandemia LIKE '2. Pandemia%' GROUP BY t.periodo, g.cole_naturaleza;</code>",
        style_code
    ))

    story.append(Paragraph("<b>5.3. Operación Dice (Subcubo Multivariable · Vista 2 y 4)</b>", style_h2))
    story.append(Paragraph(
        "Intersecta simultáneamente tres dimensiones: Sector Oficial/Privado × Tenencia de Computador × Etapa Epidemiológica.",
        style_body
    ))
    story.append(Paragraph(
        "<code>SELECT t.etapa_pandemia, d.fami_tienecomputador, g.cole_naturaleza, ROUND(CAST(SUM(f.suma_punt_global) AS REAL)/SUM(f.num_evaluados),2) FROM fact_resultados_saber11 f JOIN dim_tiempo t ON f.id_tiempo=t.id_tiempo JOIN dim_geografia g ON f.id_geografia=g.id_geografia JOIN dim_acceso_digital d ON f.id_digital=d.id_digital GROUP BY t.etapa_pandemia, d.fami_tienecomputador, g.cole_naturaleza;</code>",
        style_code
    ))

    story.append(Paragraph("<b>5.4. Operación Pivot (Rotación de Ejes Matriciales · Vista 3)</b>", style_h2))
    story.append(Paragraph(
        "Rota los ejes relacionales ubicando el nivel educativo parental en filas y la presencia de computador en columnas para evaluar matrices de cruce.",
        style_body
    ))
    story.append(Paragraph(
        "<code>SELECT s.grupo_educacion_padre, d.fami_tienecomputador, SUM(f.num_evaluados), ROUND(CAST(SUM(f.suma_punt_global) AS REAL)/SUM(f.num_evaluados),2) FROM fact_resultados_saber11 f JOIN dim_socioeconomica s ON f.id_socioeconomico=s.id_socioeconomico JOIN dim_acceso_digital d ON f.id_digital=d.id_digital GROUP BY s.grupo_educacion_padre, d.fami_tienecomputador;</code>",
        style_code
    ))

    # =========================================================
    # 6. LOS OCHO CONOCIMIENTOS MULTIDIMENSIONALES (8 ELEMENTOS)
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("6. Documentación de los Ocho Conocimientos Multidimensionales", style_h1))
    story.append(Paragraph(
        "Cada conocimiento responde a una necesidad analítica específica y se estructura bajo los 8 elementos requeridos:",
        style_body
    ))

    conocimientos = [
        ("CM 1.1: Gradiente Territorial de Exclusión Digital en el Caribe",
         "¿Cuál es la magnitud de la brecha digital al desagregar por macro-regiones DANE?",
         "dim_geografia.region_dane, dim_acceso_digital.perfil_acceso_tic, punt_global",
         "Roll-up regional y cálculo de brecha entre Acceso Pleno y Exclusión Absoluta.",
         "Matriz interactiva Vista 1 (N = 931,451 en Región Caribe).",
         "La brecha digital más severa ocurre en la Región Caribe con 42.24 puntos de penalización (264.12 pts pleno vs 221.88 pts exclusión), frente a 31.15 pts en Bogotá.",
         "Supera la simple observación urbano-rural al evidenciar que la falta de conectividad profundiza las desigualdades regionales históricas.",
         "Focalización de redes dorsales de fibra óptica y subsidios de conexión fija en departamentos costeros.",
         "El indicador no mide ancho de banda efectivo ni estabilidad del fluido eléctrico."),

        ("CM 1.2: Penalización en Matemáticas en Sedes Rurales Periféricas",
         "¿Cómo castiga la falta de conectividad en matemáticas en departamentos periféricos?",
         "dim_geografia (Depto, Zona), dim_acceso_digital, punt_matematicas",
         "Drill-down a nivel departamental rural cruzado con perfiles de acceso.",
         "Gráfica territorial y matriz de desempeño en Vista 1.",
         "En Chocó, La Guajira y Magdalena, el promedio rural en matemáticas sin TIC es de 39.42 pts, ubicando al 87% en nivel insuficiente (Nivel 1).",
         "Demuestra que más de 12 puntos del rezago rural en ciencias exactas son atribuibles a la ausencia de recursos digitales.",
         "Dotación de laboratorios computacionales con simuladores matemáticos offline.",
         "No aísla el impacto de la formación pedagógica docente."),

        ("CM 2.1: Ampliación Asimétrica de la Brecha Público-Privada en Pandemia",
         "¿Cómo evolucionó la distancia entre colegios oficiales y no oficiales durante el COVID-19?",
         "dim_tiempo.etapa_pandemia, dim_geografia.cole_naturaleza, punt_global",
         "Slice en ventana epidemiológica (2020-2021) frente a Pre-pandemia (2019).",
         "Serie de tiempo en Vista 2 (4.54M evaluados en 14 periodos).",
         "La brecha privado-oficial se amplió en 5.82 puntos netos durante el confinamiento, escalando de 32.40 pts en 2019 a 38.22 pts en 2021-2.",
         "La caída académica fue casi exclusivamente absorbida por los colegios oficiales de calendario A.",
         "Priorización presupuestal para planes de tutorías y nivelación en colegios distritales y municipales.",
         "No se cuenta con la fecha exacta de reapertura presencial por municipio."),

        ("CM 2.2: Efecto Amortiguador del Computador en el Sector Oficial",
         "¿Qué papel jugó la disponibilidad de PC en los hogares oficiales durante el confinamiento?",
         "dim_tiempo.etapa_pandemia, dim_acceso_digital.fami_tienecomputador, punt_global",
         "Dice combinando sector público, hardware y periodos de confinamiento.",
         "Matriz de hardware por etapas en Vista 2.",
         "Los estudiantes oficiales con computador alcanzaron 261.15 pts en pandemia, superando en 27.15 pts a quienes carecían del equipo (234.00 pts).",
         "El computador evitó el colapso del aprendizaje remoto en estudiantes de bajos recursos.",
         "Sustentación de compras públicas masivas de dispositivos para estudiantes vulnerables.",
         "Se desconoce el grado de compartición del dispositivo con hermanos o padres."),

        ("CM 3.1: Efecto Mitigador del Computador sobre el Rezago Parental",
         "¿Puede el computador compensar la baja escolaridad de los padres?",
         "dim_socioeconomica.grupo_educacion_padre, dim_acceso_digital, punt_global",
         "Operación Pivot disponiendo educación en filas y PC en columnas.",
         "Matriz pivote Vista 3 (N = 824,000 padres sin escolaridad o primaria incompleta).",
         "Un estudiante con padres sin escolaridad pero con PC obtiene 244.18 pts, superando en 28.52 pts a su par sin computador (215.66 pts).",
         "El equipamiento tecnológico actúa como puente que atenúa el determinismo sociocultural del hogar.",
         "Inclusión de dotación tecnológica como pilar de política social para romper trampas de pobreza intergeneracional.",
         "Tasa de no respuesta del 19.99% en el autorreporte de educación de los padres."),

        ("CM 3.2: Mayor Sensibilidad de la Lectura Crítica ante el Equipamiento TIC",
         "¿Qué competencia disciplinar es más sensible a la presencia del computador?",
         "dim_socioeconomica, punt_lectura_critica, punt_matematicas, punt_c_naturales",
         "Agregación multidimensional de puntajes por área bajo estrato bajo.",
         "Radar de competencias en Vista 3.",
         "La ventaja del PC en estratos 1 y 2 es de 6.81 puntos en Lectura Crítica, frente a 4.92 en Ciencias Naturales y 5.12 en Matemáticas.",
         "El acceso a textos electrónicos, interfaces interactivas y bibliotecas virtuales impacta preferencialmente la comprensión lectora.",
         "Despliegue de plataformas de lectura comprensiva guiada en tablets escolares.",
         "La prueba mide aptitud psicométrica formal y no hábitos lectores extracurriculares."),

        ("CM 4.1: Salto Exponencial al Bilingüismo por Intensidad de Navegación",
         "¿Cuál es el vínculo entre las horas de navegación y el nivel de inglés B1/B+?",
         "dim_acceso_digital.estu_dedicacioninternet, desemp_ingles, punt_ingles",
         "Drill-down por tramos horarios y cálculo de proporción de bilingüismo.",
         "Gráfico de barras y línea en Vista 4.",
         "Navegar más de 3 horas diarias multiplica por 6 la probabilidad de ser bilingüe: 17.91% alcanza B1/B+ (54.0 pts) vs 2.94% sin conexión (43.47 pts).",
         "El aprendizaje de un segundo idioma se beneficia del consumo multimedia y la inmersión informal en la red.",
         "Promover el autoaprendizaje y aplicaciones de idiomas libres de consumo de datos para bachilleres.",
         "No se diferencia el uso recreativo en redes sociales del uso educativo formal."),

        ("CM 4.2: La Desconexión Total como Predictor de Riesgo Crítico",
         "¿En qué medida no navegar en internet dispara el riesgo académico (<220 pts)?",
         "dim_acceso_digital.estu_dedicacioninternet, eval_riesgo_bajo, fami_estratovivienda",
         "Operación Dice calculando la tasa de evaluados con puntaje inferior a 220.",
         "Gráfico de dona y matriz de riesgo en Vista 4.",
         "El 53.83% de los estudiantes sin internet cae en riesgo crítico (< 220 pts), tasa que se reduce a 22.76% en quienes navegan de 1 a 3 horas.",
         "La exclusión digital actúa como un factor de vulnerabilidad crítica en la evaluación oficial.",
         "Alertas tempranas automáticas para focalizar tutorías en bachilleres sin conectividad domiciliaria.",
         "Causalidad compartida con otras privaciones materiales del hogar.")
    ]

    for titulo, preg, dims, proc, evid, hall, interp, util, limit in conocimientos:
        c_box = [
            [Paragraph(f"<b>{titulo}</b>", ParagraphStyle('H_CM', parent=style_body, fontName='Helvetica-Bold', textColor=c_accent)), Paragraph("", style_body)],
            [Paragraph("<b>Pregunta:</b>", style_body), Paragraph(preg, style_body)],
            [Paragraph("<b>Dimensiones / Medidas:</b>", style_body), Paragraph(dims, style_body)],
            [Paragraph("<b>Procedimiento OLAP:</b>", style_body), Paragraph(proc, style_body)],
            [Paragraph("<b>Evidencia Numérica:</b>", style_body), Paragraph(evid, style_body)],
            [Paragraph("<b>Hallazgo con Cifras:</b>", style_body), Paragraph(hall, style_body)],
            [Paragraph("<b>Interpretación vs. Evidente:</b>", style_body), Paragraph(interp, style_body)],
            [Paragraph("<b>Utilidad para Decisiones:</b>", style_body), Paragraph(util, style_body)],
            [Paragraph("<b>Limitación Metodológica:</b>", style_body), Paragraph(limit, style_body)]
        ]
        t_cm = Table(c_box, colWidths=[130, 374])
        t_cm.setStyle(TableStyle([
            ('SPAN', (0,0), (1,0)),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('GRID', (0,0), (-1,-1), 0.5, c_border),
            ('PADDING', (0,0), (-1,-1), 3.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t_cm)
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # =========================================================
    # 7. SÍNTESIS DE LIMITACIONES Y DECISIONES
    # =========================================================
    story.append(Paragraph("7. Limitaciones y Decisiones de Política Educativa", style_h1))
    
    lim_dec_data = [
        [Paragraph("<b>Dimensión / Vista</b>", style_body), Paragraph("<b>Limitación Metodológica</b>", style_body), Paragraph("<b>Decisión Sustentada en Cifras</b>", style_body)],
        [
            Paragraph("<b>Vista 1 (Territorial)</b>", style_body),
            Paragraph("No se dispone del costo del servicio de internet ni de la velocidad en megabits por municipio.", style_body),
            Paragraph("<b>Conectividad Diferencial:</b> Priorizar subsidios de fibra óptica en 140 municipios del Caribe y Pacífico con brecha superior a 40 puntos.", style_body)
        ],
        [
            Paragraph("<b>Vista 2 (Temporal)</b>", style_body),
            Paragraph("Falta de fecha exacta de reapertura física de sedes escolares durante el año lectivo 2021.", style_body),
            Paragraph("<b>Fondo de Resiliencia Tecnológica:</b> Asignar terminales portátiles al 100% de colegios oficiales para mitigar futuras contingencias.", style_body)
        ],
        [
            Paragraph("<b>Vista 3 (Capital Cultural)</b>", style_body),
            Paragraph("Tasa de no respuesta del 19.99% en educación de los padres que requiere tipificación explícita.", style_body),
            Paragraph("<b>Alfabetización Familiar:</b> Acompañar la entrega de dispositivos escolares con talleres de competencias digitales para adultos en estrato 1.", style_body)
        ],
        [
            Paragraph("<b>Vista 4 (Hábitos TIC)</b>", style_body),
            Paragraph("El instrumento no registra el uso pedagógico específico durante las horas de conexión.", style_body),
            Paragraph("<b>Ecosistemas de Inmersión:</b> Disponer plataformas gratuitas de aprendizaje de inglés sin costo de navegación móvil para bachilleres.", style_body)
        ]
    ]
    t_lim_dec = Table(lim_dec_data, colWidths=[120, 180, 204])
    t_lim_dec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_lim_dec)

    # =========================================================
    # 8. CONCLUSIONES Y REPOSITORIO GITHUB
    # =========================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("8. Conclusiones y Trazabilidad en GitHub", style_h1))
    story.append(Paragraph(
        "<b>Conclusiones del Estudio:</b><br/>"
        "1. <b>Viabilidad del Modelo Estrella:</b> El esquema implementado en SQLite comprime 4.54M de registros en 72 MB y entrega respuestas en menos de 30 ms para cubos analíticos complejos.<br/>"
        "2. <b>El Factor Habilitador de la Tecnología:</b> La tenencia de computador en el hogar atenúa en más de 28 puntos la desventaja académica impuesta por la baja escolaridad parental.<br/>"
        "3. <b>Severidad de la Brecha Periférica:</b> La brecha digital en la Región Caribe (42.24 pts) casi duplica el rezago geográfico promedio urbano-rural (24 pts).<br/>"
        "4. <b>Vínculo con el Bilingüismo:</b> El acceso intensivo a internet multiplica por 6 la probabilidad de alcanzar niveles internacionales B1/B+ en inglés.",
        style_body
    ))
    story.append(Spacer(1, 6))

    repo_data = [
        [Paragraph("<b>Parámetro</b>", style_body), Paragraph("<b>Valor de Verificación en Repositorio</b>", style_body)],
        [Paragraph("<b>Repositorio Oficial:</b>", style_body), Paragraph("https://github.com/Rockbayo/MD_Proyecto_Educacion", style_body)],
        [Paragraph("<b>Rama Activa:</b>", style_body), Paragraph("feature/etapa-5 (Sincronizada con origin/feature/etapa-5)", style_body)],
        [Paragraph("<b>Pull Request:</b>", style_body), Paragraph("https://github.com/Rockbayo/MD_Proyecto_Educacion/pull/25", style_body)],
        [Paragraph("<b>Commits de la Etapa:</b>", style_body), Paragraph("a8abeef, d71082f, 205f16c, 0bdf215, 2b6f996 (5 commits distribuidos)", style_body)],
        [Paragraph("<b>Script ETL Reproducible:</b>", style_body), Paragraph("scripts/07_modelo_estrella_olap.py", style_body)],
        [Paragraph("<b>Base de Datos Analítica:</b>", style_body), Paragraph("data/processed/edumetrics_olap.db (72.33 MB SQLite)", style_body)],
        [Paragraph("<b>Portal y Vistas Web:</b>", style_body), Paragraph("http://127.0.0.1:5000/etapa5 (Templates pregunta1.html a pregunta4.html)", style_body)]
    ]
    t_repo = Table(repo_data, colWidths=[150, 354])
    t_repo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_bg_light),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_repo)

    # Compilación con NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF generado exitosamente en: {PDF_OUTPUT}")

if __name__ == '__main__':
    generar_pdf()
