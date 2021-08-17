#Librerías
import pandas as pd
import tabula
import matplotlib.pyplot as plt
import numpy as np


#URL PDF CIDE
url="https://www.cide.edu/wp-content/uploads/2021/04/Proceso_admision_2021_MAPP-1.pdf"

###Importar solo la primera tabla

df = tabula.read_pdf(url,
                   pages=1, lattice=True)

#Transformamos el objeto a dataframe
df = pd.DataFrame(np.array(df).reshape(27,4))


#Renombrar columnas

df= df.rename(columns={df.columns[0]: 'folio',
                   df.columns[1]: 'cuanti',
                   df.columns[2]: "analit",
                   df.columns[3]: "ensayo"})

#Graficamos ejemplo de habilidades cuantitativas de la
#Maestría en Administración y Políticas Públicas 2021

#Histograma

#Definición de la figura
fig, ax = plt.subplots(figsize=(10, 8))

#Fuente del gráfico
plt.rcParams["font.family"] = "Montserrat"

plt.hist(df["cuanti"],
         facecolor='#7fcdbb',
         alpha=0.75,
         edgecolor='#e0e0e0',
         linewidth=0.5
         )
#Línea de la media
plt.axvline(df["cuanti"].mean(), color='k',
            linestyle='dashed', linewidth=1)

#Textos en el gráfico

min_ylim, max_ylim = plt.ylim()
#Total de observaciones
plt.text(df["cuanti"].mean()*1.01, max_ylim*0.9,
         'Observaciones: {:.0f}'.format(df["cuanti"].count()))

#Media de calificaciones
plt.text(df["cuanti"].mean()*1.01, max_ylim*0.86,
         'Media: {:.2f}'.format(df["cuanti"].mean()))


#Títulos de ejes
plt.xlabel('Calificaciones')
plt.ylabel('Frecuencia')

#Título del gráfico
plt.title("Centro de Investigación y Docencia Económicas\n"
          "Maestría en Administración y Políticas Públicas, 2021\n"
          "Histograma de calificaciones de habilidades cuantitativas\n")
#Cuadrícula del gráfico
plt.grid(True)

#Mostrar gráfico
plt.show()
