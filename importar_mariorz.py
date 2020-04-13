"""
Importar los datos del repositorio de @mariorz con los datos
que me faltaban. Estos los guardamos en un directorio distinto
(sinave_agregados) para no mezclar
"""
import requests
import pandas as pd

eq = {
    'confirmados': 'confirmed',
    'descartados': 'negatives',
    'probables': 'suspects',
    'muertos':'deaths'
}

series = {}

for serie in eq.keys():
    fname = f"data/sinave/series_tiempo/serie_tiempo_{serie}.csv"
    series[serie] = pd.read_csv(fname, index_col=0)

    mariorz = pd.read_csv(f"../mariorz/data/covid19_{eq[serie]}_mx.csv")
    mariorz = mariorz.set_index('Estado')
    mariorz.columns = pd.to_datetime(mariorz.columns, format="%d-%m-%Y")
    mariorz = mariorz[mariorz.columns[mariorz.columns < '2020-04-02']]
    mariorz.columns = mariorz.columns.strftime('%Y-%m-%d')
    mariorz = mariorz.merge(series[serie], on="Estado")
    series[serie] = mariorz
    series[serie].to_csv(f"data/sinave_agregados/series_tiempo/serie_tiempo_{serie}.csv")
