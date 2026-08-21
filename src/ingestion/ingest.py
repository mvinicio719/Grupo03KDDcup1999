import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

DIR_DESTINO = "data/raw"
ARCHIVO_CSV = os.path.join(DIR_DESTINO, "kddcup_10_percent.csv")

def ejecutar_ingesta():
    os.makedirs(DIR_DESTINO, exist_ok=True)
    
    print("Descargando dataset KDD Cup 1999 desde la API de UCI...")
    
    # Cargar el dataset ID 130 (KDD Cup 1999) mediante el paquete oficial ucimlrepo
    kdd_cup_1999 = fetch_ucirepo(id=130)
    
    # Extraer variables (X) y objetivo (y)
    X = kdd_cup_1999.data.features
    y = kdd_cup_1999.data.targets
    
    # Unir en un solo DataFrame
    df = pd.concat([X, y], axis=1)
    
    # Guardar CSV localmente en la carpeta data/raw
    df.to_csv(ARCHIVO_CSV, index=False)
    
    print(f"Ingesta completada con éxito. Guardado en: {ARCHIVO_CSV}")
    print(f"Filas cargadas: {df.shape[0]} | Columnas: {df.shape[1]}")

if __name__ == "__main__":
    ejecutar_ingesta()