import os
import glob
import pandas as pd

# Carpeta donde están los archivos
folder = 'Datasets/Reducidos/'

# Lista de años a procesar
years = list(range(2018, 2024))  # Ajusta a 2025 si tienes ese año

# Códigos de egreso
egreso_codigos = {'410','460','461','463','510','560','561','663','610','660','661','710','760','761','763','810','860','861','863','910','963'}

# Buscar todos los archivos CSV de cada año
csv_files = []
for year in years:
    files = glob.glob(os.path.join(folder, f"*{year}*.csv"))
    csv_files.extend(sorted(files))  # Ordena para asegurar el orden cronológico

# DataFrame acumulador
df_final = pd.DataFrame()

for csv_file in csv_files:
    df_year = pd.read_csv(csv_file, delimiter=';', dtype=str)
    # Asegura que las columnas clave existan
    for col in ['MRUN', 'SIT_FIN', 'COD_ENSE', 'COD_GRADO']:
        if col not in df_year.columns:
            df_year[col] = None
    df_year['AÑO'] = os.path.basename(csv_file)  # Puedes extraer el año si lo necesitas
    df_year = df_year.drop_duplicates(subset=['MRUN'], keep='last')
    if df_final.empty:
        df_final = df_year.copy()
        df_final['modificado'] = False
    else:
        # Identifica filas que serán reemplazadas
        mrun_intersect = set(df_final['MRUN']) & set(df_year['MRUN'])
        df_final['modificado'] = df_final['MRUN'].apply(lambda x: x in mrun_intersect)
        # Elimina filas que serán reemplazadas
        df_final = df_final[~df_final['modificado']]
        # Agrega las filas nuevas y reemplazadas
        df_final = pd.concat([df_final, df_year], ignore_index=True)
        df_final['modificado'] = df_final['MRUN'].duplicated(keep='last')
        df_final = df_final[~df_final['modificado']]
        df_final = df_final.drop(columns=['modificado'], errors='ignore')

# Ahora, crea la variable 'estado'
def calcular_estado(row):
    # Egresado
    if (row['COD_ENSE'] in egreso_codigos) and (row['COD_GRADO'] == '4'):
        return 'egresado'
    # Abandono en el año
    elif row['SIT_FIN'] == "Y":
        return 'abandono_en_año'
    # Cursando
    elif row['SIT_FIN'] != "Y":
        return 'cursando'

df_final['estado'] = df_final.apply(calcular_estado, axis=1)

# Ahora, para abandono_entre_años:
# Si una fila NO fue modificada (es decir, no fue reemplazada en ningún año posterior)
# y SIT_FIN no es 'Y', entonces 'abandono_entre_años'
# (Esto requiere rastrear los MRUN que nunca fueron reemplazados)
# Para esto, necesitamos rehacer el proceso con una columna de "modificado" persistente

# Repetimos el proceso para marcar correctamente abandono_entre_años
df_final = pd.DataFrame()
mrun_modificados = set()
for csv_file in csv_files:
    df_year = pd.read_csv(csv_file, delimiter=';', dtype=str)
    for col in ['MRUN', 'SIT_FIN', 'COD_ENSE', 'COD_GRADO']:
        if col not in df_year.columns:
            df_year[col] = None
    df_year['AÑO'] = os.path.basename(csv_file)
    df_year['modificado'] = df_year['MRUN'].apply(lambda x: x in mrun_modificados)
    mrun_modificados.update(df_year['MRUN'])
    if df_final.empty:
        df_final = df_year.copy()
    else:
        # Elimina filas que serán reemplazadas
        df_final = df_final[~df_final['MRUN'].isin(df_year['MRUN'])]
        df_final = pd.concat([df_final, df_year], ignore_index=True)

def calcular_estado_final(row):
    if (row['COD_ENSE'] in egreso_codigos) and (row['COD_GRADO'] == '4'):
        return 'egresado'
    elif row['SIT_FIN'] == "Y":
        return 'abandono_en_año'
    elif not row['modificado'] and row['SIT_FIN'] != "Y":
        return 'abandono_entre_años'
    return 'cursando'

df_final['estado'] = df_final.apply(calcular_estado_final, axis=1)
df_final = df_final.drop(columns=['modificado'])

# Guardar el resultado unificado en un CSV
output_path = os.path.join(folder, 'dataset_unificado3.csv')
df_final.to_csv(output_path, index=False, sep=';')
print(f"Archivo unificado guardado en: {output_path}")

# Resultado final
print(df_final[['MRUN', 'SIT_FIN', 'COD_ENSE', 'COD_GRADO', 'estado']].head())
print(df_final['estado'].value_counts())