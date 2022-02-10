import pandas as pd
import numpy as np 
import datetime
import os
from funciones import *
from zipfile import ZipFile


PATH_FOLDER = "datos/"
PATH_FILE = os.listdir(PATH_FOLDER)[0]
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

assert PATH_FILE.split('.')[-1] == "xlsx"

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
data = pd.read_excel(PATH_FOLDER + PATH_FILE, index_col= 0)
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

#CONTEO POR AÑO
count_year = table_pv(data, 'mes','year')
count_year.index =['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'] #tabla
graph_sisc(count_year, "acumulado_anio","Casos mes a mes - 2018-2021")

#APARICION DELITOS GENERAL
del_gen = apar_del(data)

count_day_gn = table_pv(data,"day_name","year").fillna(0).astype('int64') #tabla
count_day_gn.index = [5,1,6,7,4,2,3]
count_day_gn = count_day_gn.sort_index(ascending = True) 
count_day_gn.index = ['Lun','Mar','Mier','Juev','Vier','Sab','Dom']
bar_sisc(count_day_gn,"distri_dias" ,"Distribución por días general")

count_sex_gn = table_pv(data, 'sexo', "year").fillna(0).astype('int64') #tabla
bar_sisc(count_sex_gn,"distri_sexo" ,"Distribución por sexo")

count_edad_gn = table_pv(data, "rango_edad", "year").fillna(0).astype('int64') # tabla
bar_sisc(count_edad_gn,"distri_rango_edad" ,"Distribución por rango de edad")

casos_mes = {}
delitos_mes = {}
casos_dia = {}
casos_sex = {}
casos_edad = {}
for mes in meses:
    data_m = data[data.mes == mes]
    count_day_m =table_pv(data_m, 'dia', "year").fillna(0).astype('int64')
    casos_mes[mes] = count_day_m
    graph_sisc(count_day_m, "acumulado_dia_"+name_mes[mes].lower(),"Casos dia a dia mes de "+name_mes[mes].lower())
    del_mes = apar_del(data_m)
    delitos_mes[mes] = del_mes
    count_day_m = table_pv(data_m, 'day_name', "year").fillna(0).astype('int64')
    count_day_m = ord_sema(count_day_m)
    casos_dia[mes] = count_day_m
    bar_sisc(count_day_m,"distri_dias_" + name_mes[mes].lower(),"Distribución por dias mes de "+name_mes[mes].lower())
    count_sex_m = table_pv(data_m, 'sexo', "year").fillna(0).astype('int64')
    casos_sex[mes] = count_sex_m
    bar_sisc(count_sex_m,"distri_sex_" + name_mes[mes].lower(),"Distribución por sexo mes de "+name_mes[mes].lower())
    count_edad_m = table_pv(data_m, 'rango_edad', "year").fillna(0).astype('int64')
    casos_edad[mes] = count_edad_m
    bar_sisc(count_edad_m,"distri_edad_" + name_mes[mes].lower(),"Distribución por rango de edad de "+name_mes[mes].lower())


writer = pd.ExcelWriter('salida/tablas.xlsx', engine='xlsxwriter')

count_year.to_excel(writer, sheet_name = "casos_anio_gn")
count_day_gn.to_excel(writer, sheet_name = "casos_dia_gn")
count_sex_gn.to_excel(writer, sheet_name = "casos_sex_gn")
count_edad_gn.to_excel(writer, sheet_name = "casos_edad_gn")
del_gen.to_excel(writer, sheet_name= "delitos_general")

for num in meses:
    casos_mes[num].to_excel(writer, sheet_name = "casos_mes_"+name_mes[num])
    delitos_mes[num].to_excel(writer, sheet_name = "delitos_mes_"+name_mes[num])
    casos_dia[num].to_excel(writer, sheet_name = "casos_dia_"+name_mes[num])
    casos_sex[num].to_excel(writer, sheet_name = "casos_sex_"+name_mes[num])
    casos_edad[num].to_excel(writer, sheet_name = "casos_edad_"+name_mes[num])

writer.save()



directory = './salida'
file_paths = get_all_file_paths(directory)
print('Following files will be zipped:')
for file_name in file_paths:
    print(file_name)

with ZipFile('data_files.zip','w') as zip:
    for file in file_paths:
        zip.write(file)

print('All files zipped successfully!')

for files in file_paths:
    os.remove(files)
    print("removed{}".format(files))

#df1.to_excel(writer, sheet_name='Sheet1')






#print(count_year)
#data['year'] = data.Mycol.dt.year
