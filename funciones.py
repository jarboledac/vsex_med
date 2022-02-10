from tkinter import font
import pandas as pd
import matplotlib.pyplot as plt
import os


def edad_ran(x):
    if 0 <= x < 99:
        JORNADA_BINS = (14, 18, 28, 59, 99)
        JORNADA_LABELS = ('0-14', '15-18', '19-28', '29-59', '60+')
        if x <= JORNADA_BINS[0]:
            salida = JORNADA_LABELS[0]
        elif x<=JORNADA_BINS[1]:
            salida = JORNADA_LABELS[1]
        elif x<=JORNADA_BINS[2]:
            salida = JORNADA_LABELS[2]
        elif x <= JORNADA_BINS[3]:
            salida = JORNADA_LABELS[3]
        else:
            salida = JORNADA_LABELS[4]
        return salida
    elif x >= 99:
        salida ='Sin dato'
        return salida
    else:
        raise ValueError(x)



def jornada(x):
    if 0 <= x <= 23:
        JORNADA_BINS = (5, 11, 17, 23)
        JORNADA_LABELS = ('Madrugada', 'Mañana', 'Tarde', 'Noche')
        if x <= JORNADA_BINS[0]:
            salida = JORNADA_LABELS[0]
        elif x<=JORNADA_BINS[1]:
            salida = JORNADA_LABELS[1]
        elif x<=JORNADA_BINS[2]:
            salida = JORNADA_LABELS[2]
        else:
            salida = JORNADA_LABELS[3]
        return salida
    elif x >= 24:
        salida = 'Sin dato'
        return salida


def table_pv(data,index, column):
      return pd.pivot_table(data, index = index, columns= column,aggfunc='count')['spoa']

def graph_sisc(table, name, titulo):
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#191B4F','#1CA4C9','#511C71','#515151','#F9A61F','#178D4B','#AE3E92','#F77F11']) 
    fig, ax = plt.subplots(figsize=(20,7), dpi = 80)
    for x in table.columns:
        plt.plot(table.index,table[x],'-o', linewidth =4, markeredgewidth =10)
    ax.legend(table.columns, loc = (0.0,-0.2), ncol = 4,handlelength = 3, handletextpad =2, fontsize = 30, frameon = False)
    ax.set_title(titulo, fontsize = 20)
    plt.savefig("salida/"+name + '.jpg',bbox_inches='tight')

def bar_sisc(data, name, title):
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=['#191B4F','#1CA4C9','#511C71','#515151','#F9A61F','#178D4B','#AE3E92','#F77F11']) 
    fig = data.plot.bar(title = title)
    fig.axes.title.set_size(15)
    plt.savefig("salida/"+name + '.jpg',bbox_inches='tight')
    

def apar_del(data):
    delito  = {}
    for dat in data['delito']:
        lt = dat.strip().split(',')
        for val in lt:
            if val.strip() in delito.keys(): 
                delito[val.strip()]+=1
            else:
                delito[val.strip()] = 1
    delito_df = pd.DataFrame.from_dict(delito, orient='index', columns = ['apariciones'])
    delito_df.sort_values(by = 'apariciones', inplace = True, ascending = False)
    return delito_df

def ord_sema(data):
    data.index = [5,1,6,7,4,2,3]
    data = data.sort_index(ascending = True) 
    data.index = ['Lun','Mar','Mier','Juev','Vier','Sab','Dom']
    return data


def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
  
    return file_paths 



