from dolfinx.fem import Function
import numpy as np
import ufl
from dolfinx import fem
from dolfinx.fem import Function
from ufl import grad, inner,dot


def get_fluence_rate(power,radius):
    return power/(np.pi*radius**2)




def solve(V,mesh,dx,mut_ast,MaxY,irradiance):

    def marker(x):
        return np.isclose(x[1],0.01)
    
    W = fem.FunctionSpace(mesh[0],("CG",1))
    phic = ufl.TrialFunction(W)
    f = Function(W)
    v = ufl.TestFunction(W)
    z_i = -ufl.unit_vector(1,3)
    mut_astw = Function(W)
    mut_astw.interpolate(mut_ast)

    # a = inner(inner(grad(phic),ufl.as_vector([0.0,-1.0,0.0])),v)*dx - inner(mut_ast*phic,v)*dx
    # a = (dot(grad(phic),grad(v)))*dx + 1000*inner(phic,v)*dx
    # a = (dot(dot(grad(phic),z_i),dot(grad(v),z_i)))*dx + 1000*inner(phic,v)*dx
    a = inner(grad(phic),grad(v))*dx + inner(mut_astw*phic,v)*dx
    L = inner(f,v)*dx



    laser_dofs = fem.locate_dofs_geometrical(W, marker)
    bc = fem.dirichletbc(1., laser_dofs, W)

    
    problem = fem.petsc.LinearProblem(a, L, bcs=[bc])
    u = problem.solve()
    return u


def collimated(V,mesh,dx,MaxY,mu_a,mu_s,g,power,laser_radius):


    mut_ast = Function(V)
    mus_ast = Function(V)

    mus_ast.x.array[:] = mu_s.x.array[:]*(1-g.x.array[:]**2)
    mut_ast.x.array[:] = mu_a.x.array[:]+mus_ast.x.array[:]
    
    irradiance = get_fluence_rate(power,laser_radius)

    phic = solve(V,mesh,dx,mus_ast,MaxY,irradiance)
    # phic = Function(V)





    # collimated = Function(V)
    return phic





