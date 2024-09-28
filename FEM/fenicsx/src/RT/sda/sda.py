import numpy as np
import ufl
from dolfinx import fem
from dolfinx.fem import Function,dirichletbc
from ufl import grad, inner
from FEM.fenicsx.src.RT.dp1.dp1 import set_dofs_optical_properties
from FEM.fenicsx.src.RT.dp1.collimated import get_fluence_rate_gaussian

def get_diffussivity(V,mu_a,mu_s,g):
    # Porpiedades opticas
    def D_fun(mua,mus,g):
        musp = mus*(1-0.9)
        return 1/(3*(mua+musp))
    
    D = Function(V)

    D.x.array[:] = D_fun(mu_a.x.array[:],mu_s.x.array[:],g.x.array[:])

    return D

def set_laser_dofs(coords,surface_dofs,laser_radius):
    laser_dofs = []
    # update laser dofs
    for i in surface_dofs:
        if coords[i,0]**2+coords[i,2]**2 < laser_radius**2:
            laser_dofs.append(i)
    laser_dofs = np.array(laser_dofs)

    return laser_dofs


def set_laser_function(V,coords,laser_dofs,power,laser_radius,laser_type):
    la = Function(V)
    if laser_type == "flat":
        laser_intensity = power/np.pi/laser_radius**2
        for i in range(len(coords)):
            if i in laser_dofs:
                la.x.array[i] = laser_intensity
    elif laser_type == "gaussian":
        func_gaussian = lambda x: get_fluence_rate_gaussian(power,laser_radius,x[0,:])
        la.interpolate(func_gaussian)
    return la

def get_dirichlet_bc(V,laser_dofs,laser_intensity):
    la = Function(V)
    la.x.array[:] = laser_intensity
    bcs = [dirichletbc(la, laser_dofs)]
    return bcs

def solve_p1(V,dx,ds,v,D,mu_a,P0,bc=[]):
    phid = ufl.TrialFunction(V)
    r = ufl.SpatialCoordinate(V.mesh)[0]
    f = Function(V)
    A = lambda n: -0.13755*n**3 + 4.3390*n**2 - 4.90466*n + 1.6896
    def get_forms(A):
        F = (D*inner(grad(phid), grad(v)) * r * dx #laplaciano
            + mu_a*phid*v* r * dx #Absorcion
            - f*v*r*dx #Fuente
            # + (0.5/A1*phid)*v* r*ds
            - (2*P0 - phid/2)/A*v*r*ds
        )

        a = ufl.lhs(F)
        L = ufl.rhs(F)
        return a,L
    
    def solve(a,L,bc):
        print('Solving: SDA')
        problem = fem.petsc.LinearProblem(a, L, bcs=bc)
        uh = problem.solve()
        return uh
    A1 = A(1.33)
    # A2 = A(1)
    a,L = get_forms(A1)
    phid = solve(a,L,bc)
    return phid

def sda_get_heat_source(V,mesh,dx,ds,v,coords,regions_bc,regions,power,laser_radius,laser_type):

    mu_a,mu_s,g = set_dofs_optical_properties(V,regions)
    D = get_diffussivity(V,mu_a,mu_s,g)
    laser_dofs = set_laser_dofs(coords,regions_bc["laser"][1],laser_radius)
    P0_func = set_laser_function(V,coords,laser_dofs,power,laser_radius,laser_type)

    # bcs = get_dirichlet_bc(V,laser_dofs,laser_intensity)
    phid = solve_p1(V,dx,ds,v,D,mu_a,P0=P0_func,bc=[])
    Qs = Function(V)
    Qs.x.array[:] = phid.x.array[:]*mu_a.x.array[:]
    return phid,Qs