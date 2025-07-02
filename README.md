# Proyecto de Predicción de Abandono Escolar

Este proyecto tiene como objetivo predecir el abandono escolar utilizando datos históricos de estudiantes desde 2014 a 2024. El flujo abarca desde la limpieza y unificación de datos, pasando por el entrenamiento de modelos de machine learning, hasta la implementación de una interfaz web para predicción dinámica.

---

## 📁 Estructura de Carpetas y Archivos

```
Proyecto Final Feria/
│
├── Datasets/
│   └── Datasets/Datos año 2014-2024/      # Archivos CSV originales por año
│   └── Datasets/Reducidos/                # Archivos CSV reducidos y unificados
│
├── Desarrollo.ipynb                       # Notebook principal de análisis y modelado
├── Previo_unificar_limpieza_de_columnas.py# Script para reducir columnas de los CSV originales
├── app_prediccion.py                      # App Streamlit para predicción interactiva
├── modelo_entrenado_XGBoost.pkl           # Modelo XGBoost entrenado y serializado
├── columnas_modelo.txt                    # Columnas usadas para el entrenamiento del modelo
├── Dashboard.py                           # (Opcional) Dashboard para consulta a API (no REST)
└── README.md                              # (Este archivo)
```

---

## 🚦 Flujo y Procedimientos del Proyecto

### 1. **Reducción y Limpieza Inicial de los Datos**
- **Archivo:** `Previo_unificar_limpieza_de_columnas.py`
- **Función:** Lee todos los CSV originales de cada año, selecciona solo las columnas relevantes y guarda una versión reducida en `Datasets/Reducidos/`.
- **Uso:**  
  ```bash
  python Previo_unificar_limpieza_de_columnas.py
  ```

---

### 2. **Unificación y Limpieza Avanzada**
- **Archivo:** `Desarrollo.ipynb`
- **Función:**  
  - Une todos los datasets anuales en uno solo, reemplazando información antigua por la más reciente según el identificador `MRUN`.
  - Crea la variable `estado` con valores: `abandono_entre_años`, `abandono_en_año`, `cursando`, `egresado` según reglas de negocio.
  - Elimina egresados si es necesario.
  - Realiza limpieza de datos, imputación de valores, codificación de variables categóricas y balanceo de clases.
  - Entrena y compara varios modelos de clasificación (Logistic Regression, Random Forest, Gradient Boosting, XGBoost).
  - Guarda el modelo XGBoost final y las columnas usadas para el entrenamiento.
- **Salida:**  
  - `Datasets/Reducidos/dataset_unificado3_sin_egresados.csv` (u otro nombre según versión)
  - `modelo_entrenado_XGBoost.pkl`
  - `columnas_modelo.txt`

---

### 3. **Entrenamiento y Guardado del Modelo**
- **Archivo:** `Desarrollo.ipynb`
- **Función:**  
  - Entrena el modelo XGBoost final con los datos limpios y balanceados.
  - Guarda el modelo entrenado con `joblib.dump`.
  - Guarda las columnas usadas para el entrenamiento en `columnas_modelo.txt`.

---

### 4. **Predicción Dinámica vía Interfaz Web**
- **Archivo:** `app_prediccion.py`
- **Función:**  
  - Interfaz web con Streamlit para ingresar datos de un estudiante y obtener la probabilidad de abandono.
  - Carga el modelo entrenado y las columnas del modelo.
  - Preprocesa la entrada del usuario igual que en el entrenamiento.
  - Muestra la probabilidad y la predicción (`Abandona`/`No abandona`).
- **Uso:**  
  ```bash
  streamlit run app_prediccion.py
  ```
  - Accede a [http://localhost:8501](http://localhost:8501) en tu navegador.

---

### 5. **Dashboard de Consulta (Opcional)**
- **Archivo:** `Dashboard.py`
- **Función:**  
  - Permite configurar la URL de un endpoint de predicción (pensado para una API REST, pero Streamlit no expone endpoints REST).
  - Útil si en el futuro se implementa una API con FastAPI o Flask.

---

## 📋 Orden de Ejecución Recomendado

1. **Reducir los datasets originales:**  
   Ejecuta `Previo_unificar_limpieza_de_columnas.py` para obtener archivos reducidos.
2. **Unificar, limpiar y preparar los datos:**  
   Trabaja en `Desarrollo.ipynb` para unificar, limpiar, balancear y entrenar modelos.
3. **Guardar el modelo y columnas:**  
   Desde el notebook, guarda el modelo XGBoost y las columnas.
4. **Realizar predicciones dinámicas:**  
   Ejecuta `streamlit run app_prediccion.py` y usa la interfaz web.
5. **(Opcional) Implementar una API REST:**  
   Si necesitas exponer el modelo como API, crea un script con FastAPI o Flask.

---
