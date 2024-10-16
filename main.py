#librerías
from fastapi import FastAPI
import pandas as pd
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

#Instanciamos la app
app = FastAPI()

#Traemos las tablas necesarias
Juegos= pd.read_parquet('data/DF_Juegos.parquet')
Items = pd.read_parquet('data/DF_Items.parquet')
Reviews = pd.read_parquet('data/Reviews.parquet')
Rec_Juegos = pd.read_parquet('data/Rec_Juegos.parquet')

@app.get("/")
async def root():
    return {"message": "¡Servicio en funcionamiento!"}

@app.get('/developer/{desarrollador}',name= 'DEVELOPER')
async def developer(desarrollador):
    
    juegos_des = Juegos[Juegos['developer'] == desarrollador] # Filtramos los juegos por desarrollador
    
    item_des = Items[Items['item_id'].isin(juegos_des['id'])] # Unimos con el DataFrame de Items para obtener los IDs de los items

    cant_item = item_des.groupby('items_count').size().reset_index(name='cantidad_items') # Calculamos la cantidad de items por año
    
    # Calculamos el porcentaje de contenido gratis
    juego_gratis = juegos_des['price'] == 0  #Si el precio es 0, es gratis
    por_gratis = juego_gratis.mean() * 100  #Si el 100% de los precios son 0 entonces el Developer hace todos sus juegos gratis

    # Agrupamos por año de lanzamiento
    resumen = juegos_des.groupby('Año de Lanzamiento').agg(
        cant_item=('id', 'count'),  
        por_gratis=('price', lambda x: (x == 0).mean() * 100)  
    ).reset_index()
    
    return resumen

@app.get('/UserForGenre/{genero}', name= 'USERFORGENRE')
async def UserForGenre(genero):

    juego = Juegos[Juegos['genres'].str.contains(genero, na=False)] #Filtramos los juegos por el genero
    
    item = Items[Items['item_id'].isin(juego['id'])] #Obtenemos las horas jugadas
    
    horas = item.groupby('user_id')['items_count'].sum().reset_index() #Sumamos las horas por usuario

    usuario_que_mas_jugo = horas.loc[horas['items_count'].idxmax()] #Usuario con las horas jugadas
    
    #Horas jugadas por año de lanzamiento
    horas_por_año = (item
                     .merge(juego[['id', 'Año de Lanzamiento']], left_on='item_id', right_on='id')
                     .groupby('Año de Lanzamiento')['items_count'].sum()
                     .reset_index()
                     .rename(columns={'Año de Lanzamiento': 'Año', 'items_count': 'Horas'}))

    horas_por_año_list= horas_por_año.to_dict(orient='records') #Convertimos a diccionarios
    
    Respuesta = {
        "Usuario con más horas jugadas para Género": usuario_que_mas_jugo['user_id'],
        "Horas jugadas": horas_por_año_list
    }
    
    return Respuesta

@app.get('/userdata/{user_id}',name= 'USERDATA')
async def userdata(user_id):
    
    item = Items[Items['user_id'] == user_id] #Filtramos los items del usuario
    
    cantidad = item['items_count'].sum()  #Calculamos la cantidad de items del usuario
    
    cantidad= int(cantidad) #Arreglamos el valor de salida 

    
    gasto = item.merge(Juegos[['id', 'price']], left_on='item_id', right_on='id', how='left') #Calculamos el gasto total
    gasto = (gasto['price'] * gasto['items_count']).sum()  
    gasto = f"{gasto:.2f} USD" #Arreglamos el valor de salida 

    
    reseña = Reviews[Reviews['user_id'] == user_id] #Filtramos las reseñas del usuario

    #Calculamos el porcentaje de recomendacion
    if not reseña.empty:
        reco = (reseña['recommend'].mean()) * 100 
    else:
        reco = 0.0
        
    reco= f'{float(reco):.2f}%' #Arreglamos el valor de salida 

    return {'Usuario': user_id, 'Dinero gastado': gasto, '% de recomendación ': reco, 'Cantidad de items': cantidad}

@app.get('/best_developer_year/{año}',name= 'BESTDEVELOPERYEAR')
async def best_developer_year(año):

    reseñas = Reviews[(Reviews['year'] == año) & (Reviews['recommend'] == True)] #Filtramos las reseñas por año

    if reseñas.empty:
        return "No hay reseñas para el año dado."

    juego_reco = reseñas.merge(Juegos[['id', 'developer']], left_on='item_id', right_on='id', how='left') #Unimos con Juegos para obtener los desarrolladores

    reco_for_des = juego_reco.groupby('developer')['recommend'].count().reset_index() #Contamos recomendaciones por desarrollador

    reco_for_des.columns = ['developer', 'total_recommendations'] #Renombramos la columna para poder distinguirlas

    top_desarrolladores = reco_for_des.sort_values(by='total_recommendations', ascending=False).head(3) #Ordenamos las recomendaciones en descendente y seleccionamos las 3 primeras

    #Ajustamos el modo de respuesta
    res= []
    for index, row in top_desarrolladores.iterrows():
        puesto = f"Puesto {index + 1}"
        res.append({puesto: row['developer']})

    return res


@app.get('/developer_reviews_amalysis/{desarrolladora}',name= 'DEVELOPERREVIEWSANALYSIS')
async def developer_reviews_analysis(desarrolladora):
    
    juego_for_des = Juegos[Juegos['developer'] == desarrolladora] #Filtramos reseñas por desarrollador
    
    if juego_for_des.empty:
        return {desarrolladora: "No se encontraron juegos para este desarrollador."}
    
    reseñas = Reviews[Reviews['item_id'].isin(juego_for_des['id'])] #Filtramos reseñas por juego y desarrollador

    total_positivas = reseñas[reseñas['sentiment_analysis'] > 0].shape[0]#Diferenciamos positivas y negativas
    total_negativas = reseñas[reseñas['sentiment_analysis'] < 0].shape[0]

    #Respuesta
    respuesta = {desarrolladora: [f"Negative = {total_negativas}", f"Positive = {total_positivas}"]}
    return respuesta


@app.get('/recomendacion_juego/{id}',name= 'RECOMENDACIONJUEGO')
async def recomendacion_juego(id):
    
    id_str = str(id) #Convertimos id a string

    juego = Juegos[Juegos['id'].astype(str) == id_str] #Buscamos el juego solicitado

    if juego.empty:
        return "No logré encontrar el juego"

    genero = juego['genres'].values[0]  #Buscamos el género del juego

    sim = Juegos[(Juegos['genres'] == genero) & (Juegos['id'].astype(str) != id_str)] #Filtramos los juegos con el mismo género

    sim = sim.sample(n=min(5, sim.shape[0]))  #Seleccionamos 5 juegos

    reco = sim['app_name'].tolist()  #Creamos una lista con los juegos recomendados

    return reco

