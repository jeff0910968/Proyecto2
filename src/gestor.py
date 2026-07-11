# Gestor
# Libreria necesaria
import pandas as pd

class GestorPartidos:
    def __init__(self, df):
        self.df = df
    # Devuelve un partido con un id en especifico
    def get_partido(self, id_partido):
        resultado = self.df[self.df["id_partido"] == id_partido]
        if len(resultado) == 0:
            return None
        return resultado.iloc[0]
    # Devuelve todos los partidos donde el equipo jugo como local o visitante
    def get_por_equipo(self, equipo):
        return self.df[
            (self.df["home_team"] == equipo) | (self.df["away_team"] == equipo)
        ]
    # Devuelve los partifos de una edicion del mundial
    def get_por_anio(self, anio):
        return self.df[self.df["anio"] == anio]

    # Todos los partidos jugados en un pais sede
    def get_por_sede(self, pais):
        return self.df[self.df["country"] == pais]

    # Todos los partidos jugados en una ciudad
    def get_por_ciudad(self, ciudad):
        return self.df[self.df["city"] == ciudad]

    # Todos los partidos jugados entre dis equipos
    def get_enfrentamientos(self, equipo_a, equipo_b):
        condicion_1 = (self.df["home_team"] == equipo_a) & (self.df["away_team"] == equipo_b)
        condicion_2 = (self.df["home_team"] == equipo_b) & (self.df["away_team"] == equipo_a)
        return self.df[condicion_1 | condicion_2]

    # Lista de años del Mundial disponibles en el dataframe
    def get_ediciones_disponibles(self):
        anios = self.df["anio"].unique()
        anios.sort()
        return list(anios)

    # Todos los equipos en el dataframe
    def get_equipos_participantes(self):
        equipos = pd.concat([self.df["home_team"], self.df["away_team"]]).unique()
        equipos.sort()
        return list(equipos)

    # Calcula el porcentaje de victorias locales, visitantes y empates
    def ventaja_local(self):
        total = len(self.df)
        victorias_local = (self.df["home_score"] > self.df["away_score"]).sum()
        victorias_visitante = (self.df["home_score"] < self.df["away_score"]).sum()
        empates = (self.df["home_score"] == self.df["away_score"]).sum()
        return {
            "total_partidos": total,
            "pct_victorias_local": round(100 * victorias_local / total, 2),
            "pct_victorias_visitante": round(100 * victorias_visitante / total, 2),
            "pct_empates": round(100 * empates / total, 2),
        }

    #Devuleve los partidos con mas goles
    def get_maximos_goleadores_partido(self, top=10):
        return self.df.sort_values("total_goles", ascending=False).head(top)