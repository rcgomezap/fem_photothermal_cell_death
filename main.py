# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 09:56:34 2024

@author: Melany Martinez
"""

import numpy as np
import cell_death.Funciongeneral as Funciongeneral
import pandas as pd


Datos= pd.read_excel("Temperature_data.xlsx", sheet_name="2")
datos = np.array(Datos)
N=1
T=np.zeros(6)
TS=np.zeros(6)
for i in range(N):
    fi=1
    t_max3=150
    dt=5
    x = datos[:,1:3]
    Temp=datos[:,3:-1]
 
    index_puntos_en_tumor = []
    index_puntos_en_tejido_sano = []
    for j in range(0,20000):
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