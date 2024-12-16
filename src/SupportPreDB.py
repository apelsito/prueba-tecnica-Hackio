# Importación de librerías necesarias para el proyecto

# Automatización de navegadores (Selenium)
# -----------------------------------------------------------------------
from selenium import webdriver                      # Control automático del navegador para realizar scraping web
from selenium.webdriver.chrome.service import Service  # Manejo del servicio de ChromeDriver
from selenium.webdriver.common.by import By         # Selección de elementos en el DOM
from selenium.webdriver.chrome.options import Options  # Configuración de opciones del navegador (headless mode, etc.)
import time                                         # Para gestionar pausas y temporización

# Extracción de datos y scraping
# -----------------------------------------------------------------------
from bs4 import BeautifulSoup                       # Análisis y extracción de datos de HTML y XML (scraping web)

# Tratamiento y manipulación de datos
# -----------------------------------------------------------------------
import pandas as pd                                 # Manipulación de estructuras de datos como DataFrames
import numpy as np                                  # Cálculos numéricos y manejo de arrays
import datetime                                     # Manipulación de fechas y tiempos

# Visualización de progreso
# -----------------------------------------------------------------------
from tqdm import tqdm                               # Creación de barras de progreso durante bucles

# Manejo de tiempo y solicitudes con espera
# -----------------------------------------------------------------------
from time import sleep                              # Pausas en la ejecución del código
import random                                       # Generación de valores aleatorios, útil para espaciar solicitudes y evitar bloqueos

def crear_df_unicos(df, nombre_columna):
    """
    Crea un DataFrame con valores únicos de una columna específica y un índice numerado a partir de 1.

    Args:
        df (pandas.DataFrame): DataFrame de entrada que contiene la columna de interés.
        nombre_columna (str): Nombre de la columna cuyos valores únicos se extraerán.

    Returns:
        pandas.DataFrame: DataFrame que contiene una columna con los valores únicos y una columna de índice numerado.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'col1': [1, 2, 2, 3], 'col2': ['A', 'B', 'B', 'C']})
        >>> crear_df_unicos(df, 'col2')
           index col2
        0      1    A
        1      2    B
        2      3    C
    """
    columna = nombre_columna
    lista_unicos = df[columna].unique().tolist()
    df_unicos = pd.DataFrame({
                    columna : lista_unicos
                    })
    df_unicos.index = pd.RangeIndex(start=1,
                                    stop = len(df_unicos) + 1,
                                    step=1)
    
    df_unicos.reset_index(inplace=True)
    
    return df_unicos

def crear_dictio(df,columna):
    """
    Crea un diccionario a partir de un DataFrame, donde las claves son valores únicos de una columna específica,
    y los valores son los primeros índices asociados a cada clave en el DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame de entrada que contiene la columna de interés.
        columna (str): Nombre de la columna cuyos valores únicos se usarán como claves en el diccionario.

    Returns:
        dict: Diccionario donde las claves son los valores únicos de la columna especificada, y los valores son 
              los primeros índices asociados a cada clave en el DataFrame.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'index': [1, 2, 3, 4], 'columna': ['A', 'B', 'A', 'C']})
        >>> crear_dictio(df, 'columna')
        {'A': 1, 'B': 2, 'C': 4}
    """
    dictio = {}
    datos = df.groupby(columna)["index"].first()
    indices = list(datos.index)
    valores = list(datos.values)
    for i in range(0, len(indices)):
        dictio[indices[i]] = valores[i] 
    
    return dictio

def crear_df_historico(df_historicos,df_supermercado,df_categoria,df_producto):
    """
    Modifica el DataFrame `df_historicos`, reemplazando los nombres de supermercados, categorías y productos
    con sus correspondientes índices, utilizando diccionarios generados a partir de DataFrames de referencia.

    Args:
        df_historicos (pandas.DataFrame): DataFrame que contiene los datos históricos con columnas de nombres
                                          de supermercados, categorías y productos.
        df_supermercado (pandas.DataFrame): DataFrame que contiene los nombres de los supermercados y sus índices.
        df_categoria (pandas.DataFrame): DataFrame que contiene los nombres de las categorías y sus índices.
        df_producto (pandas.DataFrame): DataFrame que contiene los nombres de los productos y sus índices.

    Returns:
        pandas.DataFrame: DataFrame `df_historicos` modificado, con nombres reemplazados por sus índices correspondientes.

    Example:
        >>> df_historicos = pd.DataFrame({'supermercado': ['Super1', 'Super2'], 'categoria': ['Cat1', 'Cat2'], 'producto': ['Prod1', 'Prod2']})
        >>> df_supermercado = pd.DataFrame({'index': [1, 2], 'supermercado': ['Super1', 'Super2']})
        >>> df_categoria = pd.DataFrame({'index': [1, 2], 'categoria': ['Cat1', 'Cat2']})
        >>> df_producto = pd.DataFrame({'index': [1, 2], 'producto': ['Prod1', 'Prod2']})
        >>> crear_df_historico(df_historicos, df_supermercado, df_categoria, df_producto)
           supermercado  categoria  producto
        0            1          1         1
        1            2          2         2
    """
    # Creamos los diccionarios
    dictio_supermercados = crear_dictio(df_supermercado,"supermercado")
    dictio_categorias = crear_dictio(df_categoria,"categoria")
    dictio_productos = crear_dictio(df_producto,"producto")
    
    #Ponemos cada valor según cada uno de los diccionarios
    df_historicos["supermercado"] = df_historicos["supermercado"].map(dictio_supermercados)
    df_historicos["categoria"] = df_historicos["categoria"].map(dictio_categorias)
    df_historicos["producto"] = df_historicos["producto"].map(dictio_productos)

    return df_historicos