  
#Uso de la API de la ADIP 

#Librerías
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import chart_studio.plotly as py
import chart_studio



#url de la API
url="https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=ae2cd306-1aed-45a1-8ee4-3d0b0852ae4b&limit=400000"
#Respuesta de la consulta a la API con formato JSON  
respuesta = requests.get(url).json()

#Guardamos únicamente los elementos de resultados
result=respuesta["result"]
#Declaramos una dataframe únicamente usando la key denominada RECORDS
df= pd.DataFrame(result["records"])

##Pasamos los nombres de las variables a minúsculas
df.columns= df.columns.str.lower()

#Seleccionar variables y calcular promedio móvil 
df=df[["fecha_toma_muestra", "tasa_positividad_cdmx"]]
#tasa de positividad en porcentaje
df["tasa_positividad_cdmx"]=df["tasa_positividad_cdmx"]*100
df['roll'] = df['tasa_positividad_cdmx'].rolling(7).mean()

#Wide a long
df=pd.melt(df, id_vars=["fecha_toma_muestra"],
 value_vars=["tasa_positividad_cdmx",
 "roll"])
#Cambiar nombre de valores de "variable"
df["variable"] = np.where(df["variable"]=="roll", 
'Promedio móvil 7 días', 'Tasa de positividad')


#Gráfica en plotly

#Definición de la gráfica
fig=px.line(df, x='fecha_toma_muestra', 
y='value',
color="variable",
color_discrete_map={
                 "Promedio móvil 7 días": "#285c4d",
                 "Tasa de positividad": "#b38e5d"},
title="<b>Tasa de positividad en la Ciudad de México</b><br><i>(marzo 2020-septiembre 2021)</i>",
labels=dict(fecha_toma_muestra="Fecha de toma de muestra", 
value="%", variable="Tipo"))
#Formatos
#Fuente y color de texto
fig.update_layout(
    font_family="Montserrat",
     font_color="black"),



###Credenciales para subir gráfica generada a cuenta de Chart Studio
username = 'claudiodaniel' # Tu usuario
api_key = 'uWjjTHdTEyYiy1LjKGuq' # API Key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

#Salvar y mostrar
py.plot(fig, filename = 'positiv', auto_open=True)

