
import ufl
from dolfinx import fem, io
from dolfinx.fem import Function, locate_dofs_topological, dirichletbc
from ufl import grad, inner, Measure
import numpy as np

from mpi4py import MPI
from petsc4py.PETSc import ScalarType
from petsc4py import PETSc


# Leer malla y subdominios
with io.XDMFFile(MPI.COMM_WORLD, "mesh.xdmf", "r") as xdmf:
    msh = xdmf.read_mesh(name="Grid")
    ct = xdmf.read_meshtags(msh, name="Grid")
msh.topology.create_connectivity(msh.topology.dim, msh.topology.dim-1)
with io.XDMFFile(MPI.COMM_WORLD, "mesh_lines.xdmf", "r") as xdmf:
    ft = xdmf.read_meshtags(msh, name="Grid")

#Reescalado de la malla
scale = 0.01
coordmesh = msh.geometry.x
coordmesh[:, :] *= scale

# Definir espacio de funciones
V = fem.FunctionSpace(msh, ("Lagrange", 1))

# Definir subdominios
tumor_facets = ct.find(10)
tumor_dofs = locate_dofs_topological(V, msh.topology.dim, tumor_facets)

# Definir fronteras
tejido_facets = ct.find(11)
tejido_dofs = locate_dofs_topological(V, msh.topology.dim, tejido_facets)

# Conectar malla y subdominios
msh.topology.create_connectivity(msh.topology.dim-1, msh.topology.dim)

# Verificar subdominios en formato para paraview
with io.XDMFFile(msh.comm, "facet_tags.xdmf", "w") as xdmf:
    xdmf.write_mesh(msh)
    xdmf.write_meshtags(ft)

# Definir integrales de superficie y volumen en terminos de los subdominios y fronteras
ds = Measure("ds", domain=msh, subdomain_data=ft)
dx = Measure("dx", domain=msh, subdomain_data=ct)

# Definir funciones de prueba y espacio de funciones
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

# Definir coordenadas
x = ufl.SpatialCoordinate(msh)


#LASER
alpha = Function(V) #1/m
beta = Function(V) #1/m
Io = 5000 #W/m2


#Conveccion natural
h = 5 #W/m2K
Tref = 25 #C

#Perfusion sanguinea
T_b = 37 #C

w_b = Function(V) # 1/s
for i in range(len(w_b.x.array)):
    if i in tumor_dofs:
        w_b.x.array[i] = 9.1e-4
    elif i in tejido_dofs:
        w_b.x.array[i] = 1e-3


rho_b = 1000 #kg/m3
cp_b = 4200 #J/kgK

#Calor metabolico
Qm = 1091 #W/m3

#Propiedades termofisicas y opticas
k = Function(V) #W/mK
for i in range(len(k.x.array)):
    if i in tumor_dofs:
        k.x.array[i] = 0.55
        alpha.x.array[i] = 12100
        beta.x.array[i] = 50.0
    elif i in tejido_dofs:
        k.x.array[i] = 0.50
        alpha.x.array[i] = 2
        beta.x.array[i] = 650.0

rho = Function(V) #kg/m3
for i in range(len(rho.x.array)):
    if i in tumor_dofs:
        rho.x.array[i] = 1100
    elif i in tejido_dofs:
        rho.x.array[i] = 1000

cp = 4200 #J/kgK

#LASER
# f = alpha*Io*ufl.exp(-(alpha+beta)*(0.01-x[1])) #W/m3 # Opcion 1
# f = 600*Io*ufl.exp(-(600+beta)*(0.01-x[1])) #W/m3 # Opcion 1

# Opcion 2
f = Function(V)
coords= V.tabulate_dof_coordinates()
f.x.array[:] = alpha.x.array[:]*Io*np.exp(-(alpha.x.array[:]+beta.x.array[:])*(0.01-coords[:,1])) #W/m3 # Opcion 2
# f.x.array[:] = 600*Io*np.exp(-(600+beta.x.array[:])*(0.01-coords[:,1])) #W/m3 # Opcion 2

