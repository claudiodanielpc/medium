#Spatial join


##Borrar datos del entorno
rm(list=ls())


#Directorio de trabajo
#Esto se debe de cambiar en cada computadora
setwd("D:/")


# Librerías ====
if(!require('pacman')) install.packages('pacman')
pacman::p_load(tidyverse,sf)


#Url postes
url<-"https://datos.cdmx.gob.mx/dataset/bbbd201b-28fc-4a2b-978b-1968829c1d54/resource/7bb21e65-d6d1-44c3-8db0-ee91012ac2d9/download/wifi_gratuito_en_postes_mi_barrio.csv"
#Marco geo
shape<-"https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/889463807469/09_ciudaddemexico.zip"



#Crear función de descarga estableciendo el directorio de extracción de archivos
descarga<-function(url,directorio){
  temp <- tempfile()
  download.file(url, destfile = temp)
  unzip(temp, 
        exdir = directorio,
        overwrite=TRUE)
  unlink(temp)
}

descarga(shape,getwd())



#Lectura archivo de puntos
gdf<-read.csv(url)%>%
  janitor::clean_names()%>%
  #Transformar a objeto sf
  st_as_sf(coords=c("longitud","latitud"), crs = 4326)



##Lectura de shapes de alcaldías
alc<-st_read("conjunto_de_datos/09mun.shp", options = "ENCODING=WINDOWS-1252")%>%
  janitor::clean_names()%>%
  #Reproyectar
  st_transform(crs = st_crs(gdf))



#Hacer el join
union<-gdf%>%
  st_join(alc, left = TRUE)




