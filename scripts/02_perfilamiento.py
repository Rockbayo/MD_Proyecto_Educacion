import os
import pandas as pd
import numpy as np

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
REPORTS_DIR = os.path.join(BASE_DIR, 'data', 'reports')

def ejecutar_perfilamiento():
    ruta_csv = os.path.join(PROCESSED_DIR, 'saber11_integrado.csv')
    ruta_salida = os.path.join(REPORTS_DIR, 'perfil_variables.csv')
    
    print(f"Cargando dataset para perfilamiento desde: {ruta_csv}...")
    # low_memory=False por el volumen de 4.5M de registros
    df = pd.read_csv(ruta_csv, low_memory=False)
    
    # 1. Volumetría y Duplicados
    filas, columnas = df.shape
    print("\nCalculando registros duplicados (esto puede tomar unos segundos)...")
    duplicados = df.duplicated().sum()
    print(f"Registros totales: {filas:,} | Variables: {columnas} | Duplicados exactos: {duplicados:,}")
    
    # 2. Perfilamiento base por variable
    print("Calculando estadísticas por variable...")
    perfil = pd.DataFrame({
        'Tipo': df.dtypes,
        'Nulos': df.isnull().sum(),
        '%_Nulos': (df.isnull().sum() / filas * 100).round(2),
        'Unicos': df.nunique()
    })
    
    # 3. Estadísticas numéricas (Min, Max, Promedio)
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        stats = df[num_cols].describe().T[['min', 'max', 'mean']].round(2)
        perfil = perfil.join(stats)
    else:
        perfil['min'] = np.nan
        perfil['max'] = np.nan
        perfil['mean'] = np.nan
    
    # Exportar resultados
    perfil.index.name = 'Variable'
    perfil.to_csv(ruta_salida)
    
    print(f"\nPerfilamiento completado. Archivo generado exitosamente en:\n{ruta_salida}")
    
    # Muestra rápida en consola de las variables con más nulos
    print("\nTop 5 variables con mayor porcentaje de nulos:")
    print(perfil.sort_values(by='%_Nulos', ascending=False)[['Tipo', '%_Nulos', 'Unicos']].head(5))

if __name__ == '__main__':
    ejecutar_perfilamiento()