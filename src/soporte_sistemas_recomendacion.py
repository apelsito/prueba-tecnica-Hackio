# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd

# Para visualización de datos
# -----------------------------------------------------------------------
import matplotlib.pyplot as plt

def get_index_from_title(title, dataframe):
    """
    Obtiene el índice de un dataframe basado en el título de una película.

    Parameters:
    ----------
    title : str
        El título de la película a buscar.
    dataframe : pd.DataFrame
        El dataframe que contiene la información, con una columna 'title'.

    Returns:
    -------
    int
        El índice correspondiente al título de la película en el dataframe.
    """
    return dataframe[dataframe.title == title].index[0]


def get_title_from_index(index, dataframe):
    """
    Obtiene el título de una película basado en su índice en un dataframe.

    Parameters:
    ----------
    index : int
        El índice de la película a buscar.
    dataframe : pd.DataFrame
        El dataframe que contiene la información, con una columna 'title'.

    Returns:
    -------
    str
        El título de la película correspondiente al índice proporcionado.
    """
    return dataframe[dataframe.index == index]["title"].values[0]


def plot(peli1, peli2, dataframe):
    """
    Genera un gráfico de dispersión que compara dos películas en un espacio de características.

    Parameters:
    ----------
    peli1 : str
        Nombre de la primera película a comparar.
    peli2 : str
        Nombre de la segunda película a comparar.
    dataframe : pd.DataFrame
        Un dataframe transpuesto donde las columnas representan películas y las filas características.

    Returns:
    -------
    None
        Muestra un gráfico de dispersión con anotaciones para cada película.
    """
    x = dataframe.T[peli1]     
    y = dataframe.T[peli2]

    n = list(dataframe.columns)    

    plt.figure(figsize=(10, 5))

    plt.scatter(x, y, s=0)      

    plt.title('Espacio para {} VS. {}'.format(peli1, peli2), fontsize=14)
    plt.xlabel(peli1, fontsize=14)
    plt.ylabel(peli2, fontsize=14)

    for i, e in enumerate(n):
        plt.annotate(e, (x[i], y[i]), fontsize=12)  

    plt.show();


def filter_data(df):
    """
    Filtra un dataframe de ratings basado en la frecuencia mínima de valoraciones por película y por usuario.

    Parameters:
    ----------
    df : pd.DataFrame
        Un dataframe con columnas 'movieId', 'userId' y 'rating'.

    Returns:
    -------
    pd.DataFrame
        Un dataframe filtrado que contiene solo las películas con al menos 300 valoraciones 
        y los usuarios con al menos 1500 valoraciones.
    """
    ## Ratings Per Movie
    ratings_per_movie = df.groupby('movieId')['rating'].count()
    ## Ratings By Each User
    ratings_per_user = df.groupby('userId')['rating'].count()

    ratings_per_movie_df = pd.DataFrame(ratings_per_movie)
    ratings_per_user_df = pd.DataFrame(ratings_per_user)

    filtered_ratings_per_movie_df = ratings_per_movie_df[ratings_per_movie_df.rating >= 300].index.tolist()
    filtered_ratings_per_user_df = ratings_per_user_df[ratings_per_user_df.rating >= 1500].index.tolist()
    
    df = df[df.movieId.isin(filtered_ratings_per_movie_df)]
    df = df[df.userId.isin(filtered_ratings_per_user_df)]
    return df