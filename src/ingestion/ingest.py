import pandas as pd
import urllib.request
import os

# URLs oficiales
URL_DATOS = "http://kdd.ics.uci.edu/databases/kddcup99/kddcup.data_10_percent.gz"
URL_NOMBRES = "http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names"

DIR_DESTINO = "data/raw"
ARCHIVO_CSV = os.path.join(DIR_DESTINO, "kddcup_10_percent.csv")

def descargar_con_headers(url, ruta_salida):
    """Descarga un archivo simulando un navegador para evitar el error HTTP 403"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response, open(ruta_salida, 'wb') as out_file:
        out_file.write(response.read())

def ejecutar_ingesta():
    os.makedirs(DIR_DESTINO, exist_ok=True)
    
    print("Descargando nombres de columnas...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req_nombres = urllib.request.Request(URL_NOMBRES, headers=headers)
    nombres_req = urllib.request.urlopen(req_nombres).read().decode('utf-8')
    
    # Extraer columnas válidas del archivo .names
    columnas = [linea.split(':')[0] for linea in nombres_req.split('\n') if ':' in linea]
    columnas.append('label')

    print("Descargando y descomprimiendo dataset...")
    gz_path = os.path.join(DIR_DESTINO, "kddcup.gz")
    descargar_con_headers(URL_DATOS, gz_path)

    # Pandas procesa la descompresión gzip directamente
    df = pd.read_csv(gz_path, header=None, names=columnas)
    
    df.to_csv(ARCHIVO_CSV, index=False)
    
    if os.path.exists(gz_path):
        os.remove(gz_path)
        
    print(f"Ingesta completada con éxito. Guardado en: {ARCHIVO_CSV}")
    print(f"Filas cargadas: {df.shape[0]} | Columnas: {df.shape[1]}")

if __name__ == "__main__":
    ejecutar_ingesta()