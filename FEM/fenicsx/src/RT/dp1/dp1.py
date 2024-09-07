from FEM.fenicsx.src.RT.dp1.collimated import get_max_y,collimated
import numpy as np
import ufl
from dolfinx import fem
from dolfinx.fem import Function
from ufl import grad, inner

def set_dofs_optical_properties(V,regions):

    mu_a = Function(V)
    mu_s = Function(V)
    g = Function(V)
    for region, tag in regions.items():
        mu_a.x.array[tag[3]] = tag[2].mu_a
        mu_s.x.array[tag[3]] = tag[2].mu_s
        g.x.array[tag[3]] = tag[2].g

    return mu_a,mu_s,g

def get_dp1_optical_properties(V,mu_a,mu_s,g):
    # Porpiedades opticas
    def musp(mus,g):
        musp = mus*(1-g)
        return musp
    def mutr(mua,mus,g):
        return mua+musp(mus,g)
    def mus_ast(mus,g):
        return mus*(1-g**2)
    def mut_ast(mua,mus,g):
        return mua+mus_ast(mus,g)
    def mueff(mua,mus,g):
        return np.sqrt(3*mua*mutr(mua,mus,g))
    def g_ast(g):
        return g/(1+g)
    
    mueff2_func = Function(V)
    mus_ast_func = Function(V)
    mutr_func = Function(V)
    mut_ast_func = Function(V)
    g_ast_func = Function(V)

    mueff2_func.x.array[:] = mueff(mu_a.x.array[:],mu_s.x.array[:],g.x.array[:])**2
    mus_ast_func.x.array[:] = mus_ast(mu_s.x.array[:],g.x.array[:])
    mutr_func.x.array[:] = mutr(mu_a.x.array[:],mu_s.x.array[:],g.x.array[:])
    mut_ast_func.x.array[:] = mut_ast(mu_a.x.array[:],mu_s.x.array[:],g.x.array[:])
    g_ast_func.x.array[:] = g_ast(g.x.array[:])

    return mueff2_func,mus_ast_func,mutr_func,mut_ast_func,g_ast_func

def solve_dP1(V,dx,ds,v,mueff2,mus_ast,mutr_func,mut_ast,g_ast,phic,mesh,bc=[]):
    phid = ufl.TrialFunction(V)
    phi = Function(V)

    A = lambda n: -0.13755*n**3 + 4.3390*n**2 - 4.90466*n + 1.6896
    h = 2/3/mutr_func

    n = ufl.FacetNormal(mesh)
    def get_forms(A1,A2):
        F = (inner(grad(phid), grad(v)) * dx #laplaciano
            + mueff2*phid*v* dx #Absorcion
            - 3*mus_ast*(mutr_func+mut_ast*g_ast)*phic*v*dx #Dispersion de luz colimada
            # + v/h/A1*(phid + 3*h*A1*g_ast*mus_ast*phic) * ds(30)
            # + v/h/A1*(phid + 3*h*A1*g_ast*mus_ast*phic* ufl.dot(ufl.as_vector([0.0,1.0,0.0]),n)) * ds(43)
            # + v/h/A2*(phid + 3*h*A2*g_ast*mus_ast*phic) * ds(31))
        )

        a = ufl.lhs(F)
        L = ufl.rhs(F)
        return a,L
    def solve(a,L,bc):
        print('Solving: dP1')
        problem = fem.petsc.LinearProblem(a, L, bcs=bc)
        uh = problem.solve()
        return uh
    
    A1 = A(1.33)
    # A2 = A(1)
    # A1 = A(1/1.370)
    # A1 = 1.2746198517105856
    # A1 = 1e-12
    A2 = A(1.33)

    a,L = get_forms(A1,A2)
    phid = solve(a,L,bc)
    phi.x.array[:] = phid.x.array[:] + phic.x.array[:]
    return phi,phid


def dp1_get_heat_source(V,mesh,dx,ds,v,coords,regions_bc,regions,power,laser_radius,laser_type):
    MaxY = np.max(coords[1])
    mu_a,mu_s,g = set_dofs_optical_properties(V,regions)
    phic = collimated(V,coords,MaxY,mu_a,mu_s,g,power,laser_radius,laser_type)
    
    mueff2,mus_ast,mutr_func,mut_ast,g_ast = get_dp1_optical_properties(V,mu_a,mu_s,g)
    phi,phid = solve_dP1(V,dx,ds,v,mueff2,mus_ast,mutr_func,mut_ast,g_ast,phic,mesh[0])
    Qs = Function(V)
    Qs.x.array[:] = phi.x.array[:]*mu_a.x.array[:]
    return phic,phid,phi,Qs
