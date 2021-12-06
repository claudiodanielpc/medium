##Borrar datos del entorno
rm(list=ls())
# Librerías ====
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse,highcharter)


url="https://sistemas.sedatu.gob.mx/repositorio/proxy/alfresco-noauth/api/internal/shared/node/KbriVQ8FRHiEHPhMeHNpyA/content/Financiamientos_202108.csv?6&a=true"



#Leemos archivo del SNIIV
sniiv<-read.csv(url)
  
#Generación de nodos
#Primer nodo: De organismo a modalidad
nodo1<-sniiv%>%  
  #filtramos por créditos individuales
  filter(tipo_de_credito=="Credito individual")%>%
  #Agrupamos y generamos primer nodo
  group_by(organismo,modalidad)%>%
  summarise(acc=sum(acciones))%>%
  #Desagrupamos
  ungroup()%>%

#Renombrar variable
  rename(
    origen=1,
    destino=2
    
  )
  
  
#  Segundo nodo: de modalidad a rangos de ingresos
nodo2<-sniiv%>%
  #filtramos por créditos individuales
  filter(tipo_de_credito=="Credito individual")%>%
  #Agrupamos y generamos primer nodo
  group_by(modalidad,rango_de_ingresos_uma)%>%
  summarise(acc=sum(acciones))%>%
  ungroup()%>%

  rename(
    origen=1,
    destino=2
    
  )
  
#Juntamos ambos nodos para poder graficar
sankeysniiv<-rbind(nodo1,nodo2) 


  #Higchart

#Se define Sankey y los nodos
grafhc<-hchart(sankeysniiv, "sankey", name = "Créditos individuales", hcaes(from=origen,
                                                                to=destino,
                                                                  weight=acc)
         
         )%>%
  #Títulos, subtítulos y fuente
  
    hc_title(text= "Distribución de créditos individuales para soluciones habitacionales") %>%
    hc_subtitle(text= "enero-agosto 2021")%>%
    hc_caption(text = "Fuente: @claudiodanielpc con información de SEDATU. Sistema Nacional de Información e Indicadores de Vivienda (SNIIV)")%>%

  #Tema de The Economist
      hc_add_theme(hc_theme_economist())
  
#Guardar como html y posteriormente, como PNG
  
  htmlwidgets::saveWidget(grafhc,file = "dataviz/sniivsankey.html")
  webshot::webshot(url = "dataviz/sniivsankey.html", 
          file = "dataviz/sniivsankey.png",
          delay=3, vwidth = 992,vheight = 744)
  
  #Visualizar highchart
  grafhc
  