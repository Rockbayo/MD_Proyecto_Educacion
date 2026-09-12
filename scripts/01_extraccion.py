import os
import pandas as pd

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

def consolidar_txt_locales(delimitador=';', codificacion='utf-8'):
    """
    Lee y concatena todos los archivos .txt en data/raw/
    Ajusta el delimitador (';', '|', o ',') según el formato del ICFES.
    """
    archivos = [f for f in os.listdir(RAW_DIR) if f.endswith('.txt')]
    if not archivos:
        print("No se encontraron archivos .txt en data/raw/")
        return None
        
    print(f"Consolidando {len(archivos)} archivos...")
    dfs = []
    
    for archivo in archivos:
        print(f"Procesando {archivo}...")
        ruta_archivo = os.path.join(RAW_DIR, archivo)
        try:
            # low_memory=False evita advertencias por tipos de datos mixtos en archivos grandes
            df = pd.read_csv(ruta_archivo, sep=delimitador, encoding=codificacion, low_memory=False)
            dfs.append(df)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")
            print("Intenta cambiar el delimitador a '|' o la codificación a 'latin-1'")
            return None
            
    df_consolidado = pd.concat(dfs, ignore_index=True)
    ruta_salida = os.path.join(PROCESSED_DIR, 'saber11_integrado.csv')
    
    # Exportamos el consolidado como un CSV estándar separado por comas
    df_consolidado.to_csv(ruta_salida, index=False)
    print(f"Consolidación exitosa. Dataset final ({len(df_consolidado):,} registros) guardado en: {ruta_salida}")
    return df_consolidado

if __name__ == '__main__':
    # Ejecutar la consolidación
    # Si al ejecutar te da error de formato, cambia delimitador a '|' o ',' 
    consolidar_txt_locales(delimitador=';', codificacion='utf-8')