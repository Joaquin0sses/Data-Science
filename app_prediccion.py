import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Carga tu modelo entrenado (ajusta el nombre si es necesario)

model = joblib.load('modelo_entrenado_XGBoost.pkl')  # Guarda tu modelo con joblib.dump(model, 'modelo_entrenado.pkl')

# Carga las columnas usadas para entrenamiento
with open('columnas_modelo.txt', 'r') as f:
    columnas_modelo = f.read().splitlines()

st.title("Predicción de Abandono Escolar")

# Entradas del usuario
COD_DEPE2 = st.selectbox("Dependencia", ['1', '2', '3', '4'])
RURAL_RBD = st.selectbox("Ruralidad", ['0', '1'])
ESTADO_ESTAB = st.selectbox("Estado Establecimiento", ['1', '2', '3', '4'])
COD_GRADO = st.selectbox("Grado", ['1', '2', '3', '4'])
COD_JOR = st.selectbox("Jornada", ['1', '2', '3'])
GEN_ALU = st.selectbox("Género", ['1', '2'])
EDAD_ALU = st.number_input("Edad Alumno", min_value=5, max_value=25, value=15)
PROM_GRAL = st.number_input("Promedio General", min_value=10.0, max_value=70.0, value=50.0)
ASISTENCIA = st.number_input("Asistencia (%)", min_value=0.0, max_value=100.0, value=90.0)

# Construir DataFrame de entrada
input_dict = {
    'COD_DEPE2': [COD_DEPE2],
    'RURAL_RBD': [RURAL_RBD],
    'ESTADO_ESTAB': [ESTADO_ESTAB],
    'COD_GRADO': [COD_GRADO],
    'COD_JOR': [COD_JOR],
    'GEN_ALU': [GEN_ALU],
    'EDAD_ALU': [EDAD_ALU],
    'PROM_GRAL': [PROM_GRAL],
    'ASISTENCIA': [ASISTENCIA]
}
df_input = pd.DataFrame(input_dict)

# Convertir variables categóricas a string y aplicar get_dummies
categ_vars = ['COD_DEPE2', 'RURAL_RBD', 'ESTADO_ESTAB', 'COD_GRADO', 'COD_JOR', 'GEN_ALU']
df_input[categ_vars] = df_input[categ_vars].astype(str)
df_input = pd.get_dummies(df_input, columns=categ_vars, drop_first=True)

# Asegurar que las columnas coincidan con las del modelo
for col in columnas_modelo:
    if col not in df_input.columns:
        df_input[col] = 0
df_input = df_input[columnas_modelo]

if st.button("Predecir"):
    
    proba = model.predict_proba(df_input)[0][1]
    pred = model.predict(df_input)[0]
    st.write(f"**Probabilidad de abandono:** {proba:.2%}")
    st.write(f"**Predicción:** {'Abandona' if pred == 1 else 'No abandona'}")