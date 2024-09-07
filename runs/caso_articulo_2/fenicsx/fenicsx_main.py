import numpy as np
import sys


from ufl import ds, dx

from FEM.fenicsx.src.material_classes import Material_Bioheat, Material_Bioheat_Blood, Material_Optical
from FEM.fenicsx.src.fem_funcs import load_mesh, scale_mesh, locate_dofs, get_fem_objects, set_dofs_properties, set_dirichlet_bcs, solve_FEM, export_field_mesh
from FEM.fenicsx.src.RT.funcs import set_dofs_optical_properties
from FEM.fenicsx.src.RT.welch.FR import welch_fr
from FEM.bridge.export_data import export_T
from runs.caso_articulo_2.mcx.MC_interp import MC_interp
from dolfinx.fem import Function,assemble_scalar,form,Expression
import json

dir = sys.argv[1]

with open(f'{dir}/fenicsx/parameters.json', 'r') as file:
    parameters = json.load(file)

# print(parameters)

alpha = parameters['alpha']

# REGION PROPERTIES
regions = {
        'agar': [11, #GMSH physical tag
                  Material_Bioheat(k = 0.56, rho = 1070, c = 3400, w = 0, Qmet = 0),
                  Material_Optical(mu_a=1, mu_s=10000, g=0.9)],
        'agar_icg': [12, #GMSH physical tag
                  Material_Bioheat(k = 0.56, rho = 1070, c = 3400, w = 0, Qmet = 0),
                  Material_Optical(mu_a=alpha, mu_s=10000, g=0.9)]
        }
regions_bc = {
        # 'dirichlet': [],
        'convection': [9],
        }

T_dirichlet = 37

#REGION PROPERTIES
blood = Material_Bioheat_Blood(T = 37, rho = 1090, cp = 4200)

## LOAD MESH AND SCALE
mesh = load_mesh(dir)
mesh = scale_mesh(mesh,1e-2)

# SET FEM OBJECTS
mesh, V, regions, regions_bc = locate_dofs(mesh,regions,regions_bc)
mesh,T,v,x,coords,ds,dx = get_fem_objects(mesh,V)
k,rho,c,w,Qmet = set_dofs_properties(V,regions)
# bc = set_dirichlet_bcs(V,regions_bc['dirichlet'][1],T_dirichlet)
bc=[]

mu_a, mu_s, g = set_dofs_optical_properties(V,regions)

# SOURCE TERM
phi = Function(V)
Qs = Function(V)
# laser_irradiance  = 1*100**2 #W/m2
# laser_radius = 1.5e-2 #m
# laser_power = laser_irradiance*np.pi*laser_radius**2
laser_power = 1.7 #W
print(f"laser_power: {laser_power}")
phi.interpolate(lambda x: MC_interp(x,dir))
qs = phi*mu_a*laser_power
Qs.interpolate(Expression(qs,V.element.interpolation_points()))
# Qs.interpolate(qs_)

## stack coords and Qs
# print(coords.shape)
# print(Qs.x.array.shape)
export_qs = np.concatenate((coords,Qs.x.array.reshape(Qs.x.array.shape[0],1)),axis=1)
np.savetxt(f"{dir}/Qs_interpolated.csv",export_qs,delimiter=",")


# EXPORT FIELDS
# phi = assemble_scalar(phi)
export_field_mesh(mu_a,mesh,"mua",dir)
export_field_mesh(phi,mesh,"phi",dir)
export_field_mesh(Qs,mesh,"Qs",dir)

# print(regions_bc)

h = 0
# h = Function(V)

# Qs = p1_get_heat_source(V,mesh,v,coords,convection_bc_dofs,tumor_dofs,tejido_dofs,epidermis_dofs,dx,ds,domain_tumor_optical,domain_tejido_optical,domain_epidermis_optical,power)
# directory =  "bioheat-mc"
directory = dir

def Qs_func(t):
        if t <= 800:
                return Qs
        else:
                return Function(V)




sol = solve_FEM(V = V,msh = mesh[0],T = T,v = v,ds = ds,
        dx = dx,k = k,rho = rho,c = c,w = w,
        Qmet = Qmet,blood = blood,Qs_func = Qs_func,h = h,
        bc = bc,Ti = 0,Tref = 0,dt = 5,tf = 1600, 
        dir = directory, coords=coords,
        regions_bc=regions_bc,
        postprocess=False)

# print(len(sol))
# export_T(sol[0][1],dir)
import ufl
r = ufl.SpatialCoordinate(mesh[0])[0]
T_prom = np.zeros((len(sol),2))

total_power = assemble_scalar(form(Qs*r*dx))
print(f"total_power: {total_power*2*np.pi} W")
print(f"total_volume {assemble_scalar(form(r*dx))*2*np.pi} m3")


for i in range(len(sol)):
        T_prom[i,0] = sol[i][0]
        T_prom[i,1] = assemble_scalar(form(sol[i][1]*r*dx))/assemble_scalar(form(1*r*dx))
        # print(sol[i][0],T_prom[i,1])

np.save(f"{dir}/T_prom.npy",T_prom)

# print(sol[0][1].x.array == sol[1][1].x.array)
# T_int = assemble_scalar(form(sol[100][1]*dx))
# A_int = assemble_scalar(form(1*dx))
# prom = T_int/A_int
# prom = assemble_scalar(form(Qs*dx))
# print(prom)

