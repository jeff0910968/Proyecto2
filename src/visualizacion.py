# Visualizacion
# Librerias necesarias
import matplotlib.pyplot as plt
import seaborn as sns

class Visualizador:
    def __init__(self, datos):
        self.datos = datos

    # Histograma del total de goles por partido
    def histograma_goles(self, guardar_como=None):
        plt.figure(figsize=(8, 5))
        sns.histplot(self.datos["total_goles"], bins=range(0, self.datos["total_goles"].max() + 2), kde=False)
        plt.title("Distribución del total de goles por partido")
        plt.xlabel("Goles totales en el partido")
        plt.ylabel("Cantidad de partidos")

    # Grafico de barras
    def goles_por_edicion(self, promedio_por_anio):
        plt.figure(figsize=(10, 5))
        promedio_por_anio.sort_index().plot(kind="bar", color="steelblue")
        plt.title("Promedio de goles por partido según edición del Mundial")
        plt.xlabel("Año del Mundial")
        plt.ylabel("Promedio de goles por partido")

    # Heatmap de la matriz de correlacion
    def mapa_calor_correlacion(self, matriz_correlacion):
        plt.figure(figsize=(7, 6))
        sns.heatmap(matriz_correlacion, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Matriz de correlación de variables numéricas")

    # Grafico de barras horizontales
    def top_equipos_diferencia_goles(self, serie_diferencia, top_n=10):
        top = serie_diferencia.head(top_n)
        plt.figure(figsize=(8, 6))
        top.sort_values().plot(kind="barh", color="goldenrod")
        plt.title(f"Top {top_n} selecciones con mejor diferencia de goles histórica")
        plt.xlabel("Diferencia de goles (a favor - en contra)")