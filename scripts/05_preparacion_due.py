import pandas as pd
import os

# Configuración de rutas basada en tu estructura
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')

ruta_entrada = os.path.join(RAW_DIR, 'ESTABLECIMIENTOS_EDUCATIVOS-COLOMBIA_20260928.csv')
ruta_salida = os.path.join(PROCESSED_DIR, 'Dim_DUE_Limpio.csv')

print("Cargando dataset DUE...")
df = pd.read_csv(ruta_entrada, sep=None, engine='python', encoding='utf-8')

# 1. Selección estricta de columnas necesarias para el Lookup
columnas_utiles = ['codigoestablecimiento', 'zona', 'nombreestablecimiento', 'nombremunicipio']
df_due = df[columnas_utiles].copy()

# 2. Limpieza de la llave primaria (codigoestablecimiento)
# Eliminación de comillas/comas y casteo a Entero Largo (BIGINT)
df_due['codigoestablecimiento'] = df_due['codigoestablecimiento'].astype(str).str.replace('"', '').str.replace(',', '')
df_due['codigoestablecimiento'] = pd.to_numeric(df_due['codigoestablecimiento'], errors='coerce').fillna(0).astype('int64')

# 3. Reglas de Calidad y Estandarización para 'zona'
df_due['zona'] = df_due['zona'].astype(str).str.strip().str.upper()
df_due['zona'] = df_due['zona'].replace({
    'URBANA,RURAL': 'MIXTA',
    'RURAL,URBANA': 'MIXTA',
    'NAN': 'NO REGISTRA'
})

# 4. Limpieza de texto en atributos descriptivos
for col in ['nombreestablecimiento', 'nombremunicipio']:
    df_due[col] = df_due[col].astype(str).str.replace('"', '').str.strip()

# Exportación del archivo curado
df_due.to_csv(ruta_salida, index=False, encoding='utf-8')
print(f"¡Archivo DUE curado y generado exitosamente en:\n{ruta_salida}")