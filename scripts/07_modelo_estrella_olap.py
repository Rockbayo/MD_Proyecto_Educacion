import os
import time
import json
import sqlite3
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'data', 'reports')

RUTA_CSV = os.path.join(PROCESSED_DIR, 'saber11_integrado.csv')
RUTA_DB = os.path.join(PROCESSED_DIR, 'edumetrics_olap.db')
RUTA_VALIDACION = os.path.join(REPORTS_DIR, 'validacion_modelo_estrella.json')


def normalizar_texto_ascii(texto):
    if not isinstance(texto, str) or not texto:
        return 'NO_INFORMA'
    t = texto.strip().upper()
    reemplazos = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        '\xc1': 'A', '\xc9': 'E', '\xcd': 'I', '\xd3': 'O', '\xda': 'U',
        '\u0143': 'N', '\xd1': 'N', 'Ñ': 'N',
        '': ''
    }
    for k, v in reemplazos.items():
        t = t.replace(k, v)
    t = ' '.join(t.split())
    return t


def mapear_region_dane(depto):
    d = normalizar_texto_ascii(depto)
    regiones = {
        'BOGOTA': 'Región Metropolitana Bogotá',
        'BOGOTA D.C.': 'Región Metropolitana Bogotá',
        'CUNDINAMARCA': 'Región Centro Oriente',
        'BOYACA': 'Región Centro Oriente',
        'SANTANDER': 'Región Centro Oriente',
        'NORTE SANTANDER': 'Región Centro Oriente',
        'ANTIOQUIA': 'Región Eje Cafetero y Antioquia',
        'CALDAS': 'Región Eje Cafetero y Antioquia',
        'RISARALDA': 'Región Eje Cafetero y Antioquia',
        'QUINDIO': 'Región Eje Cafetero y Antioquia',
        'VALLE': 'Región Pacífico',
        'CAUCA': 'Región Pacífico',
        'NARINO': 'Región Pacífico',
        'CHOCO': 'Región Pacífico',
        'ATLANTICO': 'Región Caribe',
        'BOLIVAR': 'Región Caribe',
        'MAGDALENA': 'Región Caribe',
        'CESAR': 'Región Caribe',
        'CORDOBA': 'Región Caribe',
        'SUCRE': 'Región Caribe',
        'LA GUAJIRA': 'Región Caribe',
        'SAN ANDRES': 'Región Caribe',
        'TOLIMA': 'Región Centro Sur',
        'HUILA': 'Región Centro Sur',
        'CAQUETA': 'Región Centro Sur',
        'PUTUMAYO': 'Región Centro Sur',
        'AMAZONAS': 'Región Centro Sur',
        'META': 'Región Llano y Orinoquía',
        'CASANARE': 'Región Llano y Orinoquía',
        'ARAUCA': 'Región Llano y Orinoquía',
        'VICHADA': 'Región Llano y Orinoquía',
        'GUAVIARE': 'Región Llano y Orinoquía',
        'GUAINIA': 'Región Llano y Orinoquía',
        'VAUPES': 'Región Llano y Orinoquía',
        'NO APLICA': 'Población Individual / Validantes'
    }
    return regiones.get(d, 'Sin Información Territorial')


def mapear_grupo_estrato(estrato):
    e = normalizar_texto_ascii(estrato)
    if e in ('ESTRATO 1', 'ESTRATO 2'):
        return 'Bajo (Estratos 1 y 2)'
    elif e in ('ESTRATO 3', 'ESTRATO 4'):
        return 'Medio (Estratos 3 y 4)'
    elif e in ('ESTRATO 5', 'ESTRATO 6'):
        return 'Alto (Estratos 5 y 6)'
    return 'Sin Estratificación / Rural Disperso'


def mapear_nivel_educativo_grupo(edu):
    ed = normalizar_texto_ascii(edu)
    if 'PROFESIONAL' in ed or 'POSTGRADO' in ed or 'POSGRADO' in ed:
        return 'Superior y Posgrado'
    elif 'TECNICA' in ed or 'TECNOLOGICA' in ed:
        return 'Técnica y Tecnológica'
    elif 'SECUNDARIA' in ed or 'BACHILLERATO' in ed:
        return 'Secundaria / Media'
    elif 'PRIMARIA' in ed or 'NINGUNO' in ed:
        return 'Básica Primaria o Ninguno'
    return 'No Sabe / No Informa'


