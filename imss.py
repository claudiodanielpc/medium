##Código artículo:
#Está muy chido el tutorial del IMSS en R pero, ¿puedes hacerlo usando Python🐍?

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


#Lectura de archivos de 2015 a 2020
frames = []
for year in range(2015,2021):
#Lectura del CSV con columnas específicas a utilizar y el tipo
    data =pd.read_csv("http://datos.imss.gob.mx/sites/default/files/asg-"+str(year)+"-12-31.csv",
                      encoding="latin",
                      usecols=["cve_entidad",
                               "cve_municipio",
                               "sector_economico_1",
                               "ta"],
                      dtype={
                          "cve_entidad": int,
                          "cve_municipio": str,
                          "sector_economico_1": float,
                          "ta": float
                      },
                      sep="|")
    #Se agrega columna con el año de la información
    data.loc[:, "year"] = year
    frames.append(data)

#Consolidar
df = pd.concat(frames, axis=0,
               ignore_index=True)

#Hacer los filtro de entidad (Sonora) y sector econòmico (Construcciòn )

df = df[(df["cve_entidad"]==26) &
      (df["sector_economico_1"] == 4)]

#Leer catálogo, filtrar y renombrar

cat= pd.read_excel("http://datos.imss.gob.mx/sites/default/files/diccionario_de_datos_1.xlsx",
                   sheet_name=3, header=1)

cat = cat[cat["cve_entidad"]==26]
cat=cat.rename(columns={cat.columns[4]: 'nom_mun'})
#Se dejan las variables con las que se trabajarán
cat = cat[["cve_municipio",
           "nom_mun"]]

#Pegar datos del catálogo a dataframe

df= df.merge(cat,
             how="left")

#Hacer sumatoria por municipio y año

df= df.groupby(["year",
                 "nom_mun"])["ta"].sum().reset_index()

#Sumatoria del total para sacar porcentajes
df['tot'] = df.groupby(
    'year')["ta"].transform('sum')
#Porcentajes de participación
df["pct"] = df["ta"]/df["tot"]*100


#Filtrar para el municipio requerido

df = df[df["nom_mun"] == "Hermosillo"]

#Calcular crecimiento anual
df['growth']=df["ta"].pct_change()*100

#Quitar el nombre

df = df.drop('nom_mun', 1)

#Formato de números

format_dict = {
                "ta": "{0:,.0f}",
                "tot": "{0:,.0f}",
               "pct": "{:.1f}",
               "growth": "{:.1f}"}

for key, value in format_dict.items():
    df[key] = df[key].apply(value.format)


#Tabla usando plotly
fig = go.Figure(data=[go.Table(
    header=dict(values=["<b>Año</b>", "<b>Asegurados<br>Hermosillo</b>",
                "<b>Asegurados en la<br>entidad</b>",
                        "<b>Participación del municipio en la<br>entidad</b>",
                        "<b>Crecimiento<br> anual (%)</b>"
                        ],
                fill_color='#feb24c',
                align='center',
                font_family="Century Gothic",
                font_size=20),
cells=dict(values=[df["year"], df["ta"], df["tot"],
                   df["pct"], df["growth"]],
               fill_color='lavender',
               align='center',
           font_family="Century Gothic",
           font_size=13))
])

#Título
fig.update_layout(
    showlegend=False,
    title_text="<b>Hermosillo. Trabajadores asegurados ante el IMSS en la industria de la construcción<br>"
               "Registro de diciembre de cada año</b>",
    title_font_family="Century Gothic",
    title_font_size=25
)

#Fuente
fig.add_annotation(text="Fuente: @claudiodanielpc con información del Instituto Mexicano del Seguro Social (IMSS). Datos abiertos",
                  x=0, y=0, showarrow=False,
                   font_family="Century Gothic")

#Salvar la tabla como PNG

pio.write_image(fig, "tabla.png",scale=1, width=2000, height=400)
