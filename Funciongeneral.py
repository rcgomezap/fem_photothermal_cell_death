# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:52:32 2023

@author: Melany Martinez
"""
import numpy as np
import matplotlib.pylab as plt
from scipy import integrate
from scipy.linalg import eigvals, expm_cond
from scipy.integrate import solve_ivp
from scipy.linalg import lu_factor, lu_solve
from scipy.interpolate import interp1d
import RBF as rbf
import scipy
import pospro as pp
import pandas as pd
import int_m as im

#CREACIÓN DE LA FUNCIÓN INTEGRADORA 
fv=1 #mLnp/mLtotales
r=50E-9 #m
Qa=Qb=0.2

# Parámetros de la ecuación de Pennes
kc = 0.5  # Conductividad térmica del tejido [W / K m]
nb = 1E-4  # Perfusión sanguínea [1/s]
rhob = 1052  # Densidad de la sangre [kg/m3]
cpb = 3800  # Calor específico de la sangre [J/kg K]
cp=3800
Ta = 37.0 +273.15  # Temperatura arterial
Qmet = 400  # Tasa metabólica de calor por unidad de volumen

kfbarra=6.2*6.66e-3 #1*3.33e-3#0.25481 ############
Kb=7.77e-3 #0.66477 # 
Tk=40.1513 #40.5
#Ks=0.59547
Dtao=0.45003E-3


def foptico(Concentracion,Kfbarra):
    Betam=0.003 #1/m
    Betanp= 0.75*fv*(Qb/r)
    alfam=7.5 #1/m
    alfanp=0.75*fv*(Qa/r)
    alfa,Beta=alfam+alfanp,Betam+Betanp
    return alfa,Beta

def temp(t_max,x_max,ua,us,N,dt):
    I0=1000  #W/m2
    h=1
    Tinfinito=37+273.15
    TL=30+273.15 #Temperatura incicial
    x_min = 0.0  # Radio mínimo
    x = np.linspace(x_min, x_max, N)
    dx=(x_max-x_min)/N
    c = 0.001
    #Tiempo
    t_min=0
    Nt=int(t_max/dt)+1
    # Crear la malla
    ti = np.ones(N,int) * 5
    ti[0] = 3
    TL2=40+273.15
    ti[-1] = 1
    Te=Ta+Qmet/(nb*rhob*cpb) #311.1506 
    Tsol=np.zeros((N,Nt))
    Tsol[:,0]=Te
    t=0.
    k=0
    phi = np.zeros((N, N))
    B = np.zeros(N)
    A = np.zeros((N, N))
    rho=rhob
    
    while t<t_max:
         # Se redefine A en cada iteración del bucle
        for i in range(N):
            for j in range(N):
                r = np.sqrt((x[i]-x[j])**2)
                if k ==0:
                    phi[i,j]=rbf.mq(r,c)
                if ti[i]==1:
                    if k==0:
                        A[i,j]=rbf.mq(r,c)
                        B[i]=Te
                elif ti[i]==2:
                    if k==0: 
                        dex=x[i]-x[j]
                        A[i,j]=dex*rbf.mq1dx(r, c)
                        B[i]=0
                elif ti[i]==5:
                    if k==0:
                        A[i,j]=kc*rbf.mq2d(r, c)-rho*cp*rbf.mq(r, c)/dt-rhob*cpb*nb*rbf.mq(r, c)
                    if j==0:
                        B[i]=-rho*cp*Tsol[i,k]/dt-nb*cpb*rhob*Ta-Qmet-(I0*ua*np.exp((-ua-us)*x[i]))
                elif ti[i]==3: ####################
                    if k==0:
                        A[i,j]=-kc*rbf.mq1dx(r, c)-h*rbf.mq(r,c)
                    if j==0:
                        B[i]=-h*Tinfinito
      
        if k==0:
            alu=lu_factor(A)
        al=lu_solve(alu,B)
        Tsol[:,k+1]=np.matmul(phi,al)
        k+=1
        t+=dt
        print(t)
    return Tsol,x

def ONeill (trbft,x,t_max,dt,fi,i):
    N=np.shape(trbft)[0]
    kf=np.zeros(N)
    T=np.zeros(N)
    fit=[]
    t_min=0
    # Nt=int(t_max/dt)+1
    Nt=np.shape(trbft)[1]
    t3=np.linspace(t_min,t_max,Nt)

    for i in range(N):
        itt=interp1d(t3,trbft[i,:Nt],fill_value='extrapolate')
        # itt=interp1d(t3,trbft[i,:])
        fit.append(itt)

    def fneil(t,y):
        n=np.size(y)
        dy=np.zeros(n)
        v=np.zeros(N)
        for i in range(N):
            if y[i]>1:
                y[i]=0.9999
                y[i+N]=1-0.9999
        v=-y[:N]-y[N:]+1
        for i in range (N):
            T[i]=fit[i](t)
            kf[i]=kfbarra*np.exp(T[i]/Tk)*(1-y[i])
            dy[i]=-kf[i]*y[i]+Kb*v[i]
            dy[N+i]=kf[i]*v[i]
        print('tiempo ',t)
        return dy

    nuevo_vector=im.interp_m(x)
    nuevo_vector=np.array(nuevo_vector)
    print(N)
    y0=np.ones(2*N)
    y0[0:N]=1-nuevo_vector-0.0001
    y0[N:]=nuevo_vector+0.0001
    solucion=solve_ivp(fneil,(0,t_max),y0,method='DOP853')
    ts=solucion.t
    ys=solucion.y
    Av=np.transpose(np.vstack((ys[:N,-1],1-ys[:N,-1]-ys[N:,-1],ys[N:,-1])))
    np.savetxt('Muerte.txt',Av) #Almacena en archivo de texto
    if fi==1:
        # plt.figure()
        # plt.plot(ts,ys[0,:],label='Células vivas')
        # plt.plot(ts,ys[50,:],label='Células muertas')
        # plt.plot(ts,1-ys[50,:]-ys[0,:], label='Células vulnerables')
        # plt.xlabel('Tiempo [s]')
        # plt.ylabel('Fracción de células')
        # plt.grid()
        # plt.legend()
        # plt.title('Modelo de O´Neill')
    
        Av=np.transpose(np.vstack((ys[:N,-1],1-ys[:N,-1]-ys[N:,-1],ys[N:,-1])))
        np.savetxt('Muerte.txt',Av) #Almacena en archivo de texto
        
        pp.cont(ys[:N,-1],ys[:N,-1],x,50,50,150) #Hace las gráficas de contorno
        pp.cont(ys[N:,-1],ys[N:,-1],x,50,50,150)
        pp.cont(1-ys[:N,-1]-ys[N:,-1],1-ys[:N,-1]-ys[N:,-1],x,50,50,150) 
        
    return ys,ts

def Arrhenius(trbft,x,t_max,dt,fi,u): 
    if u=="C":
        W=273.15
    if u=="K":
        W=0
    N=np.shape(trbft)[0] 
    t_min=0
    Nt=int(t_max/dt)+1
    t3=np.linspace(t_min,t_max,Nt)
    A=1.151E61 #1/s
    Ea=0.3935E6 #J/mol
    R=8.314 #J/mol K
    I=np.zeros(N)
    Mc=np.zeros(N)
    omega=np.zeros(Nt)
    #Función arrhenius 
    for i in range (N):
        omega=A*np.exp(-Ea/R/(trbft[i,:]+W))
        print(i)
        inte=np.trapz(omega,t3)
        I[i]=inte
    pp.cont(I,I,x,50,50,150)
    pp.cont
    np.savetxt('Arrhenius.txt',I)
    return I
