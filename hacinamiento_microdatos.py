import pandas as pd
from samplics.estimation import TaylorEstimator
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import plotly.graph_objects as go
import plotly.io as pio

#Descarga de archivos
url = "https://www.inegi.org.mx/contenidos/programas/enigh/nc/2018/microdatos/enigh2018_ns_viviendas_csv.zip"

##Descarga y descomprimir archivos
resp = urlopen(url)
zipfile = ZipFile(BytesIO(resp.read()))
zf.extractall()

#Lectura y selección de variables
df =pd.read_csv("viviendas.csv",
                usecols=["folioviv",
                         "num_cuarto",
                         "tot_resid",
                         "est_dis",
                         "upm",
                         "factor"])

#Generar indicador de hacinamiento
df["hac"] = ((df['tot_resid']/df["num_cuarto"])> 2.5).astype(int)


#Precisión en la estimación del hacinamiento

hac_prec = TaylorEstimator("total")
hac_prec.estimate(
    y=df["hac"],
    samp_weight=df["factor"],
    stratum=df["est_dis"],
    psu=df["upm"],
    remove_nan=True,
)

print(hac_prec)





#Transformar el objeto a string y dataframe para visualizar

#Se transforma a objeto de texto
texto=str(hac_prec)
#Reemplazamos espacios por tabs
texto=texto.replace(' ', '|')

#Transformamos a dataframe
prec = pd.DataFrame([x.split('|') for x in
                     texto.split('\n')])

#Se elimina la primera fila y se dejan las primeras cinco columnas
prec = prec.iloc[1:, 0:5]

#Renombrar columnas
columnas = {prec.columns[0]: 'tot',
            prec.columns[1]: 'se',
            prec.columns[2]: "low",
            prec.columns[3]: "up",
            prec.columns[4]: "cv"}

prec = prec.rename(columns=columnas)



#Formato de números
cols=prec.columns
prec[cols] = prec[cols].apply(pd.to_numeric,
                              errors='coerce')
#Coeficiente de variación como porcentaje
prec["cv"]=\
    prec["cv"]*100

format_dict = {
                "tot": "{0:,.0f}",
                "se": "{0:,.0f}",
                "low": "{0:,.0f}",
                "up": "{0:,.0f}",
               "cv": "{:.2f}"}

for key, value in format_dict.items():
    prec[key] = prec[key].apply(value.format)


#Tabla usando plotly
fig = go.Figure(data=[go.Table(
    header=dict(values=["<b>Viviendas con habitantes en condición de hacinamiento</b>",
                        "<b>Error estándar</b>",
                "<b>Límite inferior</b>",
                        "<b>Límite superior</b>",
                        "<b>Coeficiente de variación</b>"
                        ],
                fill_color='#9ebcda',
                align='center',
                font_family="Montserrat",
                font_size=20),
cells=dict(values=[prec["tot"], prec["se"], prec["low"],
                   prec["up"], prec["cv"]],
               fill_color='lavender',
               align='center',
           font_family="Montserrat",
           font_size=18))
])

#Título
fig.update_layout(
    showlegend=False,
    title_text="<b>México. Viviendas con habitantes en condición de hacinamiento, 2018<br>",
    title_font_family="Montserrat",
    title_font_size=25
)

#Fuente
fig.add_annotation(text="@claudiodanielpc con información de INEGI. Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2018",
                  x=0, y=0, showarrow=False,
                   font_family="Century Gothic")

#Salvar la tabla como PNG

pio.write_image(fig, "tablaenigh.png",width=2000, scale=1,
                height=400)