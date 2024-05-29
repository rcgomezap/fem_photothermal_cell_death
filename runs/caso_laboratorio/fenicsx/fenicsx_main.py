import numpy as np
import sys


from ufl import ds, dx

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
from FEM.fenicsx.src.RT.welch.FR import welch_fr
from FEM.bridge.export_data import export_T
from dolfinx.fem import Function,assemble_scalar

dir = sys.argv[1]

# REGION PROPERTIES
regions = {
        'tumor': [7, #GMSH physical tag
                  Material_Bioheat(k = 0.59, rho = 1000, c = 4200, w = 0, Qmet = 0),
                  Material_Optical(mu_a=26, mu_s=1, g=0.9)]
        }
regions_bc = {
        # 'dirichlet': [],
        'convection1': [5],
        'convectio2': [6],
        }

T_dirichlet = 37

#REGION PROPERTIES
blood = Material_Bioheat_Blood(T = 37, rho = 1090, cp = 4200)

## LOAD MESH AND SCALE
mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-3)

# SET FEM OBJECTS
mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)
# bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],T_dirichlet)
bc=[]

mu_a, mu_s, g = set_dofs_optical_properties(V,regions)

# SOURCE TERM
ymax = 7.8e-3
I0 = 8310
sigma = 0.00062505
phi = welch_fr(V,mesh,mu_a,mu_s,ymax,sigma, I0)
Qs = mu_a*phi

# EXPORT FIELDS
# phi = assemble_scalar(phi)
export_field_mesh(mu_a,mesh,"mua",dir)
export_field_mesh(phi,mesh,"phi",dir)
# export_field_mesh(Qs,mesh,"Qs",dir)

print(regions_bc)

h = Function(V)
# for i in range(len(h.x.array)):
#     if i in regions_bc['convection']:
#         h.x.array[i] = 1
    
# h=0

# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir
# Tfem = solve_FEM(V = V,msh = mesh[0],T = T,v = v,ds = ds,
#         dx = dx,k = k,rho = rho,c = c,w = w,
#         Qmet = Qmet,blood = blood,Qs = Qs,h = h,
#         bc = bc,Ti = 0,Tref = 0,dt = 1,tf = 600, 
#         dir = directory, coords=coords,
#         regions_bc=regions_bc,
#         postprocess=False)

# export_T(Tfem,dir)
