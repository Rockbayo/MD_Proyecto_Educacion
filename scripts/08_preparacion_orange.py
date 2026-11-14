import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_CSV = os.path.join(BASE_DIR, 'data', 'raw', 'saber11_muestra_1M.csv')
OUTPUT_CSV = os.path.join(BASE_DIR, 'data', 'processed', 'saber11_orange_100k.csv')
OUTPUT_ORANGE_TAB = os.path.join(BASE_DIR, 'data', 'processed', 'saber11_orange_100k.tab')

def homologar_educacion(val):
    if pd.isna(val) or val in ['No Sabe', 'No Informa', 'NO APLICA', '']:
        return 'No Sabe / No Informa'
    val_str = str(val).strip()
    if any(k in val_str for k in ['Ninguno', 'Primaria incompleta', 'Primaria completa']):
        return 'Primaria o Ninguno'
    elif any(k in val_str for k in ['Secundaria (Bachillerato) incompleta', 'Secundaria (Bachillerato) completa']):
        return 'Secundaria / Media'
    elif any(k in val_str for k in ['Técnica o tecnológica incompleta', 'Técnica o tecnológica completa', 'Técnica', 'Tecnológica']):
        return 'Técnica / Tecnológica'
    elif any(k in val_str for k in ['Educación profesional (Pregrado) incompleta', 'Educación profesional (Pregrado) completa', 'Postgrado', 'Especialización', 'Maestría', 'Doctorado']):
        return 'Universitaria y Posgrado'
    return 'No Sabe / No Informa'

def homologar_estrato(val):
    if pd.isna(val) or val in ['Sin Estrato', 'No Informa', '']:
        return 'Sin Estrato'
    val_str = str(val).strip()
    for i in range(1, 7):
        if str(i) in val_str:
            return f'Estrato {i}'
    return 'Sin Estrato'

def homologar_dedicacion(val):
    if pd.isna(val) or val in ['No Informa', '']:
        return 'No Informa'
    val_str = str(val).strip().upper()
    if 'NO NAVEGA' in val_str or 'NO' in val_str and 'TIENE' in val_str:
        return 'No navega internet'
    elif '30 MINUTOS' in val_str or 'MENOS' in val_str:
        return '30 minutos o menos'
    elif '30 Y 60' in val_str:
        return 'Entre 30 y 60 minutos'
    elif '1 Y 3' in val_str:
        return 'Entre 1 y 3 horas'
    elif 'MÁS DE 3' in val_str or 'MAS DE 3' in val_str:
        return 'Más de 3 horas'
    return 'No Informa'

