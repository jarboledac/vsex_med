import pandas as pd
import numpy as np 
import datetime
import os
from funciones import *
from zipfile import ZipFile


PATH_FOLDER = "raw/"
PATH_FILE = os.listdir(PATH_FOLDER)

for path in PATH_FILE:
    if "victima" in path:
        PATH_VIC = path
    elif "indiciado" in path:
        PATH_IND = path
    elif "relacion" in path:
        PATH_REL = path
    else:
        pass

fecha_inicial = '31-12-2017'
fecha_final = '01-01-2022'
meses = [3, 9, 12]
name_mes = {1 :"Ene",
            2: "Feb",
            3: "Mar",
            4: "Abr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Agos",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dic"
}

assert PATH_VIC.split('.')[-1] == "xlsx"
assert PATH_IND.split('.')[-1] == "xlsx"
assert PATH_REL.split('.')[-1] == "xlsx"


ARTICULOS_DELITO_SEXUAL = ['188a. Trata de personas', '205. Acceso carnal violento',
                           '206. Acto sexual violento',
                           '207. Acceso carnal o acto sexual en persona puesta en incapacidad de resistir',
                           '208. Acceso carnal abusivo con menor de catorce años',
                           '209. Actos sexuales con menor de catorce años',
                           '210. Acceso carnal o acto sexual abusivos con incapaz de resistir',
                           '210a. Acoso sexual', '213. Inducción a la prostitución',
                           '213a. Proxenetismo con menor de edad',
                           '214. Constreñimiento a la prostitución',
                           '217. Estimulo a la prostitución de menores',
                           '217a. Demanda de explotación sexual comercial de persona menor de 18 años de edad',
                           '218. Pornografía con personas menores de 18 años',
                           '219. Turismo sexual',
                           '219a. Utilización o facilitación de medios de comunicación para ofrecer actividades sexuales con personas menores de 18 años'
                           ]

# usecols=["fecha_ultimo_hecho", "spoa", "edad", "municipio_hecho", "delito"]
#LOAD AND FILTER
data = pd.read_excel(PATH_FOLDER + PATH_VIC, index_col= 0)
data = data[data.municipio_hecho == "Medellín"]
data['filtro'] = data.delito.str.contains('|'.join(ARTICULOS_DELITO_SEXUAL),regex=True)
data = data[data.filtro == True]
data = data.reset_index(drop=True)

#NEW COLUMNS
data['fecha_uh'] =  pd.to_datetime(data['fecha_ultimo_hecho'], errors = "coerce")
data = data[(data.fecha_uh > fecha_inicial)&(data.fecha_uh < fecha_final)]

data['rango_edad'] = [edad_ran(x) for x in data['edad']]
data['year'] = data.fecha_uh.dt.year
data['mes'] = data.fecha_uh.dt.month
data['dia'] = data.fecha_uh.dt.day
data['day_name'] = [x.day_name() for x in data['fecha_uh']]

data2 = pd.read_excel(PATH_FOLDER + PATH_IND, index_col= 0)
data2 = data2[data2.spoa.isin(data.spoa)]

merg1 = data[['spoa','fecha_ultimo_hecho','year','dia']]
merg1.drop_duplicates(subset=['spoa'],inplace = True)

merg2 = data2[['spoa','sexo','numero_documento','edad']]
merge_bt = pd.merge(merg2,merg1, on ='spoa', how = "inner")
merge_bt.fillna("SIN DATO", inplace=True)

merge_bt.drop_duplicates(subset =['numero_documento'],inplace=True)

indi_anio =merge_bt.groupby(by = ['year']).count()['numero_documento']
indi_sexo = merge_bt.groupby(by = ['sexo']).count()['numero_documento']

merge_bt.edad.replace(-1,99, inplace=True)
merge_bt['rango_edad'] = [edad_ran(x) for x in merge_bt['edad']]

indi_edad = table_pv(merge_bt,'rango_edad','year')

writer = pd.ExcelWriter('refined/tablas_indi.xlsx', engine='xlsxwriter')

indi_anio.to_excel(writer, sheet_name="indi_anio")
indi_sexo.to_excel(writer, sheet_name="indi_sexo")
indi_edad.to_excel(writer, sheet_name="indi_edad")

writer.save()