#Api INEGI. Banco de Indicadores


##Paquetería necesaria
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse, httr, jsonlite, plotly)




#URl con API KEY

key="tu_llave"
url = paste0("https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1003000001/es/0700/false/BISE/2.0/",
             key,"?type=json")

#Respuesta
res=GET(url)


#Obtenemos la respuesta de la API y la pasamos a JSON
vivienda <-content(res, as = 'text')%>%
fromJSON()%>%
  #Se extrae elemento "Series"
  pluck("Series")%>%
  #Se extraen el elemento "OBSERVATIONS" que es aquel que contiene los datos
  pluck("OBSERVATIONS")%>%
  #Se transforma a dataframe y se limpian los nombres
  as.data.frame()%>%
  janitor::clean_names()%>%
  #Se seleccionan las variables requeridas
  select(time_period, obs_value)%>%
  #Se transforman a numérico y renombran
 mutate_all(as.numeric)%>%
  rename(year=1,
         vivi=2
         )%>%
  #Dato de vivienda en millones
  mutate(vivi=vivi/1000000)


#Gráfico de barras plano con ggplot2
g1<-
  ggplot(vivienda, aes(year, vivi)) +
  geom_col(fill="#285C4D")+
  theme_minimal()+
  theme(legend.title = element_blank(),
        axis.text.x = element_text(angle = 90, vjust = 0.5))


##Gráfico plano a plotly
grafi<-ggplotly(g1,width = 900, height = 500)%>%

  layout(title=list(text="<b>Viviendas particulares habitadas en Mexico</b><br><i>1990-2020</i>", 
                    x = 0,
                    font=list(family = "Montserrat",
                              size = 20,
                              color = 'black')),
         xaxis = list(title = "Años"),
         yaxis = list(title = "Viviendas particulares habitadas (millones)",
                      tickformat=".1f%"
                      ),
         dragmode="pan",
         annotations =
           list(x = 0, y = 0, text = "Fuente: @claudiodanielpc con información de INEGI.", 
                showarrow = F, xref='paper', yref='paper', 
                xanchor='left', yanchor='auto', xshift=0, yshift=0,
                font=list(size=8, color="black")))


###Credenciales para subir gráfica generada a cuenta de Chart Studio
Sys.setenv("plotly_username"="tu_usuario_chartstudio")
Sys.setenv("plotly_api_key"="tu_llave_chartstudio")
#Guardar en cuenta de Chart Studio
api_create(grafi, "vivparhab",
           fileopt = "overwrite"
           )
