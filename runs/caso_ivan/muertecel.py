from fenicsx_args import run
import sys
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from cell_death import Funciongeneral

sheet_T = 'Total conc. (gr.ml-1) -40 mV'
sheet_MC = 'Cell Death -40 mV'
file_MC = 'data/Resultados de simulaciones de electroporación 03_14_2024.xlsx'
database=np.load('caso0.npy')
dt = 10
t_max3=150
fi=1

#Calcular la muerte en el caso base
Temp_base=database[:,3:-1]
x_base=database[:,0:2]

index_puntos_en_tumor_base = []
index_puntos_en_tejido_sano_base = []

for j in range(0,database.shape[0]):
    if (x_base[j,0]<=0.01) and (x_base[j,1]>=0.005):
        index_puntos_en_tumor_base.append(j)
    else:
        index_puntos_en_tejido_sano_base.append(j)

        
Y,P=Funciongeneral.ONeill(Temp_base,x_base,t_max3,dt,fi,1,file_MC,sheet_MC)
data_tumor_base = []
data_tejido_sano_base = []

for j in index_puntos_en_tumor_base:
    data_tumor_base.append(Y[j,-1])
for j in index_puntos_en_tejido_sano_base:
    data_tejido_sano_base.append(Y[j,-1])
    
T_base = np.mean(data_tumor_base) 
TS_base= np.mean(data_tejido_sano_base) 


# plt.plot(database[0,2:])
# # plt.savefig('RESULTADOS'+str(column_T)+sheet_T+'.png')
print(f'Tejido Tumoral base {T_base}') 
print(f'Tejido Sano base {TS_base}') 



#Calcular la muerte celular con electroporación ######

for k in range(2,11):
    column_T=k
    sol = run(column_T,sheet_T)
    x = sol[:,0:2]
    Temp=sol[:,3:-1]
    index_puntos_en_tumor = []
    index_puntos_en_tejido_sano = []
    
    for j in range(0,sol.shape[0]):
        if (x[j,0]<=0.01) and (x[j,1]>=0.005):
            index_puntos_en_tumor.append(j)
        else:
            index_puntos_en_tejido_sano.append(j)
    
            
    Y,P=Funciongeneral.ONeill(Temp,x,t_max3,dt,fi,1,file_MC,sheet_MC)
    data_tumor = []
    data_tejido_sano = []
    
    for j in index_puntos_en_tumor:
        data_tumor.append(Y[j,-1])
    for j in index_puntos_en_tejido_sano:
        data_tejido_sano.append(Y[j,-1])
        
    T = np.mean(data_tumor) 
    TS = np.mean(data_tejido_sano) 
    
    
    # plt.plot(sol[0,2:])
    # #plt.savefig('RESULTADOS'+str(column_T)+sheet_T+'.png')
    print(f'Tejido Tumoral {T}') 
    print(f'Tejido Sano {TS}') 
    
    relativo_tumor=((T_base-T)/T_base)*100
    relativo_sano=((TS_base-TS)/TS_base)*100
    print(f'Relativo tejido tumoral {relativo_tumor} '+f' {k}')
    print(f'Relativo tejido sano {relativo_sano} '+f' {k}')