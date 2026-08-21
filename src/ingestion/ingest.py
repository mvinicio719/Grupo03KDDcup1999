import os
import pandas as pd
from sklearn.datasets import fetch_kddcup99

DIR_DESTINO = "data/raw"
ARCHIVO_CSV = os.path.join(DIR_DESTINO, "kddcup_10_percent.csv")

def ejecutar_ingesta():
    os.makedirs(DIR_DESTINO, exist_ok=True)
    
    print("Descargando dataset KDD Cup 1999 mediante Scikit-Learn...")
    
    # Descargar versión reducida del 10% (percent10=True) y decodificar bytes a strings (decode_toks=True)
    dataset = fetch_kddcup99(subset=None, percent10=True, as_frame=True, decode_toks=True)
    
    # Extraer el DataFrame completo con características y columna 'target' / 'labels'
    df = dataset.frame
    
    # Renombrar la última columna a 'label' para estandarizar
    if 'target' in df.columns:
        df = df.rename(columns={'target': 'label'})
    elif 'labels' in df.columns:
        df = df.rename(columns={'labels': 'label'})
    
    # Guardar CSV limpio localmente
    df.to_csv(ARCHIVO_CSV, index=False)
    
    print(f"Ingesta completada con éxito. Guardado en: {ARCHIVO_CSV}")
    print(f"Filas cargadas: {df.shape[0]} | Columnas: {df.shape[1]}")

if __name__ == "__main__":
    ejecutar_ingesta()