import numpy as np
import sys


from ufl import ds, dx

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
from FEM.fenicsx.src.RT.welch.FR import welch_fr
from FEM.bridge.export_data import export_T
from dolfinx.fem import Function,assemble_scalar,form
import json

dir = sys.argv[1]

with open(f'{dir}/fenicsx/parameters.json', 'r') as file:
    parameters = json.load(file)

# print(parameters)

k = parameters['k']
rho = parameters['rho']
c = parameters['c']
w = parameters['w']
alpha = parameters['alpha']
mu_s = parameters['mu_s']
Qmet = parameters['Qmet']
g = parameters['g']
tf = parameters['tf']
regions_bc = parameters['regions_bc']
T_dirichlet = parameters['T_dirichlet']
blood_T = parameters['blood_T']
blood_rho = parameters['blood_rho']
blood_cp = parameters['blood_cp']
I0 = parameters['I0']
sigma = parameters['sigma']
ymax = parameters['ymax']
h = parameters['h']
t_ir = parameters['t_irradiation']
dt = parameters['dt']
Ti = parameters['Ti']
Tref = parameters['Tref']

# rt_model = parameters['rt_model']

# REGION PROPERTIES
regions = {
        'tumor': [7, #GMSH physical tag
                  Material_Bioheat(k = k, rho = rho, c = c, w = w, Qmet = Qmet),
                  Material_Optical(mu_a=alpha, mu_s=mu_s, g=g)]
        }
# regions_bc = {
#         # 'dirichlet': [],
#         'convection_1': [5],
#         'convection_2': [6],
#         }

# T_dirichlet = 37

#REGION PROPERTIES
# blood = Material_Bioheat_Blood(T = 37, rho = 1090, cp = 4200)
blood = Material_Bioheat_Blood(T = blood_T, rho = blood_rho, cp = blood_cp)

## LOAD MESH AND SCALE
mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-3)

# SET FEM OBJECTS
mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)

if 'dirichlet' in regions_bc:
        bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],T_dirichlet)
else:
        bc = []

mu_a, mu_s, g = set_dofs_optical_properties(V,regions)

# SOURCE TERM
# ymax = 7.8e-3
# I0 = 8310
# sigma = 0.00062505
phi = welch_fr(V,mesh,mu_a,mu_s,ymax,sigma, I0)
Qs = mu_a*phi

# EXPORT FIELDS
# phi = assemble_scalar(phi)
export_field_mesh(mu_a,mesh,"mua",dir)
export_field_mesh(phi,mesh,"phi",dir)
# export_field_mesh(Qs,mesh,"Qs",dir)

# print(regions_bc)

# h = Function(V)
# h_1 = 10
# r=3.5e-3 # Radio interno del cilindro
# R = r + 1e-3 # Radio externo del cilindro
# Ka = 0.2 # Conductividad térmica del acrilico
# h_2 = 1/(r*np.log(R/r)/Ka+r/R/h_1)
# print(h_2)
# for i in range(len(h.x.array)):
#         if i in regions_bc['convection_1'][1]:
#                 h.x.array[i] = h_1
#         elif i in regions_bc['convection_2'][1]:
#                 h.x.array[i] = h_2

# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir

def Qs_func(t):
        if t <= t_ir:
                return Qs
        else:
                return Function(V)


sol = solve_FEM(V = V,msh = mesh[0],T = T,v = v,ds = ds,
        dx = dx,k = k,rho = rho,c = c,w = w,
        Qmet = Qmet,blood = blood,Qs_func = Qs_func,h = h,
        bc = bc,Ti = Ti,Tref = Tref,dt = dt,tf = tf, 
        dir = directory, coords=coords,
        regions_bc=regions_bc,
        postprocess=False)

# print(len(sol))
# export_T(sol[0][1],dir)

T_prom = np.zeros((len(sol),2))
for i in range(len(sol)):
        T_prom[i,0] = sol[i][0]
        T_prom[i,1] = assemble_scalar(form(sol[i][1]*dx))/assemble_scalar(form(1*dx))
        # print(sol[i][0],T_prom[i,1])

np.save(f"{dir}/T_prom.npy",T_prom)

# print(sol[0][1].x.array == sol[1][1].x.array)
# T_int = assemble_scalar(form(sol[100][1]*dx))
# A_int = assemble_scalar(form(1*dx))
# prom = T_int/A_int
# prom = assemble_scalar(form(Qs*dx))
# print(prom)
