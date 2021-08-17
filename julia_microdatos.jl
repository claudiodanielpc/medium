#Cargamos los paquetes que requerimos
import Pkg
Pkg.add(["CSV", "ZipFile","HTTP", "DataFrames", 
"DataFramesMeta", "StatsBase"])
using CSV, ZipFile, HTTP, DataFrames, DataFramesMeta, StatsBase


#Cargamos el conjunto de datos de INEGI con el que vamos a trabajar
url = "https://www.inegi.org.mx/contenidos/programas/enigh/nc/2020/microdatos/enigh2020_ns_viviendas_csv.zip"
data = HTTP.get(url)
r = ZipFile.Reader(IOBuffer(data.body))
archivo = r.files[1]
enigh = CSV.read(archivo,
 DataFrame)


#Generamos una varibale con las condiciones de calidad y espacios de la vivienda

#enigh.mat_pisos = replace(enigh.mat_pisos, "&" => missing)
#enigh.mat_pisos = passmissing(parse).(Int128,enigh.mat_pisos)


enigh = @linq enigh |>
    transform(car = ifelse.((:mat_pisos .== "1") .| (:mat_techos .<=2) .| (:mat_pared .<=5)
    .| ((:tot_resid ./ :num_cuarto) .>2.5), 
    "carencia", "sin carencia"))

    #Resultado
combine(groupby(enigh,[:car]), [:tot_resid, :factor] => ((x, y) -> sum(x, fweights(y))) => :personas)

