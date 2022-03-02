
#Librerías
if(!require('pacman')) install.packages('pacman')
pacman::p_load(pdftools, tidyverse)
#URL del PDF
pdf_file <- "https://sistemas.sedatu.gob.mx/repositorio/proxy/alfresco-noauth/api/internal/shared/node/Vm8Q6lnjQ-am9z2of4LgcQ/content/S177_PVS_Poblacion_potencial_objetivo_2020.pdf"

##Etraemos texto de página 5 del pdf
df <- pdf_text(pdf_file)[[5]]%>%
  #Quitamos caracteres
  str_split("\n") %>%
  #Pasar a tibble
  as_tibble(.name_repair = make.names)%>%
  ##Creamos columnas extrayendo la información del texto original
  mutate(
    concepto = str_sub(X, 0, 20),
    hogares=str_sub(X,70,80),
    poblacion=str_sub(X,85,100)
    
    )%>%
  #Eliminamos texto original
  select(-X) %>%
  # Se quitan espacios
  mutate_all(str_trim)%>%
  #Seleccionamos filas donde están los datos
  slice(11:16)%>%
  ##Se transforma a numérico
  mutate(
  hogares=as.numeric(gsub(",","",hogares)),
  poblacion=as.numeric(gsub(",","",poblacion)))
  
