import numpy as np
import sys


from ufl import ds, dx,SpatialCoordinate

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
from FEM.fenicsx.src.RT.dp1.dp1 import dp1_get_heat_source
from FEM.bridge.export_data import export_T
from FEM.fenicsx.src.solvers.bioheat_DPL import solve as solve_DPL
from dolfinx.fem import Function,assemble_scalar,form
import json

dir = sys.argv[1]

with open(f'{dir}/fenicsx/parameters.json', 'r') as file:
    parameters = json.load(file)

tf = parameters['numericalParameters']['tf']
dt = parameters['numericalParameters']['dt']

# REGION PROPERTIES
regions = {
        'epidermis': [26, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['epidermis']['k'], rho = parameters['regionProperties']['epidermis']['rho'], c = parameters['regionProperties']['epidermis']['c'], w = parameters['regionProperties']['epidermis']['w'], Qmet = parameters['regionProperties']['epidermis']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['epidermis']['mu_a'], mu_s=parameters['regionProperties']['epidermis']['mu_s'], g=parameters['regionProperties']['epidermis']['g'])
        ],
        'p-dermis': [27, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['p-dermis']['k'], rho = parameters['regionProperties']['p-dermis']['rho'], c = parameters['regionProperties']['p-dermis']['c'], w = parameters['regionProperties']['p-dermis']['w'], Qmet = parameters['regionProperties']['p-dermis']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['p-dermis']['mu_a'], mu_s=parameters['regionProperties']['p-dermis']['mu_s'], g=parameters['regionProperties']['p-dermis']['g'])
        ],
        'r-dermis': [28, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['r-dermis']['k'], rho = parameters['regionProperties']['r-dermis']['rho'], c = parameters['regionProperties']['r-dermis']['c'], w = parameters['regionProperties']['r-dermis']['w'], Qmet = parameters['regionProperties']['r-dermis']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['r-dermis']['mu_a'], mu_s=parameters['regionProperties']['r-dermis']['mu_s'], g=parameters['regionProperties']['r-dermis']['g'])
        ],
        'fat': [29, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['fat']['k'], rho = parameters['regionProperties']['fat']['rho'], c = parameters['regionProperties']['fat']['c'], w = parameters['regionProperties']['fat']['w'], Qmet = parameters['regionProperties']['fat']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['fat']['mu_a'], mu_s=parameters['regionProperties']['fat']['mu_s'], g=parameters['regionProperties']['fat']['g'])
        ],
        'tumor': [24, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['tumor']['k'], rho = parameters['regionProperties']['tumor']['rho'], c = parameters['regionProperties']['tumor']['c'], w = parameters['regionProperties']['tumor']['w'], Qmet = parameters['regionProperties']['tumor']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['tumor']['mu_a'], mu_s=parameters['regionProperties']['tumor']['mu_s'], g=parameters['regionProperties']['tumor']['g'])
        ],
        'tumorNP': [25, #GMSH physical tag
                  Material_Bioheat(k = parameters['regionProperties']['tumorNP']['k'], rho = parameters['regionProperties']['tumorNP']['rho'], c = parameters['regionProperties']['tumorNP']['c'], w = parameters['regionProperties']['tumorNP']['w'], Qmet = parameters['regionProperties']['tumorNP']['Qmet']),
                  Material_Optical(mu_a=parameters['regionProperties']['tumorNP']['mu_a'], mu_s=parameters['regionProperties']['tumorNP']['mu_s'], g=parameters['regionProperties']['tumorNP']['g'])
        ],
        }
regions_bc = {
        # 'dirichlet': [],
        'convection_1': [22],
        'convection_2': [23],
        }

# T_dirichlet = 37

#REGION PROPERTIES
blood = Material_Bioheat_Blood(T = parameters['bloodProperties']['T'], rho = parameters['bloodProperties']['rho'], cp = parameters['bloodProperties']['c'])

## LOAD MESH AND SCALE
mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-3)

# SET FEM OBJECTS
mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)
# bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],T_dirichlet)
bc=[]


# SOURCE TERM
mu_a, mu_s, g = set_dofs_optical_properties(V,regions)
phic,phid,phi,Qs = dp1_get_heat_source(V,mesh,dx,ds,v,coords,regions_bc,regions,power=parameters['laserProperties']['power'],laser_radius=parameters['laserProperties']['radius'],laser_type=parameters['laserProperties']['type'])
export_field_mesh(phic,mesh,"phic",dir)
export_field_mesh(phid,mesh,"phid",dir)
export_field_mesh(phi,mesh,"phi",dir)


# EXPORT FIELDS
export_field_mesh(mu_a,mesh,"mua",dir)
export_field_mesh(Qs,mesh,"Qs",dir)


h = Function(V)
h_1 = parameters['boundaryParameters']['h']
h_2 = 0

print(h_2)
for i in range(len(h.x.array)):
        if i in regions_bc['convection_1'][1]:
                h.x.array[i] = h_1
        elif i in regions_bc['convection_2'][1]:
                h.x.array[i] = h_2

# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir

def Qs_func(t):
        if t <= parameters['laserProperties']['irradiationTime']:
                return Qs
        else:
                return Function(V)


solT = solve_DPL(V = V,msh = mesh[0],T = T,v = v,ds = ds,
                dx = dx,k = k,tau_q=parameters['numericalParameters']["tau_q"],tau_t=parameters['numericalParameters']["tau_T"],rho = rho,c = c,w = w,
                Qmet = Qmet,blood = blood,Qs_func = Qs_func,h = h,
                bc = bc,Ti = parameters['initialConditions']['T'],Tref = parameters['boundaryParameters']['ambientTemperature'],dt = dt,tf = tf, 
                dir = directory, coords=coords,
                regions_bc=regions_bc,
                postprocess=False)


coords_sol = np.copy(coords)
for i in range(len(solT)):
        T = solT[i][1].x.array
        # print(coords.shape)
        coords_sol = np.concatenate((coords_sol, T.reshape(T.shape[0],1)),axis=1)

np.save(f"{dir}/T_sol.npy",coords_sol)

# print(sol[0][1].x.array == sol[1][1].x.array)
# T_int = assemble_scalar(form(sol[100][1]*dx))
# A_int = assemble_scalar(form(1*dx))
# prom = T_int/A_int
# prom = assemble_scalar(form(Qs*dx))
# print(prom)

