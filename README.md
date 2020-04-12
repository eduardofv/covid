# COVID-19 

## Datos de COVID-19 por Estado en México

Tratando de ayudar a quien le puedan ser útiles estos datos ya que los formatos en que [Secretaría de Salud los ha estado publicando](https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449) 
no son los mejores para análisis y visualización.

Los siguientes datos son "semioficiales" ya que son extraídos del [mapa de México](https://ncov.sinave.gob.mx/mapa.aspx) 
en el sitio del **Sistema Nacional de Vigilancia Epidemiológica**. Los datos son almacenados tal como se extraen
del mapa y luego son procesados para generar archivos en un formato *similar* a los publicados en el repositorio de 
[Johns Hopkins](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series):

- [Reporte diario](data/sinave/reporte_diario) contiene un archivo CSV por día con los números
a la fecha, por estado, con las siguientes columnas:
    - Casos probables
    - Casos confirmados
    - Casos descartados
    - Fallecimientos
    
- [Series de Tiempo](data/sinave/series_tiempo) contiene archivos CSV con datos agregados en forma de series 
de tiempo (un día por columna) por cada Estado, para cada una de las categorías:
    - [Casos probables](data/sinave/series_tiempo/serie_tiempo_probables.csv)
    - [Casos confirmados](data/sinave/series_tiempo/serie_tiempo_confirmados.csv)
    - [Casos descartados](data/sinave/series_tiempo/serie_tiempo_descartados.csv)
    - [Fallecimientos](data/sinave/series_tiempo/serie_tiempo_muertos.csv)

- [Series de Tiempo con datos adicionales](data/sinave_agregados/series_tiempo) contiene archivos equivalentes a los 
mencionados arriba pero con tres días anteriores agregados del [repositorio de @wallyqs](https://github.com/wallyqs/covid19mx). 
Los datos scrapeados por este proyecto los voy a mantener en el directorio original. 
- [Datos originales](data/sinave/fuente) contiene una copia de los datos tal como fueron extraídos del mapa. 
La última versión del archivo se guarda con 'latest' y las versiones anteriores se pueden acceder mediante commits anteriores. 
Hasta el 2020-04-05 se guardaba un archivo con timestamp: el nombre es un *timestamp* del momento de la extracción. 
    
Los datos son extraídos automáticamente 2 veces al día esperando tener los mas actualizados lo antes posible. 

**Limitante** Los datos están disponibles a partir del día que inicié este proyecto el 2 de Abril de 2020. 
Hay 3 días adicionales de datos en el directorio secundario [data/sinave_agregados]()


## Gráficas

Este [notebook](covid.ipynb) tiene mis gráficas que son en realidad reimplementaciones de las que se pueden encontrar en muchos lados con los datos aquí disponibles. El dato mas interesante es el del número de casos de prueba reportados por día.

Una copia **actualizada automáticamente dos veces al día** se puede consultar en este [notebook](covid.nbconvert.ipynb).

## Directorio de fuentes de datos, repositorios y visualizaciones sobre COVID-19 en México

Estoy manteniendo este repostorio [directorio_covid19_mx](https://eduardofv.github.io/directorio_covid19_mx/) apuntando a esfuerzos comunitarios de interpretación, transformación y almacenamiento de los datos oficiales. 

## Fuentes de datos 

- [Sistema Nacional de Vigilancia Epidemiológica (sinave)](https://ncov.sinave.gob.mx/)
- [Mapa de Covid-19 en México](https://ncov.sinave.gob.mx/mapa.aspx)
- [Comunicado Técnico Diario, Dirección General de Epidemiología](https://www.gob.mx/salud/documentos/coronavirus-covid-19-comunicado-tecnico-diario-238449)
- [Datos de Johns Hopkins](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
