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

# Diccionarios para mostrar opciones descriptivas
depe_dict = {'Municipal': '1', 'Particular subvencionado': '2', 'Particular pagado': '3', 'Administración delegada': '4'}
rural_dict = {'Urbano': '0', 'Rural': '1'}
estado_estab_dict = {'Vigente': '1', 'Cerrado': '2', 'En receso': '3', 'Sin actividad': '4'}
grado_dict = {
    '1° Básico': '1',
    '2° Básico': '2',
    '3° Básico': '3',
    '4° Básico': '4',
    '5° Básico': '5',
    '6° Básico': '6',
    '7° Básico': '7',
    '8° Básico': '8',
    '1° Medio': '9',
    '2° Medio': '10',
    '3° Medio': '11',
    '4° Medio': '12'
}
jor_dict = {'Mañana': '1', 'Tarde': '2', 'Vespertina': '3'}
gen_dict = {'Masculino': '1', 'Femenino': '2'}

# Entradas del usuario con opciones descriptivas
COD_DEPE2 = depe_dict[st.selectbox("Dependencia", list(depe_dict.keys()))]
RURAL_RBD = rural_dict[st.selectbox("Ruralidad", list(rural_dict.keys()))]
ESTADO_ESTAB = estado_estab_dict[st.selectbox("Estado Establecimiento", list(estado_estab_dict.keys()))]
COD_GRADO = grado_dict[st.selectbox("Grado", list(grado_dict.keys()))]
COD_JOR = jor_dict[st.selectbox("Jornada", list(jor_dict.keys()))]
GEN_ALU = gen_dict[st.selectbox("Género", list(gen_dict.keys()))]
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