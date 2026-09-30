import os
import pandas as pd

# Configuración dinámica de rutas basada en la estructura del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')

def generar_muestra_staging():
    ruta_origen = os.path.join(PROCESSED_DIR, 'saber11_integrado.csv')
    ruta_destino = os.path.join(RAW_DIR, 'saber11_muestra_1M.csv')

    print(f"Cargando dataset original (+4.5M registros)...")
    # Lectura optimizada en memoria
    df_original = pd.read_csv(ruta_origen, low_memory=False)

    print("Extrayendo muestra aleatoria de 1.000.000 de registros...")
    # random_state asegura que siempre se extraiga la misma muestra en caso de reprocesamiento
    df_muestra = df_original.sample(n=1000000, random_state=42)

    print("Exportando archivo de Staging...")
    # Exportación sin índice para mantener la estructura tabular intacta para SSIS
    df_muestra.to_csv(ruta_destino, index=False, encoding='utf-8')
    
    print(f"¡Éxito! Muestra generada en: {ruta_destino}")

if __name__ == '__main__':
    generar_muestra_staging()