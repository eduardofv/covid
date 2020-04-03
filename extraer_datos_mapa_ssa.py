import sys
import os
import re
import datetime
import locale
import json
import requests
import pandas as pd

locale.setlocale(locale.LC_ALL, 'es_MX.utf8')


def get_last_update_time():
    url = "http://ncov.sinave.gob.mx/mapa.aspx"
    headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            #'Origin': 'http://ncov.sinave.gob.mx',
            #'Referer': 'http://ncov.sinave.gob.mx/mapa.aspx',
            'Accept-Language': 'en-US,en;q=0.9,es-419;q=0.8,es;q=0.7,gl;q=0.6',
            #'Cookie': 'acceptcookiefreecounterstat=ok; counter=062a8dcced58cba87445df457640d3dc; counter_nv=062a8dcced58cba87445df457640d3dc;'
    }

    r = requests.get(url, headers=headers)
    date_search = re.search('corte a las (.*)";', r.text)
    date_str = date_search.group(1)
    data_date = datetime.datetime.strptime(date_str, "%H:%M  hrs, %d de %B de %Y")
    return data_date


def get_data():
    """Traer datos de SINAVE, scrappeados del mapa"""
    url = 'https://ncov.sinave.gob.mx/Mapa.aspx/Grafica22'
    headers = {
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'http://ncov.sinave.gob.mx',
            'Referer': 'http://ncov.sinave.gob.mx/mapa.aspx',
            'Accept-Language': 'en-US,en;q=0.9,es-419;q=0.8,es;q=0.7,gl;q=0.6',
            'Cookie': 'acceptcookiefreecounterstat=ok; counter=062a8dcced58cba87445df457640d3dc; counter_nv=062a8dcced58cba87445df457640d3dc; acceptcookie=ok.'
    }

    r = requests.post(url, headers=headers)
    #Guardar una copia antes de que pase otra cosa
    fname = f"data/sinave/fuente/datos_sinave-{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(fname, 'w') as fo:
        fo.write(r.text)
    return r.json()['d']

#def get_data_local():
#    with open("datos_sinave-20200403_1116.json") as fin:
#        r = json.loads(fin.read())
#    return r['d']


def save_daily(df, current_time, last_update_time):
    current = current_time.strftime('%Y-%m-%d_%H%M')
    if last_update_time is None:
        last_update = "DATE_NOT_FOUND"
    else:
        last_update = last_update_time.strftime('%Y-%m-%d_%H%M')
    fname = f"data/sinave/reporte_diario/{last_update}.csv"
    df.to_csv(fname)


def update_time_series(df, current_time, last_update_time):
    for col in ['confirmados', 'descartados', 'muertos', 'probables']:
        fname = f"data/sinave/series_tiempo/serie_tiempo_{col}.csv"
        last_update = last_update_time.strftime("%Y-%m-%d")
        if os.path.isfile(fname):
            d = pd.read_csv(fname, index_col=0)
            d[last_update] = df[col]
        else:
            d = pd.DataFrame({last_update: df[col]})
            d.index = df.index
        d.to_csv(fname)


#TODO: Cambiar por logging
def msg(str):
    print(str)

def main():
    current_time = datetime.datetime.today()

    msg("Leyendo datos del mapa")
    data = get_data()

    msg("Obteniendo fecha de actualizacion")
    last_update_time = get_last_update_time()
    if last_update_time is None:
        raise AttributeError("No se pudo recuperar la fecha de actualizacion.")

    msg("Procesando datos")
    original = json.loads(data)
    data = {}
    for item in original:
        data[item[1]] = {
            'ultima_actualizacion': last_update_time.strftime('%Y-%m-%d %H:%M'),
            'probables': int(item[6]),
            'confirmados': int(item[4]),
            'descartados': int(item[5]),
            'muertos': int(item[7])
        }
    df = pd.DataFrame(data).transpose().sort_index()
    df.index.name = "Estado"

    msg("Guardando datos diarios")
    save_daily(df, current_time, last_update_time)

    msg("Guardando series de tiempo")
    update_time_series(df, current_time, last_update_time)
    #print(df)

try:
    main()
except:
    msg("Unexpected error:", sys.exc_info()[0])
