# Gestor
# Libreria necesaria
import pandas as pd

class GestorPartidos:
    def __init__(self, datos):
        self.datos = datos

    # Devuelve todos los partidos donde el equipo jugo como local o visitante
    def get_por_equipo(self, equipo):
        return self.datos[
            (self.datos["home_team"] == equipo) | (self.datos["away_team"] == equipo)
        ]
    # Devuelve los partidos de una edicion del mundial
    def get_por_anio(self, anio):
        return self.datos[self.datos["anio"] == anio]

    # Todos los partidos jugados entre dos equipos
    def get_enfrentamientos(self, equipo_a, equipo_b):
        condicion_1 = (self.datos["home_team"] == equipo_a) & (self.datos["away_team"] == equipo_b)
        condicion_2 = (self.datos["home_team"] == equipo_b) & (self.datos["away_team"] == equipo_a)
        return self.datos[condicion_1 | condicion_2]

    # Lista de años del Mundial disponibles en el dataframe
    def get_ediciones_disponibles(self):
        anios = self.datos["anio"].unique()
        anios.sort()
        return list(anios)

    # Todos los equipos en el dataframe
    def get_equipos_participantes(self):
        equipos = pd.concat([self.datos["home_team"], self.datos["away_team"]]).unique()
        return list(equipos)

    #Devuleve los partidos con mas goles
    def get_maximos_goleadores_partido(self, top=10):
        return self.datos.sort_values("total_goles", ascending=False).head(top)