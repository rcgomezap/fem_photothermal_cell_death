import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import NearestNDInterpolator
#from scipy.interpolate import LinearNDInterpolator

def interp_m(list_cells):
    graficar = False 

    # read file ''ResIvan27012023.xlsx'' with pandas
    df = pd.read_excel('Resultados_de_simulaciones.xlsx', sheet_name='Cell Death', header=0)
    # convert column 1 of df to numpy array
    #Q = 0.214
    Q = 0.245
    r = 20e-9

    xdata = df.iloc[:,0].to_numpy()
    ydata = df.iloc[:,1].to_numpy()
    mdata = df.iloc[:,2].to_numpy()
    # preacondicionamiento de datos para hallar alpha en funcion de la concentracion

    #normalizar datos y escalarlos a la malla de OpenFoam (20x10 mm)
    maxy = np.max(ydata)
    maxx = np.max(xdata)

    # xdata = xdata/maxx/1000*20
    # ydata = ydata/maxy/1000*10
    
    #interpolar datos con CloughTocher2DInterpolator y NearestNDInterpolator
    # estas funciones crean una funcion que interpola los datos con los que se evaluen
    interp_Clough = CloughTocher2DInterpolator(list(zip(xdata, ydata)), mdata)
    interp_Nearest = NearestNDInterpolator(list(zip(xdata, ydata)), mdata)

    #se van a guardar los datos en una lista
    list_alpha=[]
    nd=np.size(list_cells[:,0])

    for i in range(nd):
        x = list_cells[i,0]
        y = list_cells[i,1]
        # Percentage process
        # print('Proceso interpolacion: ', str(i/len(list_cells)*100) + '%')

        #interpolar un valor de alpha para una coordenada (x,y) de cada celda
        valor_alpha = interp_Clough(x,y)

        # si el valor de alpha es nan, interpolar con NearestNDInterpolator
        if str(valor_alpha) == 'nan':
            valor_alpha = interp_Nearest(x,y)
            #print('InterpNear')
            #print(valor_alpha)
            if str(valor_alpha) == 'nan':
                print('Error: valor_alpha is nan')
        #guardar valor de alpha en la lista
        list_alpha.append(valor_alpha)

    #graficar datos creando un meshgrid con las dimensiones de la malla de OpenFoam
    if graficar == True:
        X = np.linspace(min(xdata), max(xdata),100)
        Y = np.linspace(min(ydata), max(ydata),100)
        XX, YY = np.meshgrid(X, Y)
        Z = interp_Clough(XX, YY)
        #plot a 2D color map

        #graficar datos experimentales
        plt.figure(figsize=(10, 5))
        # q: que cmaps hay?
        # a: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        plt.scatter(xdata*1000, ydata*1000, c=mdata, cmap='viridis', s=1)
        plt.colorbar()
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.savefig('alpha_datos.png', dpi=500)
        #plt.show()


        #graficar datos interpolados
        plt.figure(figsize=(10, 5))
        plt.pcolormesh(XX*1000, YY*1000, Z, cmap='viridis')
        plt.colorbar()
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.savefig('alpha_interp.png', dpi=500)
        #plt.show()
    return list_alpha

