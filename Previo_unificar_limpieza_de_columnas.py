import os
import glob
import pandas as pd

# Columnas a conservar
columnas_usar = [
    'AGNO', 'NOM_COM_RBD', 'COD_DEPE2', 'RURAL_RBD', 'ESTADO_ESTAB',
    'COD_ENSE', 'COD_ENSE2', 'COD_GRADO', 'COD_JOR', 'GEN_ALU',
    'EDAD_ALU', 'NOM_COM_ALU', 'PROM_GRAL', 'ASISTENCIA', 'SIT_FIN_R', 'MRUN'
]

# Carpeta de entrada y salida
input_folder = 'Datasets/Datos año 2014-2024/'
output_folder = 'Datasets/Reducidos/'

os.makedirs(output_folder, exist_ok=True)

# Procesar todos los CSV en la carpeta de entrada
csv_files = glob.glob(os.path.join(input_folder, '*.csv'))

for csv_file in csv_files:
    df = pd.read_csv(csv_file, delimiter=';', dtype=str)
    # Seleccionar solo las columnas necesarias (si existen)
    cols_presentes = [col for col in columnas_usar if col in df.columns]
    df_reducido = df[cols_presentes].copy()
    # Guardar el archivo reducido
    nombre_archivo = os.path.basename(csv_file)
    output_path = os.path.join(output_folder, nombre_archivo)
    df_reducido.to_csv(output_path, index=False, sep=';')
    print(f"Archivo reducido guardado: {output_path}")