def mapear_perfil_tic(inet, pc):
    i = normalizar_texto_ascii(inet)
    p = normalizar_texto_ascii(pc)
    if i == 'SI' and p == 'SI':
        return 'Acceso Pleno (Internet + PC)'
    elif i == 'SI' and p == 'NO':
        return 'Conectividad Móvil / Sin PC (Solo Internet)'
    elif i == 'NO' and p == 'SI':
        return 'Equipo Offline (Solo PC)'
    elif i == 'NO' and p == 'NO':
        return 'Exclusión Digital Absoluta (Sin Internet ni PC)'
    return 'No Informa / Parcial'


def construir_modelo_estrella():
    t0 = time.time()
    print(f"Iniciando construcción del Modelo Estrella desde: {RUTA_CSV}")

    columnas_lectura = [
        'periodo', 'cole_depto_ubicacion', 'cole_mcpio_ubicacion', 'cole_area_ubicacion',
        'cole_naturaleza', 'cole_calendario', 'fami_tieneinternet', 'fami_tienecomputador',
        'estu_dedicacioninternet', 'fami_estratovivienda', 'fami_educacionpadre',
        'estu_genero', 'punt_global', 'punt_matematicas', 'punt_lectura_critica',
        'punt_ingles', 'punt_c_naturales', 'punt_sociales_ciudadanas', 'desemp_ingles'
    ]

    # Estadísticas globales directas sobre el dataset tratado para las 3 comprobaciones
    total_origen = 0
    suma_global_origen = 0.0
    suma_mate_origen = 0.0
    suma_lectura_origen = 0.0
    suma_ingles_origen = 0.0
    conteo_ingles_origen = 0

    chunks_agrupados = []
    chunks_mcpio = []

    cols_grupo_principal = [
        'periodo', 'cole_depto_ubicacion', 'cole_area_ubicacion',
        'cole_naturaleza', 'cole_calendario', 'fami_tieneinternet',
        'fami_tienecomputador', 'estu_dedicacioninternet',
        'fami_estratovivienda', 'fami_educacionpadre', 'estu_genero'
    ]

    cols_grupo_mcpio = [
        'periodo', 'cole_depto_ubicacion', 'cole_mcpio_ubicacion',
        'cole_area_ubicacion', 'cole_naturaleza', 'fami_tieneinternet',
        'fami_tienecomputador'
    ]

    lote = 0
    for chunk in pd.read_csv(RUTA_CSV, usecols=columnas_lectura, chunksize=300_000, low_memory=False):
        lote += 1
        n_chunk = len(chunk)
        total_origen += n_chunk

        # Normalizar textos a cadenas limpias y homologadas
        for col_txt in ['cole_depto_ubicacion', 'cole_mcpio_ubicacion', 'cole_area_ubicacion',
                        'cole_naturaleza', 'cole_calendario', 'fami_tieneinternet',
                        'fami_tienecomputador', 'estu_dedicacioninternet',
                        'fami_estratovivienda', 'fami_educacionpadre', 'estu_genero']:
            chunk[col_txt] = chunk[col_txt].apply(normalizar_texto_ascii)

        # Métricas base de origen
        suma_global_origen += float(chunk['punt_global'].sum())
        suma_mate_origen += float(chunk['punt_matematicas'].sum())
        suma_lectura_origen += float(chunk['punt_lectura_critica'].sum())

        mask_ing = chunk['punt_ingles'] >= 0
        suma_ingles_origen += float(chunk.loc[mask_ing, 'punt_ingles'].sum())
        conteo_ingles_origen += int(mask_ing.sum())

        # Columnas auxiliares para agregación aditiva exacta
        chunk['num_evaluados'] = 1
        chunk['eval_alto_rendimiento'] = (chunk['punt_global'] >= 300).astype('int64')
        chunk['eval_riesgo_bajo'] = (chunk['punt_global'] < 220).astype('int64')
        chunk['eval_ingles_bilingue'] = chunk['desemp_ingles'].isin(['B1', 'B+']).astype('int64')
        chunk['eval_ingles_presente'] = mask_ing.astype('int64')
        chunk['punt_ingles_valido'] = np.where(mask_ing, chunk['punt_ingles'], 0.0)

        cols_medidas = [
            'num_evaluados', 'punt_global', 'punt_matematicas',
            'punt_lectura_critica', 'punt_c_naturales', 'punt_sociales_ciudadanas',
            'punt_ingles_valido', 'eval_ingles_presente',
            'eval_alto_rendimiento', 'eval_riesgo_bajo', 'eval_ingles_bilingue'
        ]

        agrupado = chunk.groupby(cols_grupo_principal, as_index=False, observed=True)[cols_medidas].sum()
        chunks_agrupados.append(agrupado)

        agrupado_m = chunk.groupby(cols_grupo_mcpio, as_index=False, observed=True)[cols_medidas].sum()
        chunks_mcpio.append(agrupado_m)

        print(f"  [Lote {lote:02d}] Leídos acumulados: {total_origen:,}")

    print("\nConsolidando cubos multidimensionales en memoria...")
    df_cubo = pd.concat(chunks_agrupados, ignore_index=True).groupby(
        cols_grupo_principal, as_index=False, observed=True
    ).sum()

    df_cubo_mcpio = pd.concat(chunks_mcpio, ignore_index=True).groupby(
        cols_grupo_mcpio, as_index=False, observed=True
    ).sum()

    print(f"Filas en tabla de hechos principal (fact_saber11): {len(df_cubo):,}")
    print(f"Filas en tabla de detalle municipal (fact_saber11_municipal): {len(df_cubo_mcpio):,}")

    # =========================================================
    # CONSTRUCCIÓN DE LAS 4 TABLAS DE DIMENSIONES
    # =========================================================

    # 1. DIM_TIEMPO
    dim_tiempo = df_cubo[['periodo']].drop_duplicates().sort_values('periodo').reset_index(drop=True)
    dim_tiempo['id_tiempo'] = dim_tiempo.index + 1
    dim_tiempo['anio'] = (dim_tiempo['periodo'] // 10).astype('int64')
    dim_tiempo['semestre_num'] = (dim_tiempo['periodo'] % 10).astype('int64')
    dim_tiempo['semestre_etiqueta'] = np.where(
        dim_tiempo['semestre_num'] == 1,
        'Semestre 1 (Cal. B)',
        'Semestre 2 (Cal. A)'
    )
    dim_tiempo['etapa_pandemia'] = np.select(
        [
            dim_tiempo['anio'] == 2019,
            dim_tiempo['anio'].isin([2020, 2021]),
            dim_tiempo['anio'] >= 2022
        ],
        [
            '1. Pre-Pandemia (2019)',
            '2. Confinamiento y Pandemia (2020-2021)',
            '3. Post-Pandemia y Recuperación (2022-2025)'
        ],
        default='Otro'
    )

    # 2. DIM_GEOGRAFIA_INSTITUCION (Jerarquía Región -> Departamento -> Área -> Naturaleza -> Calendario)
    cols_geo = ['cole_depto_ubicacion', 'cole_area_ubicacion', 'cole_naturaleza', 'cole_calendario']
    dim_geografia = df_cubo[cols_geo].drop_duplicates().sort_values(cols_geo).reset_index(drop=True)
    dim_geografia['id_geografia'] = dim_geografia.index + 1
    dim_geografia['region_dane'] = dim_geografia['cole_depto_ubicacion'].apply(mapear_region_dane)

    # 3. DIM_ACCESO_DIGITAL (Jerarquía Perfil TIC -> Internet/PC -> Dedicación diaria)
    cols_dig = ['fami_tieneinternet', 'fami_tienecomputador', 'estu_dedicacioninternet']
    dim_digital = df_cubo[cols_dig].drop_duplicates().sort_values(cols_dig).reset_index(drop=True)
    dim_digital['id_digital'] = dim_digital.index + 1
    dim_digital['perfil_acceso_tic'] = [
        mapear_perfil_tic(i, p) for i, p in zip(dim_digital['fami_tieneinternet'], dim_digital['fami_tienecomputador'])
    ]

    # 4. DIM_SOCIOECONOMICA (Jerarquía Grupo Estrato -> Estrato -> Grupo Educación Padre -> Educación Padre -> Género)
    cols_soc = ['fami_estratovivienda', 'fami_educacionpadre', 'estu_genero']
    dim_socioeconomica = df_cubo[cols_soc].drop_duplicates().sort_values(cols_soc).reset_index(drop=True)
    dim_socioeconomica['id_socioeconomico'] = dim_socioeconomica.index + 1
    dim_socioeconomica['grupo_estrato'] = dim_socioeconomica['fami_estratovivienda'].apply(mapear_grupo_estrato)
    dim_socioeconomica['grupo_educacion_padre'] = dim_socioeconomica['fami_educacionpadre'].apply(mapear_nivel_educativo_grupo)

    # =========================================================
    # ASIGNACIÓN DE CLAVES FORÁNEAS EN TABLA DE HECHOS
    # =========================================================
    fact = df_cubo.merge(dim_tiempo[['id_tiempo', 'periodo']], on='periodo', how='left')
    fact = fact.merge(dim_geografia[['id_geografia'] + cols_geo], on=cols_geo, how='left')
    fact = fact.merge(dim_digital[['id_digital'] + cols_dig], on=cols_dig, how='left')
    fact = fact.merge(dim_socioeconomica[['id_socioeconomico'] + cols_soc], on=cols_soc, how='left')

    fact['id_hecho'] = np.arange(1, len(fact) + 1)

    columnas_fact_final = [
        'id_hecho', 'id_tiempo', 'id_geografia', 'id_digital', 'id_socioeconomico',
        'num_evaluados', 'punt_global', 'punt_matematicas', 'punt_lectura_critica',
        'punt_c_naturales', 'punt_sociales_ciudadanas', 'punt_ingles_valido',
        'eval_ingles_presente', 'eval_alto_rendimiento', 'eval_riesgo_bajo',
        'eval_ingles_bilingue'
    ]
    fact = fact[columnas_fact_final].rename(columns={
        'punt_global': 'suma_punt_global',
        'punt_matematicas': 'suma_matematicas',
        'punt_lectura_critica': 'suma_lectura_critica',
        'punt_c_naturales': 'suma_c_naturales',
        'punt_sociales_ciudadanas': 'suma_sociales_ciudadanas',
        'punt_ingles_valido': 'suma_ingles'
    })

    # Dimensión y hechos para drill-down hasta nivel Municipio
    df_cubo_mcpio['region_dane'] = df_cubo_mcpio['cole_depto_ubicacion'].apply(mapear_region_dane)
    df_cubo_mcpio['perfil_acceso_tic'] = [
        mapear_perfil_tic(i, p) for i, p in zip(df_cubo_mcpio['fami_tieneinternet'], df_cubo_mcpio['fami_tienecomputador'])
    ]
    df_cubo_mcpio = df_cubo_mcpio.rename(columns={
        'punt_global': 'suma_punt_global',
        'punt_matematicas': 'suma_matematicas',
        'punt_lectura_critica': 'suma_lectura_critica',
        'punt_c_naturales': 'suma_c_naturales',
        'punt_sociales_ciudadanas': 'suma_sociales_ciudadanas',
        'punt_ingles_valido': 'suma_ingles'
    })

    # =========================================================
    # PERSISTENCIA EN SQLITE E INDEXACIÓN RELACIONAL
    # =========================================================
    if os.path.exists(RUTA_DB):
        os.remove(RUTA_DB)

    print(f"\nCreando base de datos SQLite en: {RUTA_DB} ...")
    conn = sqlite3.connect(RUTA_DB)
    cur = conn.cursor()

    cur.executescript("""
        PRAGMA foreign_keys = ON;

        CREATE TABLE dim_tiempo (
            id_tiempo INTEGER PRIMARY KEY,
            periodo INTEGER NOT NULL UNIQUE,
            anio INTEGER NOT NULL,
            semestre_num INTEGER NOT NULL,
            semestre_etiqueta TEXT NOT NULL,
            etapa_pandemia TEXT NOT NULL
        );

        CREATE TABLE dim_geografia (
            id_geografia INTEGER PRIMARY KEY,
            region_dane TEXT NOT NULL,
            cole_depto_ubicacion TEXT NOT NULL,
            cole_area_ubicacion TEXT NOT NULL,
            cole_naturaleza TEXT NOT NULL,
            cole_calendario TEXT NOT NULL
        );

        CREATE TABLE dim_acceso_digital (
            id_digital INTEGER PRIMARY KEY,
            perfil_acceso_tic TEXT NOT NULL,
            fami_tieneinternet TEXT NOT NULL,
            fami_tienecomputador TEXT NOT NULL,
            estu_dedicacioninternet TEXT NOT NULL
        );

        CREATE TABLE dim_socioeconomica (
            id_socioeconomico INTEGER PRIMARY KEY,
            grupo_estrato TEXT NOT NULL,
            fami_estratovivienda TEXT NOT NULL,
            grupo_educacion_padre TEXT NOT NULL,
            fami_educacionpadre TEXT NOT NULL,
            estu_genero TEXT NOT NULL
        );

        CREATE TABLE fact_resultados_saber11 (
            id_hecho INTEGER PRIMARY KEY,
            id_tiempo INTEGER NOT NULL,
            id_geografia INTEGER NOT NULL,
            id_digital INTEGER NOT NULL,
            id_socioeconomico INTEGER NOT NULL,
            num_evaluados INTEGER NOT NULL,
            suma_punt_global REAL NOT NULL,
            suma_matematicas REAL NOT NULL,
            suma_lectura_critica REAL NOT NULL,
            suma_c_naturales REAL NOT NULL,
            suma_sociales_ciudadanas REAL NOT NULL,
            suma_ingles REAL NOT NULL,
            eval_ingles_presente INTEGER NOT NULL,
            eval_alto_rendimiento INTEGER NOT NULL,
            eval_riesgo_bajo INTEGER NOT NULL,
            eval_ingles_bilingue INTEGER NOT NULL,
            FOREIGN KEY (id_tiempo) REFERENCES dim_tiempo(id_tiempo),
            FOREIGN KEY (id_geografia) REFERENCES dim_geografia(id_geografia),
            FOREIGN KEY (id_digital) REFERENCES dim_acceso_digital(id_digital),
            FOREIGN KEY (id_socioeconomico) REFERENCES dim_socioeconomica(id_socioeconomico)
        );
    """)

    dim_tiempo[['id_tiempo', 'periodo', 'anio', 'semestre_num', 'semestre_etiqueta', 'etapa_pandemia']].to_sql(
        'dim_tiempo', conn, if_exists='append', index=False
    )
    dim_geografia[['id_geografia', 'region_dane', 'cole_depto_ubicacion', 'cole_area_ubicacion', 'cole_naturaleza', 'cole_calendario']].to_sql(
        'dim_geografia', conn, if_exists='append', index=False
    )
    dim_digital[['id_digital', 'perfil_acceso_tic', 'fami_tieneinternet', 'fami_tienecomputador', 'estu_dedicacioninternet']].to_sql(
        'dim_acceso_digital', conn, if_exists='append', index=False
    )
    dim_socioeconomica[['id_socioeconomico', 'grupo_estrato', 'fami_estratovivienda', 'grupo_educacion_padre', 'fami_educacionpadre', 'estu_genero']].to_sql(
        'dim_socioeconomica', conn, if_exists='append', index=False
    )
    fact.to_sql('fact_resultados_saber11', conn, if_exists='append', index=False)
    df_cubo_mcpio.to_sql('agg_territorial_municipio', conn, if_exists='replace', index=False)

    print("Creando índices de consulta analítica...")
    cur.executescript("""
        CREATE INDEX idx_fact_tiempo ON fact_resultados_saber11(id_tiempo);
        CREATE INDEX idx_fact_geo ON fact_resultados_saber11(id_geografia);
        CREATE INDEX idx_fact_dig ON fact_resultados_saber11(id_digital);
        CREATE INDEX idx_fact_soc ON fact_resultados_saber11(id_socioeconomico);
        CREATE INDEX idx_mcpio_depto ON agg_territorial_municipio(cole_depto_ubicacion, cole_mcpio_ubicacion);
        CREATE INDEX idx_mcpio_periodo ON agg_territorial_municipio(periodo);
    """)
    conn.commit()

    # =========================================================
    # VERIFICACIONES Y 3 COMPROBACIONES CONTRA DATOS TRATADOS
    # =========================================================
    print("\nEjecutando comprobaciones de integridad y cuadre contra origen...")

    # Comprobación 1: Conteo total de evaluados y ausencia de duplicaciones
    res_c1 = cur.execute("""
        SELECT
            SUM(f.num_evaluados) AS total_evaluados_estrella,
            COUNT(*) AS total_celdas_hechos,
            SUM(CASE WHEN f.id_tiempo IS NULL OR f.id_geografia IS NULL OR f.id_digital IS NULL OR f.id_socioeconomico IS NULL THEN 1 ELSE 0 END) AS huerfanos_fk
        FROM fact_resultados_saber11 f
        INNER JOIN dim_tiempo t ON f.id_tiempo = t.id_tiempo
        INNER JOIN dim_geografia g ON f.id_geografia = g.id_geografia
        INNER JOIN dim_acceso_digital d ON f.id_digital = d.id_digital
        INNER JOIN dim_socioeconomica s ON f.id_socioeconomico = s.id_socioeconomico
    """).fetchone()

    # Comprobación 2: Promedios ponderados globales y por área
    res_c2 = cur.execute("""
        SELECT
            ROUND(SUM(suma_punt_global) / SUM(num_evaluados), 4) AS prom_global,
            ROUND(SUM(suma_matematicas) / SUM(num_evaluados), 4) AS prom_mate,
            ROUND(SUM(suma_lectura_critica) / SUM(num_evaluados), 4) AS prom_lectura,
            ROUND(SUM(suma_ingles) / SUM(eval_ingles_presente), 4) AS prom_ingles
        FROM fact_resultados_saber11
    """).fetchone()

    # Comprobación 3: Distribución por acceso a internet y zona geográfica
    res_c3 = cur.execute("""
        SELECT
            d.fami_tieneinternet,
            SUM(f.num_evaluados) AS evaluados,
            ROUND(SUM(f.suma_punt_global) / SUM(f.num_evaluados), 2) AS promedio_global
        FROM fact_resultados_saber11 f
        JOIN dim_acceso_digital d ON f.id_digital = d.id_digital
        GROUP BY d.fami_tieneinternet
        ORDER BY evaluados DESC
    """).fetchall()

    cur.execute("VACUUM")
    conn.close()

    tamano_db_mb = os.path.getsize(RUTA_DB) / (1024 * 1024)
    prom_global_origen = round(suma_global_origen / total_origen, 4)
    prom_mate_origen = round(suma_mate_origen / total_origen, 4)
    prom_lectura_origen = round(suma_lectura_origen / total_origen, 4)
    prom_ingles_origen = round(suma_ingles_origen / conteo_ingles_origen, 4)

    reporte_validacion = {
        "fecha_generacion": time.strftime("%Y-%m-%d %H:%M:%S"),
        "tamano_db_mb": round(tamano_db_mb, 2),
        "dimensiones_conteo": {
            "dim_tiempo": len(dim_tiempo),
            "dim_geografia": len(dim_geografia),
            "dim_acceso_digital": len(dim_digital),
            "dim_socioeconomica": len(dim_socioeconomica),
            "fact_resultados_saber11": len(fact),
            "agg_territorial_municipio": len(df_cubo_mcpio)
        },
        "comprobacion_1_volumetria_e_integridad": {
            "evaluados_csv_tratado": total_origen,
            "evaluados_modelo_estrella": int(res_c1[0]),
            "diferencia_registros": total_origen - int(res_c1[0]),
            "registros_huerfanos_fk": int(res_c1[2]),
            "celdas_agrupadas_hechos": int(res_c1[1])
        },
        "comprobacion_2_exactitud_medidas": {
            "punt_global_csv": prom_global_origen,
            "punt_global_estrella": res_c2[0],
            "punt_matematicas_csv": prom_mate_origen,
            "punt_matematicas_estrella": res_c2[1],
            "punt_lectura_csv": prom_lectura_origen,
            "punt_lectura_estrella": res_c2[2],
            "punt_ingles_csv": prom_ingles_origen,
            "punt_ingles_estrella": res_c2[3]
        },
        "comprobacion_3_segmentacion_conectividad": [
            {"fami_tieneinternet": r[0], "evaluados": r[1], "promedio_global": r[2]}
            for r in res_c3
        ]
    }

    with open(RUTA_VALIDACION, 'w', encoding='utf-8') as f_json:
        json.dump(reporte_validacion, f_json, indent=2, ensure_ascii=False)

    print("============================================================")
    print("MODELO ESTRELLA CONSTRUIDO Y VALIDADO EXITOSAMENTE")
    print("============================================================")
    print(f" - Tamaño de edumetrics_olap.db:  {tamano_db_mb:.2f} MB")
    print(f" - Evaluados CSV vs Estrella:     {total_origen:,} vs {res_c1[0]:,} (Dif: {total_origen - res_c1[0]})")
    print(f" - Promedio Global CSV vs DB:     {prom_global_origen} vs {res_c2[0]}")
    print(f" - Huérfanos de clave foránea:    {res_c1[2]}")
    print(f" - Tiempo total:                  {time.time() - t0:.1f} s")
    print("============================================================")


if __name__ == '__main__':
    construir_modelo_estrella()

