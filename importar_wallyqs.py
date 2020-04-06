"""
Importar los datos del repositorio de @wallysqs con los datos
que me faltaban. Estos los guardamos en un directorio distinto
(sinave_agregados) para no mezclar
"""
import requests
import pandas as pd

tipos = ['confirmados', 'descartados', 'muertos', 'probables']
eq = {
    'confirmados': 'positive',
    'descartados': 'negative',
    'probables': 'suspect',
    'muertos':'deaths'
}

series = {}

for serie in tipos:
    fname = f"data/sinave/series_tiempo/serie_tiempo_{serie}.csv"
    series[serie] = pd.read_csv(fname, index_col=0)

for day in ['2020-03-30', '2020-03-31', '2020-04-01']:
    url = f"https://raw.githubusercontent.com/wallyqs/covid19mx/master/data/{day}.json"
    data = requests.get(url).json()
    for serie in tipos:
        series[serie][day] = [0]*32
        for estado in data['states']:
            series[serie].at[estado['name'], day] = int(estado[eq[serie]])

for serie in tipos:
    columns = sorted(series[serie].columns[1:])
    series[serie] = series[serie].reindex(columns, axis=1)
    series[serie].to_csv(f"data/sinave_agregados/series_tiempo/serie_tiempo_{serie}.csv")


