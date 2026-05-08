import os
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Team Vibe Pro", page_icon="📈")

DATA_FILE = "vibes_equipo.csv"
HUMOR_OPTIONS = ["🤩 Increíble", "☕ Café", "😴 Sueño", "🤯 Caos"]


def guardar_datos(nuevo_registro: dict) -> None:
    df_nuevo = pd.DataFrame([nuevo_registro])
    if not os.path.isfile(DATA_FILE):
        df_nuevo.to_csv(DATA_FILE, index=False)
    else:
        df_nuevo.to_csv(DATA_FILE, mode="a", index=False, header=False)


def cargar_datos() -> pd.DataFrame:
    if os.path.isfile(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["FechaHora", "Nombre", "Humor", "Energia"])


st.title("🚀 Team Vibe Dashboard Permanente")
st.markdown("Registra el pulso del equipo y mantenlo guardado en CSV.")

with st.sidebar:
    st.header("Registra tu estado")
    nombre = st.text_input("Nombre")
    humor = st.selectbox("Humor", HUMOR_OPTIONS)
    energia = st.slider("Energía", 0, 100, 50)

    if st.button("Enviar Vibe"):
        if nombre.strip():
            datos_vibe = {
                "FechaHora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nombre": nombre.strip(),
                "Humor": humor,
                "Energia": energia,
            }
            guardar_datos(datos_vibe)
            st.success("¡Datos guardados en el CSV!")
            st.balloons()
        else:
            st.warning("Por favor, escribe tu nombre.")

    if st.button("Resetear datos"):
        if os.path.isfile(DATA_FILE):
            os.remove(DATA_FILE)
            st.success("CSV eliminado. Dashboard reiniciado.")
        else:
            st.info("No hay archivo CSV para eliminar.")

df = cargar_datos()

if not df.empty:
    st.subheader("Análisis del equipo")
    col1, col2 = st.columns(2)
    col1.metric("Total registros", len(df))
    col2.metric("Energía media", f"{int(df['Energia'].mean())}%")

    st.bar_chart(data=df, x="Nombre", y="Energia")

    with st.expander("Ver tabla de datos completa"):
        st.dataframe(df[["FechaHora", "Nombre", "Humor", "Energia"]], use_container_width=True)
else:
    st.info("Aún no hay datos guardados. ¡Sé la primera!")