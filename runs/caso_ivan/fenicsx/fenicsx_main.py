import numpy as np
import sys


from ufl import ds, dx
import ufl

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
# from FEM.fenicsx.src.RT.welch.FR import welch_fr
from FEM.fenicsx.src.RT.beer_lambert.beer_lambert import beer_Qs
# from FEM.bridge.export_data import export_T
from alpha_interp.interp import interp_alpha
from dolfinx.fem import Function,assemble_scalar,form
import json

dir = sys.argv[1]

with open(f'{dir}/fenicsx/parameters.json', 'r') as file:
    parameters = json.load(file)

# print(parameters)

column = parameters['column']
sheet = parameters['sheet']

# REGION PROPERTIES
regions = {
        'tumor': [10, #GMSH physical tag
                  Material_Bioheat(k = 0.59, rho = 1000, c = 4200, w = 0, Qmet = 1091),
                  Material_Optical(mu_a=0, mu_s=50, g=0.9)],
        'tejido': [11, #GMSH physical tag
                   Material_Bioheat(k = 0.59, rho = 1000, c = 4200, w = 0, Qmet = 1091),
                   Material_Optical(mu_a=0, mu_s=50, g=0.9)],
        }
regions_bc = {
        'dirichlet': [13],
        'convection': [14],
        }

#REGION PROPERTIES
blood = Material_Bioheat_Blood(T = 37, rho = 1090, cp = 4200)

T_dirichlet = 37


## LOAD MESH AND SCALE
mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-2)

# SET FEM OBJECTS
mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)
bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],T_dirichlet)
# bc=[]

mu_a, mu_s, g = set_dofs_optical_properties(V,regions)

# SOURCE TERM
mu_a, mu_s, g = set_dofs_optical_properties(V,regions)

# Interpolate alpha
# mu_a.x.array[:] = interp_alpha(coords,dir,column,sheet)
x =  ufl.SpatialCoordinate(mesh[0])
# mu_a.interpolate(lambda x: (0.01 - x[1]))
mu_a.interpolate(lambda x: interp_alpha(x,dir,column,sheet))
# print(mu_a.x.array.max())



intensity = 5000
Qs = beer_Qs(V,mesh,mu_a,mu_s,intensity,R=0.01)

export_field_mesh(mu_a,mesh,"mua",dir)
export_field_mesh(Qs,mesh,"Qs",dir)

# print(regions_bc)

h = 5
# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir

def Qs_func(t):
        return Qs


sol = solve_FEM(V = V,msh = mesh[0],T = T,v = v,ds = ds,
        dx = dx,k = k,rho = rho,c = c,w = w,
        Qmet = Qmet,blood = blood,Qs_func = Qs_func,h = h,
        bc = bc,Ti = 35,Tref = 0,dt = 10,tf = 1800, 
        dir = directory, coords=coords,
        regions_bc=regions_bc,
        postprocess=False)

# print(len(sol))
# export_T(sol[0][1],dir)

# T_prom = np.zeros((len(sol),3))
# for i in range(len(sol)):
#         T_prom[i,0] = sol[i][0]
#         T_prom[i,1] = assemble_scalar(form(sol[i][1]*dx(10)))/assemble_scalar(form(1*dx(10)))
#         T_prom[i,2] = assemble_scalar(form(sol[i][1]*dx(11)))/assemble_scalar(form(1*dx(11)))
#         # print(sol[i][0],T_prom[i,1])

# np.save(f"{dir}/T_prom.npy",T_prom)

coords_sol = np.copy(coords)
for i in range(len(sol)):
        T = sol[i][1].x.array
        # print(coords.shape)
        coords_sol = np.concatenate((coords_sol, T.reshape(T.shape[0],1)),axis=1)

np.save(f"{dir}/coords_sol.npy",coords_sol)

# print(sol[0][1].x.array == sol[1][1].x.array)
# T_int = assemble_scalar(form(sol[100][1]*dx))
# A_int = assemble_scalar(form(1*dx))
# prom = T_int/A_int
# prom = assemble_scalar(form(Qs*dx))
# print(prom)

