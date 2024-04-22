from dolfinx.fem import Function
import numpy as np
import ufl

def beer_Qs(V,msh,alpha,beta,Io=5000):
    x = ufl.SpatialCoordinate(msh[0])
    # Qs = alpha*Io*ufl.exp(-(alpha+beta)*(0.01-x[1]))
    f = Function(V)
    coords= V.tabulate_dof_coordinates()
    f.x.array[:] = alpha.x.array[:]*Io*np.exp(-(alpha.x.array[:]+beta.x.array[:])*(0.01-coords[:,1]))
    return f