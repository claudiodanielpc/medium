# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import requests
import plotly.graph_objects as go
import chart_studio.plotly as py
import chart_studio


# %%
url = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/?token=TU_TOKEN"
respuesta = requests.get(url).json()
respuesta


# %%
#Obtener los datos
datos=respuesta["bmx"]["series"][0]["datos"]
datos


# %%
#Dataframe de pandas
banxico= pd.DataFrame(datos)
#Checar el tipo de variables
banxico.dtypes


# %%
#Cambiar variable de fecha a datetime
banxico['fecha'] = pd.to_datetime(banxico['fecha'],format="%d/%m/%Y")
#Cambiar dato a float
banxico["dato"] = pd.to_numeric(banxico["dato"])

banxico


# %%
#Gráfica en plotly

#Definición de la gráfica
fig=go.Figure([go.Scatter(x=banxico["fecha"], y=banxico["dato"],
line=dict(color="#285c4d",width=3)
)])

# Poner título
fig.update_layout(
    title_text="<b>Tipo de cambio diario. Fecha de determinación (FIX)</b><br><i>(Pesos por dólar)</i>"
)

#Fuente y color de texto
fig.update_layout(
    font_family="Montserrat",
     font_color="black",
     #Color del fondo del gráfico
     plot_bgcolor="white"
     )

#Formato de ejes y botones
fig.update_layout(

    xaxis=dict(
        dtick="M24",
    tickformat="%d/%m\n%Y",
rangeslider_visible=True,    
rangeselector=dict(
        buttons=list([
            dict(count=1, label="1 mes", step="month", stepmode="backward"),
            dict(count=3, label="3 meses", step="month", stepmode="backward"),
            dict(count=6, label="6 meses", step="month", stepmode="backward"),
            dict(count=1, label="1 año", step="year", stepmode="todate"),
            dict(label="Todo", step="all")
            ]),
            
),
 type="date"
),



yaxis=dict(gridcolor='grey', 
gridwidth=0.05,
fixedrange=False
)

)
fig.update_layout(hovermode="x unified")

fig.show()   
    


# %%
###Credenciales para subir gráfica generada a cuenta de Chart Studio
username = 'tu_usuario' # Tu usuario
api_key = 'tu_llave' # API Key
chart_studio.tools.set_credentials_file(username=username, api_key=api_key)

#Salvar y mostrar
py.plot(fig, filename = 'exchange_rate', auto_open=True)


