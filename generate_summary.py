#pip install tabulate
import sys
from string import Template
import pandas as pd
import seaborn as sns
import covid_analysis as ca

#sns.set(style="whitegrid")
estados_analisis = ["Ciudad de México", "Nuevo León", "Jalisco", "Queretaro"]

ca.OUTPUT_TYPE = "markdown"

res = {}
estados = ca.load_sinave()
mexico = {}
for ds_name, ds in estados.items():
    mexico[ds_name] = pd.DataFrame({'Mexico': ds.sum(axis=1)})
mexico['pruebas'] = mexico['confirmados'].add(mexico['probables']).add(mexico['descartados'])
mexico['daily_pruebas'] = mexico['daily_confirmados'].add(mexico['daily_probables']).add(mexico['daily_descartados'])

#Resumen
res['actualizacion'] = mexico['confirmados'].index[-1].strftime("%d-%m-%Y")
res['confirmados'] = sum(mexico['confirmados'].iloc[-1])
res['nuevos_confirmados'] = sum(mexico['daily_confirmados'].iloc[-1])
res['muertos'] = sum(mexico['muertos'].iloc[-1])
res['nuevos_muertos'] = sum(mexico['daily_muertos'].iloc[-1])

for metric in ['confirmados', 'muertos', 'pruebas']:
    res[f"tabla_{metric}_ac"] = ca.analysis(mexico, ["Mexico"], metric, log=True, smooth=False, since=1, image_fn=f"mex_{metric}_ac.png").to_markdown()
    res[f"grafica_{metric}_ac"] = f"img/mex_{metric}_ac.png"

    res[f"tabla_{metric}_dia"] = ca.analysis(mexico, ["Mexico"], f"daily_{metric}", since=1, smooth=False, log=False, image_fn=f"mex_{metric}_dia.png").to_markdown()
    res[f"grafica_{metric}_dia"] = f"img/mex_{metric}_dia.png"

with open('summary_template.md') as fin:
    template = fin.read()

with open(sys.argv[1], 'w') as fout:
    fout.write(Template(template).substitute(res))

