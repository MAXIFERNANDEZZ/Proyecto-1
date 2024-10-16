# <h1 align=center> **PROYECTO INDIVIDUAL Nº1** </h1>

# <h1 align=center>**`Machine Learning Operations (MLOps)`**</h1>

¡Bienvenidos a mi primer proyecto individual de la etapa de labs! En esta ocasión, realizaré un trabajo desde el rol de un ***MLOps Engineer***.

<hr>  

## **Descripción del problema (Contexto y rol a desarrollar)**

## Contexto

Tienes tu modelo de recomendación dando unas buenas métricas y ahora, cómo lo llevas al mundo real?

El ciclo de vida de un proyecto de Machine Learning debe contemplar desde el tratamiento y recolección de los datos (Data Engineer stuff) hasta el entrenamiento y mantenimiento del modelo de ML según llegan nuevos datos.


## Rol a desarrollar

Empezaste a trabajar como **`Data Scientist`** en Steam, una plataforma multinacional de videojuegos. El mundo es bello y vas a crear tu primer modelo de ML que soluciona un problema de negocio: Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios. :

Vas a sus datos y te das cuenta que la madurez de los mismos es poca (ok, es nula : ): Datos anidados, de tipo raw, no hay procesos automatizados para la actualización de nuevos productos, entre otras cosas… haciendo tu trabajo imposible : . 

Debes empezar desde 0, haciendo un trabajo rápido de **`Data Engineer`** y tener un **`MVP`** (_Minimum Viable Product_) para el cierre del proyecto! Tu cabeza va a explotar, pero al menos sabes cual es, conceptualmente, el camino que debes de seguir :. Así que espantas los miedos y pones manos a la obra:

## Descripción del proyecto

El proceso que hice yo para este proyecto fue: ETL -> EDA -> Funciones para la API -> Desarrollo del sistema de recomendación -> FastAPI -> Deployment

<br/>

## **Datos Originales**

+ [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con el archivo que requieren ser procesados, tengan en cuenta que hay datos que estan anidados (un diccionario o una lista como valores en la fila).
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>

## ETL

En el proceso de ETL se generaron los siguientes archivos [ETL_STEAM](ETL_Juegos.ipynb), [ETL_ITEMS](ETL_Items.ipynb) y [ETL_REVIEWS](ETL_Reviews.ipynb)

<br/>

## EDA

Una vez terminado el ETL  se continuó con el EDA para investigar las relaciones entra las variables, ver outliers, anomalias, patrones, etc. 
Lamentablemente por un error mio perdí todo lo que estaba hecho en el EDA por lo que no voy a poder mostrar lo que hice

## Desarrollo de la API

Para el desarrollo de la API se utiliza FastAPI, creando las siguientes funciones:

No logre que funcione
+ def **developer( *`desarrollador` : str* )**:
    `Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora. 
Ejemplo de retorno:

| Año  | Cantidad de Items | Contenido Free  |
|------|-------------------|------------------|
| 2023 | 50                | 27%              |
| 2022 | 45                | 25%              |
| xxxx | xx                | xx%              |


+ def **userdata( *`User_id` : str* )**:
    Debe devolver `cantidad` de dinero gastado por el usuario, el `porcentaje` de recomendación en base a reviews.recommend y `cantidad de items`.

Ejemplo de retorno: {"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}

+ def **UserForGenre( *`genero` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}

 No logre que funcione
+ def **best_developer_year( *`año` : int* )**:
   Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos)
  
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]

+ def **developer_reviews_analysis( *`desarrolladora` : str* )**:
    Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}

+ def **recomendacion_juego( *`id de producto`* )**:
    Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

## FastAPI

El código para generar la API se encuentra en el archivo [Main](/main.py).

## Deployment
Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web.

* Se genera el link donde queda corriendo [link](https://proyecto-individual-maxi-1.onrender.com)

## Video
Demostración y funcionamiento de la API [link](https://youtu.be/JOHpoVytzfo)



  