#Condiciones iniciales
#DIRICHLET
T_dir = 37 #C

#Condiciones de frontera de Dirichlet
left_facets = ft.find(13)
left_dofs = locate_dofs_topological(V, msh.topology.dim-1, left_facets)
bcs = [dirichletbc(ScalarType(T_dir), left_dofs, V)]

#Condiciones iniciales
Tinitial = 35 #C
u_n = fem.Function(V)
u_n.x.array[:] = Tinitial

#Parametros de tiempo
t = 0 # tiempo inicial
dt = 1e-1 # paso de tiempo
t_final = 300 # tiempo final
num_steps = int(t_final/dt) # numero de pasos de tiempo


# Defininir problema variacional
# Old
a = ((rho*cp*u*v*x[0]
      + dt*k*inner(grad(u), grad(v))*x[0])*dx #laplaciano
      + dt*h*u*v*x[0]* ds(14) #Condicion de convecccion natural
      + dt*u*cp_b*rho_b*w_b*v*x[0]*dx #Perfusion sanguinea
      )
L = (rho*cp*u_n*v*x[0]*dx
    + dt*inner(f, v)*x[0]* dx(10) #Laser
    + dt*h*Tref*v*x[0]*ds(14) #Condicion de convecccion natural
    + dt*T_b*cp_b*rho_b*w_b*v*x[0]*dx#Perfusion sanguinea
    + dt*Qm*v*x[0]*dx#Calor metabolico)
    )

# a=(-(dt*k)/(rho*cp)*x[0]*inner(grad(u), grad(v))-\
#    x[0]*v*u-(w_b*rho_b*cp_b*dt)/(rho*cp)*x[0]*v*u)*dx-h*dt/(rho*cp)*x[0]*v*u*ds(14)
# L=(-dt/(rho*cp)*v*f*x[0]-v*u_n*x[0]-(w_b*rho_b*cp_b*dt)/(rho*cp)*v*T_b*x[0])*dx\
#     -h*dt/(rho*cp)*x[0]*v*Tref*ds(14)

# Crear forma bilineal y lineal
bilinear_form = fem.form(a)
linear_form = fem.form(L)

# Crear matrices y vectores PETSc
A = fem.petsc.assemble_matrix(bilinear_form, bcs=bcs)
A.assemble()
b = fem.petsc.create_vector(linear_form)

#PETSc solver
solver = PETSc.KSP().create(msh.comm)
solver.setOperators(A)
solver.setType(PETSc.KSP.Type.PREONLY)
solver.getPC().setType(PETSc.PC.Type.LU)

# Crear archivo XDMF para guardar condiciones iniciales
xdmf = io.XDMFFile(msh.comm, "results_transient/res.xdmf", "w")
xdmf.write_mesh(msh)
uh = fem.Function(V)
uh.x.array[:] = Tinitial
xdmf.write_function(uh, t)


# Resolver problema variacional en cada paso de tiempo
for i in range(num_steps):
    # Avanzar en el tiempo
    t += dt
    
    # Ensamblar vector lineal
    with b.localForm() as loc_b:
        loc_b.set(0)
    fem.petsc.assemble_vector(b, linear_form)

    # Aplicar condiciones de frontera
    fem.petsc.apply_lifting(b, [bilinear_form], [bcs])
    b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
    fem.petsc.set_bc(b, bcs)

    # Resolver sistema lineal
    solver.solve(b, uh.vector)
    uh.x.scatter_forward()

    # Actualizar solucion anterior
    u_n.x.array[:] = uh.x.array

    # Guardar solucion en archivo XDMF
    if (i+1)*dt % 10 == 0:
        xdmf.write_function(uh, t)
        print(f"t = {t:.2f} / {t_final:.2f}")


    

xdmf.close()