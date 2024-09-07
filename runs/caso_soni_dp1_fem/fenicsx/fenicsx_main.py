import numpy as np
import sys


from ufl import ds, dx

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
from FEM.fenicsx.src.RT.beer_lambert.beer_lambert import beer_Qs
from FEM.fenicsx.src.RT.dp1.dp1 import dp1_get_heat_source
from dolfinx.fem import Function,assemble_scalar

dir = sys.argv[1]

# REGION PROPERTIES
regions = {
        'tumor': [10, #GMSH physical tag
                  Material_Bioheat(k = 0.59, rho = 1000, c = 4200, w = 0, Qmet = 1091),
                  Material_Optical(mu_a=12100, mu_s=50, g=0.9)],
        'tejido': [11, #GMSH physical tag
                   Material_Bioheat(k = 0.59, rho = 1000, c = 4200, w = 0, Qmet = 1091),
                   Material_Optical(mu_a=0, mu_s=176, g=0.9)],
        }
regions_bc = {
        'dirichlet': [13],
        'convection': [14],
        }

#REGION PROPERTIES
blood = Material_Bioheat_Blood(T = 37, rho = 1090, cp = 4200)

mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-2)

mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)
bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],37)
# bc=[]

mu_a, mu_s, g = set_dofs_optical_properties(V,regions)
export_field_mesh(mu_a,mesh,"mua",dir)
intensity = 5000
laser_radius = 10e-3
power = intensity*np.pi*laser_radius**2 #W
Qs = beer_Qs(V,mesh,mu_a,mu_s,intensity)
# phic,phid,phi,Qs = dp1_get_heat_source(V,mesh,dx,ds,v,coords,regions_bc,regions,power=power,laser_radius=laser_radius,laser_type="flat")
def Qs_func(t):
    return Qs
# export_field_mesh(Qs,mesh,"Qs",dir)
# export_field_mesh(phic,mesh,"phic",dir)
# export_field_mesh(phid,mesh,"phid",dir)
# export_field_mesh(phi,mesh,"phi",dir)
# Qs=0

# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir
Tfem = solve_FEM(V = V,msh = mesh[0],T = T,v = v,ds = ds,
        dx = dx,k = k,rho = rho,c = c,w = w,
        Qmet = Qmet,blood = blood,Qs_func = Qs_func,h = 5,
        bc = bc,Ti = 35,Tref = 22.9,dt = 1,tf = 300, 
        dir = directory, coords=coords,
        regions_bc=regions_bc,
        postprocess=False)
# export_T(Tfem,dir)