def preparar_datos_orange():
    print(f"Leyendo microdatos desde: {INPUT_CSV}")
    cols_usar = [
        'periodo', 'cole_area_ubicacion', 'cole_naturaleza', 'cole_calendario',
        'cole_depto_ubicacion', 'estu_genero', 'fami_estratovivienda',
        'fami_educacionpadre', 'fami_educacionmadre', 'fami_tieneinternet',
        'fami_tienecomputador', 'estu_dedicacioninternet', 'punt_global'
    ]

    df = pd.read_csv(INPUT_CSV, usecols=cols_usar, low_memory=False)
    print(f"Total registros leídos: {len(df):,}")

    # 1. Filtrar registros válidos con puntaje global
    df = df[df['punt_global'].notna() & (df['punt_global'] > 0)].copy()

    # 2. Homologación y limpieza de variables
    df['periodo'] = df['periodo'].astype(int)
    df['cole_area_ubicacion'] = df['cole_area_ubicacion'].fillna('URBANO').str.strip().str.upper()
    df['cole_naturaleza'] = df['cole_naturaleza'].fillna('OFICIAL').str.strip().str.upper()
    df['cole_calendario'] = df['cole_calendario'].fillna('A').str.strip().str.upper()
    df['cole_calendario'] = df['cole_calendario'].apply(lambda x: x if x in ['A', 'B'] else 'OTRO')
    df['cole_depto_ubicacion'] = df['cole_depto_ubicacion'].fillna('BOGOTA').str.strip().str.upper()
    df['estu_genero'] = df['estu_genero'].fillna('F').str.strip().str.upper()
    df['estu_genero'] = df['estu_genero'].apply(lambda x: x if x in ['F', 'M'] else 'F')

    df['fami_tieneinternet'] = df['fami_tieneinternet'].fillna('NO').str.strip().str.upper()
    df['fami_tieneinternet'] = df['fami_tieneinternet'].apply(lambda x: 'SI' if x == 'SI' else 'NO')

    df['fami_tienecomputador'] = df['fami_tienecomputador'].fillna('NO').str.strip().str.upper()
    df['fami_tienecomputador'] = df['fami_tienecomputador'].apply(lambda x: 'SI' if x == 'SI' else 'NO')

    df['fami_estratovivienda'] = df['fami_estratovivienda'].apply(homologar_estrato)
    df['fami_educacionpadre'] = df['fami_educacionpadre'].apply(homologar_educacion)
    df['fami_educacionmadre'] = df['fami_educacionmadre'].apply(homologar_educacion)
    df['estu_dedicacioninternet'] = df['estu_dedicacioninternet'].apply(homologar_dedicacion)

    # 3. Variable Objetivo de Clasificación (Riesgo Crítico: puntaje < 220)
    df['riesgo_critico'] = np.where(df['punt_global'] < 220, 'SI', 'NO')

    print(f"Distribución de Riesgo Crítico en la población base:")
    print(df['riesgo_critico'].value_counts(normalize=True).round(4) * 100)

    # 4. Muestreo estratificado de 100,000 registros
    # Estratificamos por periodo y riesgo_critico para garantizar representatividad
    n_muestra = 100000
    frac = n_muestra / len(df)
    
    df_muestra = df.groupby(['periodo', 'riesgo_critico'], group_keys=False).apply(
        lambda x: x.sample(frac=frac, random_state=42)
    ).reset_index(drop=True)

    # Ajuste fino por si difiere por redondeo
    if len(df_muestra) > n_muestra:
        df_muestra = df_muestra.sample(n=n_muestra, random_state=42).reset_index(drop=True)
    elif len(df_muestra) < n_muestra:
        faltantes = n_muestra - len(df_muestra)
        pool = df[~df.index.isin(df_muestra.index)]
        df_muestra = pd.concat([df_muestra, pool.sample(n=faltantes, random_state=42)]).reset_index(drop=True)

    print(f"\nMuestra final generada: {len(df_muestra):,} registros")
    print(f"Media de Puntaje Global en muestra: {df_muestra['punt_global'].mean():.2f} pts (Base: {df['punt_global'].mean():.2f} pts)")
    print(f"Porcentaje de Riesgo Crítico en muestra: {(df_muestra['riesgo_critico'] == 'SI').mean()*100:.2f}%")

    # 5. Exportar CSV estándar para Orange y Python
    cols_orden = [
        'periodo', 'cole_depto_ubicacion', 'cole_area_ubicacion', 'cole_naturaleza',
        'cole_calendario', 'estu_genero', 'fami_estratovivienda', 'fami_educacionpadre',
        'fami_educacionmadre', 'fami_tieneinternet', 'fami_tienecomputador',
        'estu_dedicacioninternet', 'punt_global', 'riesgo_critico'
    ]
    df_muestra = df_muestra[cols_orden]
    df_muestra.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"Archivo CSV guardado exitosamente en: {OUTPUT_CSV}")

    # 6. Exportar formato nativo Orange TAB (con metadatos de tipos y roles)
    # Fila 1: Nombres de columnas
    # Fila 2: Tipos (continuous / discrete / string)
    # Fila 3: Rol (class / meta / feature)
    types_row = [
        'continuous', 'discrete', 'discrete', 'discrete', 'discrete',
        'discrete', 'discrete', 'discrete', 'discrete', 'discrete',
        'discrete', 'discrete', 'continuous', 'discrete'
    ]
    flags_row = [
        'meta', '', '', '', '',
        '', '', '', '', '',
        '', '', 'meta', 'class'
    ]

    with open(OUTPUT_ORANGE_TAB, 'w', encoding='utf-8') as f:
        f.write('\t'.join(cols_orden) + '\n')
        f.write('\t'.join(types_row) + '\n')
        f.write('\t'.join(flags_row) + '\n')
        for _, row in df_muestra.iterrows():
            f.write('\t'.join(str(val) for val in row.values) + '\n')

    print(f"Archivo Orange TAB guardado exitosamente en: {OUTPUT_ORANGE_TAB}")
    print("Dataset preparado y listo para los flujos supervisados y no supervisados.")

if __name__ == '__main__':
    preparar_datos_orange()
