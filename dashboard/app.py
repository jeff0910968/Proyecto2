# Librerias necesarias
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Hacemos que src/ sea importable, sin importar desde dónde se lance streamlit ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..")
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
sys.path.append(SRC_DIR)

from ingesta import CargaDatos
from eda import ProceEDA
from gestor import GestorPartidos
from visualizacion import Visualizador

RUTA_RAW = os.path.join(PROJECT_ROOT, "data", "raw")
RUTA_PROCESSED = os.path.join(PROJECT_ROOT, "data", "processed")
ARCHIVO_PROCESADO = os.path.join(RUTA_PROCESSED, "partidos-mundial-procesado.csv")
ARCHIVO_RAW = os.path.join(RUTA_RAW, "partidos-mundial.csv")

@st.cache_data
def cargar_datos():
    if os.path.exists(ARCHIVO_PROCESADO):
        return pd.read_csv(ARCHIVO_PROCESADO)
    if os.path.exists(ARCHIVO_RAW):
        datos_crudos = pd.read_csv(ARCHIVO_RAW)
    else:
        cargador = CargaDatos(ruta_raw=RUTA_RAW, ruta_processed=RUTA_PROCESSED)
        cargador.descargar_csv(destino=os.path.join(RUTA_RAW, "results.csv"))
        cargador.filtrar_mundial()
        cargador.guardar_raw()
        datos_crudos = cargador.datos
    eda_temp = ProceEDA(datos_crudos)
    eda_temp.limpieza_datos()
    eda_temp.crear_columnas_derivadas()
    datos_listos = eda_temp.obtener_datos()
    os.makedirs(RUTA_PROCESSED, exist_ok=True)
    datos_listos.to_csv(ARCHIVO_PROCESADO, index=False)
    return datos_listos

#  Renderiza la figura activa de matplotlib en Streamlit y la limpia
def mostrar_figura():
    st.pyplot(plt.gcf())
    plt.clf()
    plt.close("all")

# Configuración de la página
st.set_page_config(page_title="World Cup Insights", page_icon="🏆", layout="wide")
datos = cargar_datos()
eda = ProceEDA(datos)
gestor = GestorPartidos(datos)
visualizador = Visualizador(datos)
st.title("World Cup")
st.caption("Análisis exploratorio y visualización de partidos de la Copa Mundial de la FIFA")

# Sidebar: filtros globales
st.sidebar.header("Filtros")
equipos_disponibles = ["Todos"] + list(gestor.get_equipos_participantes())
equipo_sel = st.sidebar.selectbox("Equipo", equipos_disponibles)
ediciones_disponibles = ["Todas"] + [str(a) for a in gestor.get_ediciones_disponibles()]
anio_sel = st.sidebar.selectbox("Edición del Mundial", ediciones_disponibles)
datos_filtrados = datos.copy()
if equipo_sel != "Todos":
    datos_filtrados = gestor.get_por_equipo(equipo_sel)
if anio_sel != "Todas":
    datos_filtrados = datos_filtrados[datos_filtrados["anio"] == int(anio_sel)]

# Tabs principales
tab_resumen, tab_consultas, tab_visualizaciones = st.tabs(
    ["Resumen", "Consultas", "Visualizaciones"]
)

# TAB 1: Resumen general
with tab_resumen:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Partidos totales", len(datos))
    col2.metric("Ediciones", datos["anio"].nunique())
    col3.metric("Equipos distintos", len(gestor.get_equipos_participantes()))
    col4.metric("Goles totales", int(datos["total_goles"].sum()))
    st.subheader("Resumen estadístico descriptivo")
    st.dataframe(eda.resumen_descriptivo(), use_container_width=True)
    st.subheader("Vista rápida del dataset")
    st.dataframe(datos.head(20), use_container_width=True)

# TAB 2: Consultas con GestorPartidos
with tab_consultas:
    st.subheader("Partidos según los filtros seleccionados")
    columnas_mostrar = [
        "date", "home_team", "away_team", "home_score", "away_score",
        "city", "country", "anio", "ganador",
    ]
    st.dataframe(datos_filtrados[columnas_mostrar], use_container_width=True)
    st.caption(f"{len(datos_filtrados)} partidos encontrados con los filtros actuales")
    st.divider()
    st.subheader("Enfrentamientos históricos entre dos selecciones")
    col_a, col_b = st.columns(2)
    equipo_a = col_a.selectbox("Equipo A", gestor.get_equipos_participantes(), key="equipo_a")
    equipo_b = col_b.selectbox("Equipo B", gestor.get_equipos_participantes(), key="equipo_b")
    if equipo_a and equipo_b:
        enfrentamientos = gestor.get_enfrentamientos(equipo_a, equipo_b)
        if enfrentamientos.empty:
            st.info(f"{equipo_a} y {equipo_b} nunca se han enfrentado en la Copa Mundial.")
        else:
            st.dataframe(
                enfrentamientos[["date", "home_team", "away_team", "home_score", "away_score", "anio"]],
                use_container_width=True,
            )
    st.divider()
    st.subheader("Top partidos con más goles")
    top_n = st.slider("Cantidad de partidos a mostrar", min_value=3, max_value=20, value=10)
    top_goleadores = gestor.get_maximos_goleadores_partido(top=top_n)
    st.dataframe(
        top_goleadores[["date", "home_team", "away_team", "home_score", "away_score", "total_goles"]],
        use_container_width=True,
    )

# TAB 3: Visualizaciones
with tab_visualizaciones:
    st.subheader("¿Qué distribución tienen los goles por partido?")
    visualizador.histograma_goles()
    mostrar_figura()
    st.subheader("¿En qué edición se metieron más goles?")
    visualizador.goles_por_edicion(eda.goles_promedio_por_edicion())
    mostrar_figura()
    st.subheader("¿Cómo se correlacionan las variables numéricas?")
    visualizador.mapa_calor_correlacion(eda.matriz_correlacion())
    mostrar_figura()
    st.subheader("¿Qué selecciones tienen la mejor diferencia de goles histórica?")
    serie_diferencia = eda.resultados_por_equipo().set_index("equipo")["diferencia_gol"]
    visualizador.top_equipos_diferencia_goles(serie_diferencia, top_n=10)
    mostrar_figura()