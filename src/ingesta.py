# Ingesta
# La clase de CargarDatos, se encarga de descargar el CSV desde una url publica
# Filtra solo partidos de la copa mundial y verifica los datos filtrados

# Librerias necesarias
import os
import pandas as pd
import requests

# Primero se crea la clase
class CargarDatos:
    URL_DATASET = "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
    TORNEO = "FIFA World Cup"
    def __init__(self, ruta_raw="data/raw/partidos-mundial.csv", ruta_processed="data/processed"):
        self.ruta_raw = ruta_raw
        self.ruta_processed = ruta_processed
        self.df_raw = None
        self.df_filtrado = None

    # Descarga el csv completo
    def descargar_datos(self):
        respuesta = requests.get(self.URL_DATASET)
        respuesta.raise_for_status()
        os.makedirs("data/raw", exist_ok=True)
        ruta_temporal = "data/raw/results_completo.csv"
        with open(ruta_temporal, "wb") as archivo:
            archivo.write(respuesta.content)
        self.df_raw = pd.read_csv(ruta_temporal)
        print("Partidos descargados en total:", len(self.df_raw))
        return self.df_raw

    # Se filtran los partidos que solo sean de la copa mundial
    def filtrar_mundial(self):
        df = self.df_raw[self.df_raw["tournament"] == self.TORNEO].copy()
        df = df.dropna(subset=["home_score", "away_score"]) # Se quitan partidos que no tengan marcador
        df = df.reset_index(drop=True)
        df.insert(0, "id_partido", range(1, len(df) + 1))
        self.df_filtrado = df
        print("Partidos de Copa Mundial encontrados:", len(df))
        return df

    # Validar que las columnas mas importantes esten en el dataset
    def validar_datos(self):
        df = self.df_filtrado
        if df is None or len(df) == 0:
            print("Error: no hay datos para validar.")
            return False
        columnas_necesarias = ["date", "home_team", "away_team", "home_score", "away_score"]
        for columna in columnas_necesarias:
            if columna not in df.columns:
                print("Error: falta la columna", columna)
                return False
        if (df["home_score"] < 0).any() or (df["away_score"] < 0).any():
            print("Error: hay marcadores negativos.")
            return False
        print("Los datos son válidos.")
        return True

    # Guarda el CSV filtrado
    def guardar_raw(self):
        os.makedirs("data/raw", exist_ok=True)
        self.df_filtrado.to_csv(self.ruta_raw, index=False)
        print("Archivo guardado en", self.ruta_raw)

    # Guarda el dataframe procesado
    def guardar_procesado(self, df, nombre_archivo="partidos-mundial-procesado"):
        os.makedirs(self.ruta_processed, exist_ok=True)
        ruta_csv = self.ruta_processed + "/" + nombre_archivo + ".csv"
        df.to_csv(ruta_csv, index=False)
        print("Archivo guardado en", ruta_csv)

    # Carga el archivo en raw existente
    def cargar_raw_existente(self):
        self.df_filtrado = pd.read_csv(self.ruta_raw)
        print("Datos cargados desde archivo existente:", len(self.df_filtrado), "partidos.")
        return self.df_filtrado

    # Ejecuta todo lo anterior
    def ejecutar_pipeline_ingesta(self):
        self.descargar_datos()
        self.filtrar_mundial()
        if self.validar_datos():
            self.guardar_raw()
        return self.df_filtrado