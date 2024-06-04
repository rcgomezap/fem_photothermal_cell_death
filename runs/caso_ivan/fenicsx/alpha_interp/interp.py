import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import CloughTocher2DInterpolator
from scipy.interpolate import NearestNDInterpolator
from scipy.interpolate import LinearNDInterpolator

def interp_alpha(list_cells,dir_):
    graficar = False

    # read file ''ResIvan27012023.xlsx'' with pandas
    # df = pd.read_excel('Resultados_de_simulaciones.xlsx', sheet_name='Total concentration (gr.ml-1)', header=1)
    df = pd.read_excel(f'{dir_}/data/Resultados de simulaciones de electroporación 03_14_2024.xlsx', sheet_name='Total conc. (gr.ml-1) 40 mV', header=1)
    # convert column 1 of df to numpy array
    #Q = 0.214
    Q = 0.245
    r = 20e-9

    xdata = df.iloc[:,0].to_numpy()
    ydata = df.iloc[:,1].to_numpy()
    cdata = df.iloc[:,10].to_numpy()
    cdata = cdata * 1e3
    rau=19300
    fv=cdata/rau
    alpha = 2.0 + 0.75 * fv * Q / r

    maxy = np.max(ydata)
    maxx = np.max(xdata)

    xdata = xdata/maxx/1000*20
    ydata = ydata/maxy/1000*10
    interp_Clough = CloughTocher2DInterpolator(list(zip(xdata, ydata)), alpha)
    interp_Nearest = NearestNDInterpolator(list(zip(xdata, ydata)), alpha)
    #z = np.zeros(len(X))

    # for i in range(len(X)):
    #     z[i] = interp_Clough(X[i], Y[i])
    #     if str(z[i]) == 'nan':
    #         z[i] = interp_Nearest(X[i], Y[i])
    #         print('InterpNear')
    #         print(z[i])
    #         if str(z[i]) == 'nan':
    #             print('Error: z[i] is nan')
    list_alpha=[]
    for i in range(len(list_cells)):
        x = list_cells[i][0]
        y = list_cells[i][1]
        # Percentage process
        # print('Proceso interpolacion: ', str(i/len(list_cells)*100) + '%')
        valor_alpha = interp_Clough(x,y)
        if str(valor_alpha) == 'nan':
            valor_alpha = interp_Nearest(x,y)
            print('InterpNear')
            print(valor_alpha)
            if str(valor_alpha) == 'nan':
                print('Error: valor_alpha is nan')
        list_alpha.append(valor_alpha)

    if graficar == True:
        X = np.linspace(min(xdata), max(xdata),200)
        Y = np.linspace(min(ydata), max(ydata),100)
        XX, YY = np.meshgrid(X, Y)
        Z = interp_Clough(XX, YY)
        #plot a 2D color map
        plt.figure(figsize=(10, 5))
        # q: que cmaps hay?
        # a: https://matplotlib.org/stable/tutorials/colors/colormaps.html
        plt.scatter(xdata*1000, ydata*1000, c=alpha, cmap='viridis', s=1)
        plt.colorbar()
        plt.clim(15,145)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.savefig('alpha_datos.png', dpi=400)
        #plt.show()


        #plot a 2D color map
        plt.figure(figsize=(10, 5))
        plt.pcolormesh(XX*1000, YY*1000, Z, cmap='viridis')
        plt.colorbar()
        plt.clim(15,145)
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.savefig('alpha_interp.png', dpi=400)
        #plt.show()
    return list_alpha
# xx=10/1000
# yy=0/1000
# print(interp_alpha([[xx,yy]]))