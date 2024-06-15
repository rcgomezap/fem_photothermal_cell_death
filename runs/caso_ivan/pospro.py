
import numpy as np
import matplotlib.pylab as plt
from scipy.interpolate import griddata

def erl2(u,ua):
    er=np.sqrt(np.dot(u-ua,u-ua))
    return er

def cont(u,ua,mpre,nvx,nvy,t):
    x1=np.linspace(min(mpre[:,0]),max(mpre[:,0]),nvx);
    y1=np.linspace(min(mpre[:,1]),max(mpre[:,1]),nvy);
    [X,Y]=np.meshgrid(x1,y1);
    Z = griddata(mpre[:,0:2],u[:],(X,Y),'linear');
    # plt.figure()
    # cp = plt.contourf(X, Y, Z)
    # plt.colorbar(cp)
    Za = griddata(mpre[:,0:2],ua[:],(X,Y),'linear');
    plt.figure()
    cp = plt.contourf(X, Y, Z)
    plt.colorbar(cp)
    plt.ylabel('y[m]')
    plt.xlabel('x[m]')
    name='tempc_'+str(int(t))+'.pdf'
    plt.savefig(name,format='pdf',dpi=600)
    plt.show()
    
def plotit(u,ua,mpre,d,val,eps,t,z):
    n=np.shape(u)[0]
    nz=0
    xp=np.zeros(n,float)
    up=np.zeros(n,float)
    upa=np.zeros(n,float)
    if d==1:
        do=0
    else:
        do=1        
    for i in range(0,n):
        if (mpre[i,d]>=val and mpre[i,d]<val+eps):
            xp[nz]=mpre[i,do]
            up[nz]=u[i]
            upa[nz]=ua[i]
            nz+=1
    plt.figure(5)
    plt.plot(xp[0:nz],up[0:nz],'k.',xp[0:nz],upa[0:nz],'b-')
    plt.ylabel('u')
    plt.xlabel('x')
  
    savf='%.15e'

    title='T'+str(n)+'x_'+str(d)+'z_'+str(z)+'JuanNS.txt'
    np.savetxt(title,up[0:nz],fmt=savf, delimiter=' ')
    title='pos'+str(n)+'x_'+str(d)+'z_'+str(z)+'_JuanNS.txt'
    np.savetxt(title,xp[0:nz],fmt=savf, delimiter=' ')
    
    
    plt.show(5)

def calaver(mpre,u):
    L1=np.max(mpre[:,0])
    L2=np.max(mpre[:,1])
    uaver=2*np.mean(u*mpre[:,0])/L1
    return uaver
    
def plotet(e,cv,ts):
    ns=np.shape(e)[1]
   # nc=np.shape(e)[0]
    plt.figure()
    for i in range(ns):
        plt.plot(cv[:],e[:,i])
    plt.ylabel('El2')
    plt.xlabel('c')
    plt.show()
            
