# Eda
# Librerias necesarias
import pandas as pd

class ProceEDA:
    def __init__(self, datos):
        self.datos = datos.copy()

    # Retorna la cantidad de valores nulos
    def verificar_nulos(self):
        nulos = self.datos.isnull().sum()
        return nulos[nulos > 0].sort_values(ascending=False)

    # Elimina duplicados, quita nulos y trabaja con la fecha
    def limpieza_datos(self):
        self.datos = self.datos.drop_duplicates()
        self.datos = self.datos.dropna(subset=["home_score", "away_score"])
        self.datos["date"] = pd.to_datetime(self.datos["date"], errors="coerce")
        self.datos["home_score"] = self.datos["home_score"].astype(int)
        self.datos["away_score"] = self.datos["away_score"].astype(int)
        return self.datos

    # Agrega nuevas columnas
    def crear_columnas_derivadas(self):
        self.datos["anio"] = self.datos["date"].dt.year
        self.datos["total_goles"] = self.datos["home_score"] + self.datos["away_score"]
        self.datos["diferencia_goles"] = (self.datos["home_score"] - self.datos["away_score"]).abs()
        self.datos["ganador"] = self.datos.apply(self._definir_ganador, axis=1)
        return self.datos

    # Se define el ganador de un partido
    def _definir_ganador(self, fila):
        if fila["home_score"] > fila["away_score"]:
            return "Local"
        elif fila["home_score"] < fila["away_score"]:
            return "Visitante"
        else:
            return "Empate"

    # Resumen estadistico
    def resumen_descriptivo(self):
        return self.datos.describe()

    # Matriz de correlacion
    def matriz_correlacion(self):
        columnas_numericas = self.datos.select_dtypes(include="number")
        return columnas_numericas.corr()

    # Outliers
    def detectar_outliers(self, columna):
        q1 = self.datos[columna].quantile(0.25)
        q3 = self.datos[columna].quantile(0.75)
        iqr = q3 - q1
        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr
        return self.datos[(self.datos[columna] < limite_inferior) | (self.datos[columna] > limite_superior)]

    # Promedio de goles totales por partido, lo agrupa por año de mundial
    def goles_promedio_por_edicion(self):
        return self.datos.groupby("anio")["total_goles"].mean().sort_values(ascending=False)

    # Calcula victorias, empates, derrotas y diferencias de goles por cada equipo
    def resultados_por_equipo(self):
        equipos = pd.concat([self.datos["home_team"], self.datos["away_team"]]).unique()
        filas = []
        for equipo in equipos:
            local = self.datos[self.datos["home_team"] == equipo]
            visitante = self.datos[self.datos["away_team"] == equipo]
            victorias = (local["home_score"] > local["away_score"]).sum() + \
                        (visitante["away_score"] > visitante["home_score"]).sum()
            empates = (local["home_score"] == local["away_score"]).sum() + \
                      (visitante["away_score"] == visitante["home_score"]).sum()
            derrotas = (local["home_score"] < local["away_score"]).sum() + \
                       (visitante["away_score"] < visitante["home_score"]).sum()
            goles_favor = local["home_score"].sum() + visitante["away_score"].sum()
            goles_contra = local["away_score"].sum() + visitante["home_score"].sum()
            filas.append({
                "equipo": equipo,
                "partidos_jugados": len(local) + len(visitante),
                "victorias": victorias,
                "empates": empates,
                "derrotas": derrotas,
                "goles_favor": goles_favor,
                "goles_contra": goles_contra,
                "diferencia_gol": goles_favor - goles_contra,
            })
        resultado = pd.DataFrame(filas)
        return resultado.sort_values("diferencia_gol", ascending=False).reset_index(drop=True)

    # Retorna el procesado
    def obtener_datos(self):
        return self.datos