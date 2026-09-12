import os
import sys

# Configuración de exclusiones
EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', 'env', 'node_modules', '.idea', '.vscode', 'data'}
EXCLUDE_EXT = {'.pdf', '.png', '.jpg', '.jpeg', '.ico', '.csv', '.xlsx', '.pyc', '.zip', '.txt'}

def generar_estructura_completa(ruta_base='.', archivo_salida='contexto_completo.txt'):
    with open(archivo_salida, 'w', encoding='utf-8') as out:
        out.write("# ESTRUCTURA Y CONTEXTO COMPLETO DEL PROYECTO EDUDATACO\n")
        out.write("="*50 + "\n\n")
        
        # 1. Árbol de Directorios
        out.write("## 1. ÁRBOL DE DIRECTORIOS\n")
        for root, dirs, files in os.walk(ruta_base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            nivel = root.replace(ruta_base, '').count(os.sep)
            sangria = ' ' * 4 * nivel
            out.write(f"{sangria}{os.path.basename(root)}/\n")
            sub_sangria = ' ' * 4 * (nivel + 1)
            for file in files:
                if not any(file.endswith(ext) for ext in EXCLUDE_EXT) and file != archivo_salida:
                    out.write(f"{sub_sangria}{file}\n")
        
        out.write("\n" + "="*50 + "\n\n")
        
        # 2. Contenido SIN truncar
        out.write("## 2. CÓDIGO Y CONTENIDO DE ARCHIVOS CLAVE (COMPLETO)\n")
        for root, dirs, files in os.walk(ruta_base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                # Incluimos los archivos clave para la revisión
                if file.endswith(('.py', '.html', '.css', '.md')) and file not in [archivo_salida, os.path.basename(sys.argv[0])]:
                    ruta_archivo = os.path.join(root, file)
                    out.write(f"\n### Archivo: {ruta_archivo}\n```\n")
                    try:
                        with open(ruta_archivo, 'r', encoding='utf-8') as f:
                            # Se escribe el 100% del archivo sin cortes
                            out.write(f.read())
                    except Exception as e:
                        out.write(f"[Error leyendo el archivo: {e}]\n")
                    out.write("\n```\n")

if __name__ == '__main__':
    generar_estructura_completa()
    print("Archivo 'contexto_completo.txt' generado exitosamente sin truncamiento.")