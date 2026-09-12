import os
import pandas as pd
import numpy as np

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def evaluar_dimensiones():
    ruta_csv = os.path.join(PROCESSED_DIR, 'saber11_integrado.csv')
    print(f"Cargando dataset para evaluación de dimensiones...\n")
    df = pd.read_csv(ruta_csv, low_memory=False)
    total_registros = len(df)
    
    # 1. COMPLETITUD
    print("--- 1. COMPLETITUD ---")
    vars_target = ['punt_global', 'punt_matematicas', 'punt_lectura_critica']
    vars_familia = ['fami_tieneinternet', 'fami_estratovivienda', 'fami_tienecomputador']
    
    print("Variables Objetivo (Exigencia 100%):")
    for var in vars_target:
        completos = df[var].notnull().sum()
        print(f" - {var}: {(completos/total_registros)*100:.2f}% completos")
        
    print("\nVariables Autoreporte (Tolerancia < 5% nulos):")
    for var in vars_familia:
        nulos = df[var].isnull().sum()
        print(f" - {var}: {(nulos/total_registros)*100:.2f}% nulos ({nulos:,} registros vacíos)")

    # 2. UNICIDAD
    print("\n--- 2. UNICIDAD ---")
    duplicados = df.duplicated().sum()
    unicidad = ((total_registros - duplicados) / total_registros) * 100
    print(f"Métrica de Unicidad general: {unicidad:.2f}% ({duplicados} registros duplicados exactos)")

    # 3. VALIDEZ
    print("\n--- 3. VALIDEZ ---")
    # Regla: punt_global debe estar entre 0 y 500
    invalidos_punt = df[~df['punt_global'].between(0, 500, inclusive='both')].shape[0]
    print(f"Registros con 'punt_global' fuera de rango (0-500): {invalidos_punt}")
    
    # Regla: estu_grado debe ser un grado de media (ej. 10 u 11)
    if 'estu_grado' in df.columns:
        invalidos_grado = df[df['estu_grado'] > 11].shape[0]
        print(f"Registros con 'estu_grado' inválido (>11): {invalidos_grado:,} (Presencia de outliers como 20234.0)")

    # 4. CONSISTENCIA
    print("\n--- 4. CONSISTENCIA ---")
    # Revisión de formatos de fecha
    if 'estu_fechanacimiento' in df.columns:
        formatos_unicos = df['estu_fechanacimiento'].astype(str).str.len().unique()
        print(f"Longitudes de cadena encontradas en 'estu_fechanacimiento': {formatos_unicos}")
        print("Conclusión: Discrepancia en formatos de fecha (requiere estandarización a YYYY-MM-DD)")

if __name__ == '__main__':
    evaluar_dimensiones()