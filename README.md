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


## Gráficas

Esto es replicando lo que mucha gente ha hecho, pero me sirve para aprender. No es mas que las mismas gráficas reimplementadas con los datos que tenemos disponibles. Crea réplicas de los datos en directorios locales.

[Notebook](covid.ipynb)

## Fuentes de datos y Repositorios

- [Sistema Nacional de Vigilancia Epidemiológica (sinave)](https://ncov.sinave.gob.mx/)
- [Mapa de Covid-19 en Méixco](https://ncov.sinave.gob.mx/mapa.aspx)
- [Datos de Johns Hopkins](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
- [Gran trabajo del equipo de @guzmart en capturar los datos oficiales, caso por caso](https://github.com/guzmart/covid19_mex)
- [Waldemar Quevedo, Herramienta para obtener datos recientes sobre la situación de COVID19 en México.](https://wallyqs.github.io/covid19mx/) y su [repositorio](https://github.com/wallyqs/covid19mx)
- [Covidatos de Eli Parra](https://covidatos.mx/), muy buena [hoja de cálculo](https://docs.google.com/spreadsheets/d/1ihdwd-YY5h_wCkaaKVK0P70gjhxxRlLuNLYPQeJwrq8/edit?usp=sharing)
- [Serendipia](https://serendipia.digital/2020/03/datos-abiertos-sobre-casos-de-coronavirus-covid-19-en-mexico/)
- [@covidctdmx](https://twitter.com/covidctdmx) y su [repositorio](https://github.com/covidctdmx/covid_ctd_mx)
- [@mariorz](https://twitter.com/mariorz) series de tiempo en el [repositorio](https://github.com/mariorz/covid19-mx-time-series)

### Otros recursos interesantes
- https://aatishb.com/covidtrends/
- https://bnonews.com/index.php/2020/04/the-latest-coronavirus-cases/
