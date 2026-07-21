# Ingesta
# La clase de CargarDatos, se encarga de descargar el CSV desde una url publica
# Filtra solo partidos de la copa mundial y verifica los datos filtrados
# Librerias necesarias
import os
import pandas as pd
import urllib.request

class CargaDatos:
    URL_CSV = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    def __init__(self, ruta_raw="data/raw", ruta_processed="data/processed"):
        self.ruta_raw = ruta_raw
        self.ruta_processed = ruta_processed
        self.datos = None
    # Descarga el CSV original
    def descargar_csv(self, destino="data/raw/results.csv", url=None):
        urllib.request.urlretrieve(url or self.URL_CSV, destino)
        self.datos = pd.read_csv(destino)
        print(f"Archivo descargado en: {destino}")
        return self.datos
    #Filtra solo los partidos del mundial
    def filtrar_mundial(self, torneo="FIFA World Cup"):
        self.datos = self.datos[self.datos["tournament"] == torneo]
        self.datos = self.datos.dropna(subset=["home_score", "away_score"])
        return self.datos
    # Guarda los partidos del mundiall sin procesar
    def guardar_raw(self, nombre_archivo="partidos-mundial.csv"):
        ruta = os.path.join(self.ruta_raw, nombre_archivo)
        self.datos.to_csv(ruta, index=False)
        print(f"Datos guardados en: {ruta}")
        return ruta
    # Guarda el dataset procesado
    def guardar_processed(self, nombre_archivo="partidos-mundial-procesado.csv"):
        ruta = os.path.join(self.ruta_processed, nombre_archivo)
        self.datos.to_csv(ruta, index=False)
        print(f"Datos guardados en: {ruta}")
        return ruta