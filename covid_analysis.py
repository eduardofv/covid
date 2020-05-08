import os
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#from scipy.interpolate import make_interp_spline, BSpline

#get_ipython().run_line_magic('matplotlib', 'inline')
#sns.set(style="whitegrid")
FIGSIZE = [8, 5]
OUTPUT_TYPE = "notebook"

def get_new_per_day(df):
    new_per_day = {}
    for location in df.columns:
        d = df[location]
        dif = [d[i] - d[i-1] for i in range(1,len(d))]
        new_per_day[location] = dif

    df_new_per_day = pd.DataFrame(new_per_day)
    df_new_per_day.index = df.index[1:]
    return df_new_per_day

def load_collection(tables, get_function, tables_names=None):
    collection = {}
    if tables_names is None:
        tables_names = tables
    for index, dset in enumerate(tables):
        t_name = tables_names[index]
        collection[t_name] = get_function(dset)
        collection[f"daily_{t_name}"] = get_new_per_day(collection[t_name])
    return collection

def calculate_new_last_period(df_new_per_day, PERIOD=7):
    new_per_period = {}
    for location in df_new_per_day.columns:
        d = df_new_per_day[location]
        cum = [sum(d[(i-PERIOD):i]) for i in range(PERIOD, len(d))]
        new_per_period[location] = cum
    return new_per_period

def cum_and_new_from_init(cum, new, init=99):
    cum_from_init = cum[cum > init]
    new_from_init = new[-len(cum_from_init):]
    assert len(cum_from_init) == len(new_from_init)
    return cum_from_init, new_from_init

def get_values_since_first_geq(values, min_value):
    for index, value in enumerate(values):
        if value >= min_value:
            return values[index:]
    return pd.Series([], dtype='int')

def get_values_since(series, min_value, fill_to=None):
    series = get_values_since_first_geq(series, min_value)
    if fill_to is not None:
        series = pd.Series(list(series) + [0] * (fill_to - len(series)))
    return series.reset_index(drop=True)

#Splines: https://stackoverflow.com/questions/5283649/plot-smooth-line-with-pyplot
#def smooth_plot(data, num_points=300, k=3):
#    xnew = np.linspace(d.index.min(), d.index.max(), num_points) 
#    spl = make_interp_spline(d.index, d, k=k)  # type: BSpline
#    power_smooth = spl(xnew)
#    plt.plot(power_smooth)

def smooth_plot(data, window):
    data = data.rolling(window=window).mean()
    plt.plot(data)
    
def graph_daily_metric(df, 
                       since=None,
                       min_y=0,
                       log=False, 
                       ylabel=None, 
                       smooth=False,
                       smooth_window=7,
                       image_fn="output.png"):
    xlabel = None
    f, ax = plt.subplots(figsize=FIGSIZE)
    if log:
        ax.set(yscale='log')
        ylabel += " (log)"
    for location in df.columns:
        d = df[location]
        if since is not None:
            d = get_values_since(d, since)
            xlabel = f"days since {since} cases"
        d[d < min_y] = np.NaN
        #print(d)
        if smooth:
            smooth_plot(d, window=smooth_window)
        else:
            sns.lineplot(x=d.index, y=d)
    ax.set(ylabel=ylabel)
    if xlabel is not None:
        ax.set(xlabel=xlabel)
    else:
        plt.xticks(rotation=45)
    plt.legend(df.columns)
    if OUTPUT_TYPE == 'markdown':
        plt.savefig(f"img/{image_fn}")

#test
#graph_daily_metric(world['daily_deaths'][["Mexico", "Italy", "Australia"]],
#                   since=3,
#                   smooth=True,
#                   log=True)
#plt.show()

def analysis(datasets, 
             locations, 
             metric,
             show_last_days=14,
             log = True,
             since=100, 
             smooth=True, 
             smooth_window=7,
             image_fn="output.png"):
    data = datasets[metric][locations]
    label = f"{metric}"
    graph_daily_metric(data,
                       log=log,                   
                       since=since,
                       ylabel=label,
                       smooth=smooth,
                       smooth_window=smooth_window,
                       image_fn=image_fn)
    if OUTPUT_TYPE == 'notebook':
        display(data.tail(show_last_days))
    else:
        return data.tail(show_last_days)

#Genius Eric & Aatish: https://aatishb.com/covidtrends/
def trajectories(datasets, locations, metric, new_metric=None, since=50, window=7):
    f, ax = plt.subplots(figsize=FIGSIZE)
    if new_metric is None:
        new_metric = f"daily_{metric}"
    ax.set(yscale="log", xscale="log")
    for location in locations:
        data = get_values_since(datasets[metric][location], since)
        cum = data
        new = datasets[new_metric][location][-len(data):].rolling(window=window).sum()
        plt.plot(cum[-len(new):], new)
    plt.legend(locations)
    plt.xlabel(f"total {metric} cases (log)")
    plt.ylabel(f"{new_metric} last {window} days (log)")

JH_DATASETS = ['confirmed', 'deaths', 'recovered']
def transform_johns_hopkins(df):
    df = df.groupby('Country/Region').sum()
    cols = list(df.columns)
    cols.remove('Lat')
    cols.remove('Long')
    df = df[cols]
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format='%m/%d/%y')
    df.index.name = "Date"
    return df#[columns]

def get_johns_hopkins(kind='confirmed'):
    assert kind in JH_DATASETS
    url = f"https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_{kind}_global.csv"
    df = pd.read_csv(url)
    df = transform_johns_hopkins(df)
    fname = f"data/CSSEGUSandData/time_series_covid19_{kind}_global.csv"
    df.to_csv(fname)
    return df

def load_johns_hopkins():
    return load_collection(JH_DATASETS, get_johns_hopkins)

def transform_timeseries(df, state_column='Estado', date_format='%Y/%m/%d'):
    df = df.groupby(state_column).sum()
    df = df.transpose()
    df.index = pd.to_datetime(df.index, format=date_format)
    df.index.name = "Date"
    return df#[columns]

SINAVE_DATASETS = ['confirmados', 'probables', 'muertos', 'descartados']

def get_sinave_eduardofv(kind="confirmados"):
    assert kind in SINAVE_DATASETS
    url = f"https://raw.githubusercontent.com/eduardofv/covid/master/data/sinave_agregados/series_tiempo/serie_tiempo_{kind}.csv"
    df = pd.read_csv(url)
    df = transform_timeseries(df)
    return df

def load_sinave():
    return load_collection(SINAVE_DATASETS, get_sinave_eduardofv)

MARIORZ_DATASETS = ['confirmed', 'suspects', 'deaths', 'negatives']

def get_mariorz(kind):
    url = f"https://raw.githubusercontent.com/mariorz/covid19-mx-time-series/master/data/covid19_{kind}_mx.csv"
    df = pd.read_csv(url)
    df = transform_timeseries(df, date_format='%d-%m-%Y')
    return df

def load_mariorz():
    return load_collection(
        MARIORZ_DATASETS,
        get_mariorz,
        tables_names=SINAVE_DATASETS)
