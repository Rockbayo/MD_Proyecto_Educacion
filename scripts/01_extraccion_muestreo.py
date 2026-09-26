import os
import pandas as pd

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def consolidar_muestra_estratificada(fraccion=0.05, seed=42, delimitador=';', codificacion='utf-8'):
    """
    Lee cada archivo .txt en data/raw/ y extrae una muestra aleatoria reproducible
    (por defecto 5%) preservando la proporción exacta de cada periodo (muestreo estratificado).
    Consolida las muestras en 'data/processed/saber11_integrado_comprimido.csv'.
    """
    archivos = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('.txt')])
    if not archivos:
        print("No se encontraron archivos .txt en data/raw/")
        return None

    print(f"Iniciando muestreo del {fraccion*100:.0f}% estratificado por archivo...")
    print(f"Archivos a procesar: {len(archivos)}\n")
    
    muestras = []
    total_poblacion = 0
    total_muestra = 0

    for archivo in archivos:
        ruta_archivo = os.path.join(RAW_DIR, archivo)
        try:
            # Leemos el archivo periodo a periodo
            df = pd.read_csv(ruta_archivo, sep=delimitador, encoding=codificacion, low_memory=False)
            n_poblacion = len(df)
            total_poblacion += n_poblacion
            
            # Muestreo aleatorio reproducible
            df_sample = df.sample(frac=fraccion, random_state=seed)
            n_sample = len(df_sample)
            total_muestra += n_sample
            
            print(f" - {archivo:<26} | Población: {n_poblacion:>7,} -> Muestra (5%): {n_sample:>6,}")
            muestras.append(df_sample)
            
            # Liberamos memoria del DataFrame completo antes del siguiente archivo
            del df
            
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")
            return None

    print("\nConcatenando muestras y unificando columnas...")
    df_consolidado = pd.concat(muestras, ignore_index=True)
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    ruta_salida = os.path.join(PROCESSED_DIR, 'saber11_integrado_comprimido.csv')
    
    print(f"Guardando archivo final en: {ruta_salida}...")
    df_consolidado.to_csv(ruta_salida, index=False)
    
    tamano_mb = os.path.getsize(ruta_salida) / (1024 * 1024)
    print("\n" + "="*60)
    print("MUESTREO Y CONSOLIDACIÓN EXITOSOS")
    print("="*60)
    print(f"Registros originales:  {total_poblacion:,}")
    print(f"Registros muestreados: {total_muestra:,} ({total_muestra/total_poblacion*100:.2f}%)")
    print(f"Columnas integradas:   {len(df_consolidado.columns)}")
    print(f"Tamaño en disco:       {tamano_mb:.2f} MB")
    print(f"Ubicación:             {ruta_salida}")
    print("="*60)
    
    return df_consolidado

if __name__ == '__main__':
    # Extraer el 5% aleatorio con semilla fija 42
    consolidar_muestra_estratificada(fraccion=0.05, seed=42)
