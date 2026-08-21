import pandas as pd
import urllib.request
import gzip
import os

# 1. Definir URLs oficiales y rutas
URL_DATOS = "http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz"
URL_NOMBRES = "http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names"

DIR_DESTINO = "data/raw"
ARCHIVO_CSV = os.path.join(DIR_DESTINO, "kddcup_10_percent.csv")

def ejecutar_ingesta():
    # Crear carpeta data/raw si no existe
    os.makedirs(DIR_DESTINO, exist_ok=True)
    
    print(" Descargando nombres de columnas...")
    nombres_req = urllib.request.urlopen(URL_NOMBRES).read().decode('utf-8')
    # Extraer los nombres de las columnas del archivo .names
    columnas = [linea.split(':')[0] for linea in nombres_req.split('\n') if ':' in linea]
    columnas.append('label') # Agregar la columna objetivo (si es ataque o normal)

    print(" Descargando y descomprimiendo dataset...")
    gz_path = os.path.join(DIR_DESTINO, "kddcup.gz")
    urllib.request.urlretrieve(URL_DATOS, gz_path)

    # Leer el archivo .gz comprimido directamente con Pandas
    df = pd.read_csv(gz_path, header=None, names=columnas)
    
    # Guardar como CSV limpio localmente
    df.to_csv(ARCHIVO_CSV, index=False)
    
    # Borrar el .gz temporal
    if os.path.exists(gz_path):
        os.remove(gz_path)
        
    print(f" Ingesta completada con éxito. Guardado en: {ARCHIVO_CSV}")
    print(f" Filas cargadas: {df.shape[0]} | Columnas: {df.shape[1]}")

if __name__ == "__main__":
    ejecutar_ingesta()