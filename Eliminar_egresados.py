import pandas as pd

# Ruta del archivo unificado
input_file = 'Datasets/Reducidos/dataset_unificado3.csv'
output_file = 'Datasets/Reducidos/dataset_unificado3_sin_egresados.csv'

# Leer el dataset
df = pd.read_csv(input_file, delimiter=';', dtype=str)

# Eliminar filas donde estado == 'egresado'
df_filtrado = df[df['estado'] != 'egresado']

# Guardar el resultado
df_filtrado.to_csv(output_file, index=False, sep=';')
print(f"Archivo guardado sin egresados: {output_file}")