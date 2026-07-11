# Eda
# Libreria necesaria
import pandas as pd

class ProceEDA:
    def __init__(self, df):
        self.df = df

    # Quita duplicados o filas con datos vacios
    def limpieza_datos(self):
        df = self.df.copy()
        filas_antes = len(df)
        df = df.drop_duplicates()
        df = df.dropna(subset=["date", "home_team", "away_team", "home_score", "away_score"])
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["home_score"] = df["home_score"].astype(int)
        df["away_score"] = df["away_score"].astype(int)
        df = df.reset_index(drop=True)
        self.df = df
        print("Limpieza completada:", filas_antes, "->", len(df), "filas")
        return self.df

    # Agrega algunas columnas
    def generar_columnas_derivadas(self):
        df = self.df.copy()
        df["anio"] = df["date"].dt.year
        df["total_goles"] = df["home_score"] + df["away_score"]
        df["diferencia_goles"] = (df["home_score"] - df["away_score"]).abs()
        ganadores = []
        for i in range(len(df)):
            local = df["home_score"].iloc[i]
            visitante = df["away_score"].iloc[i]
            if local > visitante:
                ganadores.append("Local")
            elif local < visitante:
                ganadores.append("Visitante")
            else:
                ganadores.append("Empate")
        df["ganador"] = ganadores
        self.df = df
        print("Columnas agregadas: anio, total_goles, diferencia_goles, ganador")
        return self.df
    # Estadisticas basicas
    def resumen_descriptivo(self):
        columnas = ["home_score", "away_score", "total_goles", "diferencia_goles"]
        return self.df[columnas].describe()

    # Matriz de correlacion
    def matriz_correlacion(self):
        columnas = ["home_score", "away_score", "total_goles", "diferencia_goles", "anio"]
        return self.df[columnas].corr()

    # Outliers
    def detectar_outliers(self, columna="total_goles"):
        q1 = self.df[columna].quantile(0.25)
        q3 = self.df[columna].quantile(0.75)
        rango = q3 - q1
        limite_inferior = q1 - 1.5 * rango
        limite_superior = q3 + 1.5 * rango
        return self.df[(self.df[columna] < limite_inferior) | (self.df[columna] > limite_superior)]

    # Agrupacion de partidos por año y calcula el total y promedio de goles
    def goles_por_edicion(self):
        anios = sorted(self.df["anio"].unique())
        filas = []
        for anio in anios:
            partidos_anio = self.df[self.df["anio"] == anio]
            cantidad_partidos = len(partidos_anio)
            total_goles = partidos_anio["total_goles"].sum()
            promedio_goles = round(total_goles / cantidad_partidos, 2)
            filas.append({
                "anio": anio,
                "partidos": cantidad_partidos,
                "total_goles": total_goles,
                "promedio_goles": promedio_goles,
            })
        return pd.DataFrame(filas)

    # Calcula victorias, empates, derrotas y diferencias de goles por cada equipo
    def resultados_por_equipo(self):
        equipos = pd.concat([self.df["home_team"], self.df["away_team"]]).unique()
        filas = []
        for equipo in equipos:
            local = self.df[self.df["home_team"] == equipo]
            visitante = self.df[self.df["away_team"] == equipo]
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
    # Revisa si el anfitrion gano mas de la mitad de sus partidos
    def anfitrion_gana_mas(self):
        filas = []
        anios = sorted(self.df["anio"].unique())
        for anio in anios:
            partidos_edicion = self.df[self.df["anio"] == anio]
            pais_sede = partidos_edicion["country"].mode()
            if len(pais_sede) == 0:
                continue
            pais_sede = pais_sede.iloc[0]
            jugados = partidos_edicion[
                (partidos_edicion["home_team"] == pais_sede) | (partidos_edicion["away_team"] == pais_sede)
            ]
            if len(jugados) == 0:
                continue
            victorias = 0
            for i in range(len(jugados)):
                fila = jugados.iloc[i]
                if fila["home_team"] == pais_sede and fila["home_score"] > fila["away_score"]:
                    victorias += 1
                elif fila["away_team"] == pais_sede and fila["away_score"] > fila["home_score"]:
                    victorias += 1
            filas.append({
                "anio": anio,
                "pais_sede": pais_sede,
                "partidos_jugados_por_sede": len(jugados),
                "victorias_sede": victorias,
                "pct_victorias_sede": round(100 * victorias / len(jugados), 2),
            })
        return pd.DataFrame(filas)