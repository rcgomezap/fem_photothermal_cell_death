from fenicsx_args import run
import matplotlib.pyplot as plt
import numpy as np
import Funciongeneral
import csv
import pandas as pd

column = 10
sheet = 'Total conc. (gr.ml-1) -40 mV'
dt = 10
t_max3=150
fi=1

sol = run(column,sheet)

x = sol[:,0:2]
Temp=sol[:,3:-1]
index_puntos_en_tumor = []
index_puntos_en_tejido_sano = []

for j in range(0,14365):
    if (x[j,0]<=0.01) and (x[j,1]>=0.005):
        index_puntos_en_tumor.append(j)
    else:
        index_puntos_en_tejido_sano.append(j)
    for k in range(0,30):
        Temp[j,k]=Temp[j,k]-273.15
        
Y,P=Funciongeneral.ONeill(Temp,x,t_max3,dt,fi,1)
data_tumor = []
data_tejido_sano = []

for j in index_puntos_en_tumor:
    data_tumor.append(Y[j,-1])
for j in index_puntos_en_tejido_sano:
    data_tejido_sano.append(Y[j,-1])
    
T = np.mean(data_tumor) 
TS = np.mean(data_tejido_sano) 


plt.plot(sol[0,2:])
plt.show()
print(sol.shape)