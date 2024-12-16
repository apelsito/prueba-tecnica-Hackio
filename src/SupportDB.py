# Importación de librerías necesarias para trabajar con bases de datos y DataFrames

# Conexión y manejo de bases de datos PostgreSQL
# -----------------------------------------------------------------------
import psycopg2                                 # Conexión con bases de datos PostgreSQL
from psycopg2 import OperationalError, errorcodes, errors  # Manejo de errores específicos de psycopg2

# Manipulación de DataFrames
# -----------------------------------------------------------------------
import pandas as pd                             # Manipulación y análisis de datos en estructuras DataFrame



def conectarse_a_bd(db,user,pwd):
    """
    Establece una conexión a la base de datos PostgreSQL.

    Args:
        db (str): Nombre de la base de datos a la que se desea conectar.
        user (str): Nombre de usuario para la autenticación en la base de datos.
        pwd (str): Contraseña para el usuario especificado. Es recomendable almacenarla en un archivo .env.

    Returns:
        connection: Objeto de conexión a la base de datos si la conexión es exitosa.
    
    Raises:
        psycopg2.OperationalError: Si ocurre un error durante la conexión.
    
    Exceptions:
        Imprime mensajes específicos en caso de errores de conexión comunes:
            - "La contraseña es errónea" si el código de error es `INVALID_PASSWORD`.
            - "Error de conexión" si el código de error es `CONNECTION_EXCEPTION`.
            - "Ocurrió el error {e}" para otros errores inesperados.

    Example:
        >>> conexion = conectarse_a_bd("mi_base_de_datos", "mi_usuario", "mi_contraseña")
        Conectado a la base de datos: mi_base_de_datos

    """
    try:
        conexion = psycopg2.connect(
            database = db,
            user = user,
            password = pwd,#Esto en un .env
            host = "localhost",
            port = "5432" )
        print (f"Conectado a la base de datos: {db}")
        return conexion
    except OperationalError as e:
        if e.pgcode == errorcodes.INVALID_PASSWORD:
            print("La contraseña es errónea")
        elif e.pgcode == errorcodes.CONNECTION_EXCEPTION:
            print("Error de conexión")
        else:
            print(f"Ocurrió el error {e}")

def modificar_bd(conexion, query):
    """
    Ejecuta una consulta SQL de modificación en la base de datos PostgreSQL y confirma los cambios.

    Args:
        conexion: Objeto de conexión a la base de datos, previamente establecido.
        query (str): Cadena de texto con la consulta SQL de modificación (por ejemplo, INSERT, UPDATE, DELETE).

    Returns:
        None

    Raises:
        Exception: Imprime un mensaje de error si no se puede ejecutar la consulta o confirmar la modificación.

    Example:
        >>> modificar_bd(conexion, "UPDATE productos SET precio = 9.99 WHERE id_producto = 1")
        Se ha modificado correctamente la base de Datos
    """
    try:
        cursor = conexion.cursor()
        cursor.execute(query)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Se ha modificado correctamente la base de Datos")
    except Exception as e:
        print("No se ha podido realizar la operación:", e)


def insertar_muchos_datos_bd(conexion, query, tupla):
    """
    Inserta múltiples filas en la base de datos PostgreSQL utilizando una consulta SQL parametrizada.

    Args:
        conexion: Objeto de conexión a la base de datos, previamente establecido.
        query (str): Cadena de texto con la consulta SQL de inserción parametrizada.
        tupla (list of tuples): Lista de tuplas que contienen los valores a insertar.

    Returns:
        None

    Raises:
        Exception: Imprime un mensaje de error si no se puede ejecutar la consulta o confirmar la inserción.

    Example:
        >>> datos = [(1, "Producto A", 9.99), (2, "Producto B", 19.99)]
        >>> insertar_muchos_datos_bd(conexion, "INSERT INTO productos (id_producto, nombre, precio) VALUES (%s, %s, %s)", datos)
        Se han añadido los valores correctamente
    """
    try:
        cursor = conexion.cursor()
        cursor.executemany(query,tupla)
        conexion.commit()
        cursor.close()
        conexion.close()
        print("Se han añadido los valores correctamente")
    except Exception as e:
        print("No se ha podido realizar la operación:", e)

def generar_tupla(df,drop_index=False):
    """
    Convierte un DataFrame de pandas en una lista de tuplas para su uso en operaciones de inserción en bases de datos.

    Args:
        df (pandas.DataFrame): DataFrame que se convertirá en una lista de tuplas.
        drop_index (bool, optional): Indica si se debe eliminar la columna de índice llamada "index" del DataFrame. 
                                     El valor predeterminado es False.

    Returns:
        list of tuples: Lista de tuplas, donde cada tupla representa una fila del DataFrame.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'col1': [1, 2], 'col2': ['A', 'B']})
        >>> generar_tupla(df)
        [(1, 'A'), (2, 'B')]
    """
    if drop_index == True:
        df.drop(columns="index",inplace=True)
    tupla = [tuple(valores) for valores in df.values]
    return tupla

def consulta_sql(conexion, query):
    """
    Ejecuta una consulta SQL en la base de datos PostgreSQL y devuelve los resultados en un DataFrame de pandas.

    Args:
        conexion: Objeto de conexión a la base de datos, previamente establecido.
        query (str): Cadena de texto con la consulta SQL a ejecutar.

    Returns:
        pandas.DataFrame: DataFrame que contiene los resultados de la consulta, con las columnas correspondientes.

    Example:
        >>> df = consulta_sql(conexion, "SELECT * FROM productos")
        >>> print(df.head())
        
    Notes:
        La conexión a la base de datos se cierra después de ejecutar la consulta.
    """
    cursor = conexion.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    columnas = [col[0] for col in cursor.description]
    cursor.close()
    conexion.close()
    df = pd.DataFrame(resultados,columns=columnas)
    return df