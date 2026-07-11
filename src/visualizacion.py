# Visualizacion
# Librerias necesarias
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

class Visualizar:
    def __init__(self, df, carpeta_salida="data/processed/graficos"):
        self.df = df
        self.carpeta_salida = carpeta_salida
        os.makedirs(self.carpeta_salida, exist_ok=True)

    def guardar(self, fig, nombre):
        ruta = self.carpeta_salida + "/" + nombre
        fig.savefig(ruta, bbox_inches="tight")
        print("Gráfico guardado en", ruta)

    # Linea de tiempo con el promedio de goles por partido
    def goles_promedio_por_edicion(self):
        anios = sorted(self.df["anio"].unique())
        promedios = []
        for anio in anios:
            partidos_anio = self.df[self.df["anio"] == anio]
            promedio = partidos_anio["total_goles"].mean()
            promedios.append(promedio)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(anios, promedios, marker="o")
        ax.set_title("Promedio de goles por partido en cada Mundial")
        ax.set_xlabel("Año")
        ax.set_ylabel("Promedio de goles")
        self.guardar(fig, "01_goles_promedio_por_edicion.png")

    # Grafico de barras con la cantidad de partidos ganados por el local, visitante o empatados
    def ventaja_local_barras(self):
        conteo = self.df["ganador"].value_counts()
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(conteo.index, conteo.values, color=["green", "red", "gray"])
        ax.set_title("Resultados históricos en la Copa Mundial")
        ax.set_xlabel("Resultado")
        ax.set_ylabel("Cantidad de partidos")
        self.guardar(fig, "02_distribucion_resultados.png")

    # Grafico de barras con los equipos de mejor diferencia de gol historica
    def top_diferencia_gol(self, resultados_por_equipo, top=15):
        datos = resultados_por_equipo.head(top)
        fig, ax = plt.subplots(figsize=(9, 8))
        ax.barh(datos["equipo"], datos["diferencia_gol"], color="steelblue")
        ax.invert_yaxis()
        ax.set_title("Top equipos por diferencia de gol en Mundiales")
        ax.set_xlabel("Diferencia de gol")
        self.guardar(fig, "03_top_diferencia_gol.png")

    # Heatmap con la correlacion entre variables numericas
    def heatmap_correlacion(self, matriz_correlacion):
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.heatmap(matriz_correlacion, annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Matriz de correlación")
        self.guardar(fig, "04_heatmap_correlacion.png")

    # Histograma con la cantidad de goles totales por partido
    def histograma_goles_totales(self):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(self.df["total_goles"], bins=range(0, self.df["total_goles"].max() + 2), color="orange")
        ax.set_title("Distribución de goles totales por partido")
        ax.set_xlabel("Goles totales")
        ax.set_ylabel("Cantidad de partidos")
        self.guardar(fig, "05_histograma_goles_totales.png")

    # Barras con el porcentaje de victorias del pais anfitrion
    def desempeno_anfitrion(self, df_anfitrion):
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_anfitrion["anio"].astype(str), df_anfitrion["pct_victorias_sede"], color="purple")
        ax.axhline(50, color="black", linestyle="--")
        ax.set_title("Porcentaje de victorias del país anfitrión por edición")
        ax.set_xlabel("Año")
        ax.set_ylabel("% de victorias")
        plt.xticks(rotation=45)
        self.guardar(fig, "07_desempeno_anfitrion.png")