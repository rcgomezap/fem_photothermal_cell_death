from dolfinx.fem import Function,Expression
import numpy as np
import ufl

def beer_Qs(V,msh,alpha,beta,Io=5000,R=0.01):
    x = ufl.SpatialCoordinate(msh[0])

    def Qs(x):
        tmp = np.zeros(x.shape[1])
        # print(tmp.shape)
        for i in range(x.shape[1]):
            if x[0,i] < R:
                tmp[i] = (0.01-x[1,i])
            else:
                tmp[i] = 1e10
        return tmp
    # Qs = alpha*Io*ufl.exp(-(alpha+beta)*(0.01-x[1]))
    f = Function(V)
    f.interpolate(lambda x: (Qs(x)))
    f = alpha*Io*ufl.exp(-(alpha+beta)*f)
    qs = Function(V)
    qs.interpolate(Expression(f, V.element.interpolation_points()))
    # q = 2*f
    return qs