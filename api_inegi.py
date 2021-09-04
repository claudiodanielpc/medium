#Uso de la API del DENUE de INEGI

#Librerías
import requests
import pandas as pd
import folium
from folium import plugins



#url con token
#Ejemplo: todas las unidades económicas de Morelos
url = "https://www.inegi.org.mx/app/api/denue/v1/consulta/BuscarEntidad/todos/17/1/100000000/AQUÍ_VA_TU_TOKEN"

#Respuesta de la consulta a la API  
respuesta = requests.get(url).json()

#Dataframe de pandas
df= pd.DataFrame(respuesta)

##Pasamos los nombres de las variables a minúsculas
df.columns= df.columns.str.lower()
#Corroborar la descarga y arreglo
df.info()


#Seleccionamos solo la latitud y longitud
df=df[["latitud", "longitud"]]

#Convertimos nuestra df a un array
df =df.values



#Mapa en Folium
m=folium.Map(
    location=[18.731829,-99.3438812],
    tiles='OpenStreetMap',
             zoom_start=10)
#Heatmap
m.add_child(plugins.HeatMap(df, radius=15))

#Salvar mapa en html
m.save("mapa.html")



