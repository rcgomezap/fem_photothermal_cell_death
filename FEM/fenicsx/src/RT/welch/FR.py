from dolfinx.fem import Function, Expression
import numpy as np
import ufl

def welch_fr(V,msh,alpha,beta,ymax,sigma,Io=5000):
    x = ufl.SpatialCoordinate(msh[0])
    f = Io*ufl.exp(-x[0]**2/(2*sigma**2*ufl.exp(-2*beta*(ymax-x[1]))))*ufl.exp(-(alpha+beta)*(ymax-x[1]))
    # f.eval()
    # f = Io*ufl.exp(-x[0]**2/(2*sigma**2*ufl.exp(-2*beta*(ymax-[1]))))
    fr = Function(V)
    # fr.interpolate(lambda x: alpha.eval(x))
    fr.interpolate(Expression(f, V.element.interpolation_points()))
    # f = 3
    # f.interpolate(lambda x: alpha(x)*Io*np.exp(-(alpha(x)+beta(x))*(0.01-x[1]))) #W/m3 # Opcion 3
    # f.interpolate(lambda x: Io*np.exp(-x[0]**2/(2*sigma**2)*beta(x)))


    return fr