import numpy as np

import ufl
from dolfinx import fem, io
from dolfinx.fem import Function, locate_dofs_topological, dirichletbc,Expression
from ufl import ds, dx, grad, inner, Measure

from mpi4py import MPI
from petsc4py.PETSc import ScalarType
from petsc4py import PETSc

import FEM.fenicsx.src.postprocess_funcs as postprocess_funcs

def load_mesh(dir):
    print('Loading mesh...')
    with io.XDMFFile(MPI.COMM_WORLD, f"{dir}/fenicsx/mesh/xdmf/mesh_triangle.xdmf", "r") as xdmf:
        msh = xdmf.read_mesh(name="Grid")
        ct = xdmf.read_meshtags(msh, name="Grid")
    msh.topology.create_connectivity(msh.topology.dim, msh.topology.dim-1)
    with io.XDMFFile(MPI.COMM_WORLD, f"{dir}/fenicsx/mesh/xdmf/mesh_line.xdmf", "r") as xdmf:
        ft = xdmf.read_meshtags(msh, name="Grid")
    return msh,ct,ft

def scale_mesh(msh,scale):
    print('Scaling mesh...')
    coordmesh = msh[0].geometry.x
    coordmesh[:, :] *= scale
    return msh

def locate_dofs(mesh,regions,regions_bc):

    print('Defining function space')
    V = fem.FunctionSpace(mesh[0], ("Lagrange", 1))

    print('Locating DOFS regions')
    for region, tag in regions.items():
        facets = mesh[1].find(tag[0])
        regions[region].append(locate_dofs_topological(V, mesh[0].topology.dim, facets))
    for region, tag in regions_bc.items():
        facets = mesh[2].find(tag[0])
        regions_bc[region].append(locate_dofs_topological(V, mesh[0].topology.dim-1, facets))


    mesh[0].topology.create_connectivity(mesh[0].topology.dim-1, mesh[0].topology.dim)

    return mesh,V, regions, regions_bc
    
def get_fem_objects(mesh,V):
    print('Defining FEM objects')
    ds = Measure("ds", domain=mesh[0], subdomain_data=mesh[2])
    dx = Measure("dx", domain=mesh[0], subdomain_data=mesh[1])

    # Definicion de las funciones
    T = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)
    x = ufl.SpatialCoordinate(mesh[0])
    coords = V.tabulate_dof_coordinates()
    return mesh,T,v,x,coords,ds,dx

def set_dofs_properties(V,regions):

    print('Setting DOFS region properties')
    k = Function(V)
    rho = Function(V)
    c = Function(V)
    w = Function(V)
    Qmet = Function(V)

    for region, tag in regions.items():
        k.x.array[tag[3]] = tag[1].k
        rho.x.array[tag[3]] = tag[1].rho
        c.x.array[tag[3]] = tag[1].c
        w.x.array[tag[3]] = tag[1].w
        Qmet.x.array[tag[3]] = tag[1].Qmet

    return k,rho,c,w,Qmet

def export_mesh_facets(mesh,dir):
    mesh[0].topology.create_connectivity(mesh[0].topology.dim-1, mesh[0].topology.dim)
    with io.XDMFFile(mesh[0].comm, f"{dir}/fenicsx/results/export_facets/mesh_tags.xdmf", "w") as xdmf:
        xdmf.write_mesh(mesh[0])
        xdmf.write_meshtags(mesh[1])

def set_dirichlet_bcs(V,dirichlet_bc_dofs,temperature):
    print('Setting Dirichlet BCs')
    bc = [dirichletbc(ScalarType(temperature), dirichlet_bc_dofs, V)]
    return bc

def solve_FEM(V,msh,T,v,ds,dx,k,rho,c,w,Qmet,blood,Qs_func,h,bc,Ti,Tref,dt,tf,dir,coords,regions_bc,postprocess=True):
    print('Running Simulation...')
    x = ufl.SpatialCoordinate(msh)
    # Definicion de las ecuaciones
    T_old = Function(V)
    Qs=Function(V)
    # conv_bc = regions_bc['convection'][0]
    def get_forms():
        a = ((rho*c*T*v + dt*k*inner(grad(T), grad(v)))*x[0]*dx #laplaciano
            + dt*h*T*v*x[0]*ds #Condicion de convecccion natural
            + dt*T*blood.cp*blood.rho*w*v*x[0]*dx #Perfusion sanguinea
        )
        L = (rho*c*T_old*v*x[0]*dx
            + dt*inner(Qs, v)*x[0]*dx #Laser
            + dt*h*Tref*v*x[0]*ds #Condicion de convecccion natural
            + dt*blood.T*blood.cp*blood.rho*w*v*x[0]*dx#Perfusion sanguinea
            + dt*Qmet*v*x[0]*dx#Calor metabolico)
            )
        bilinear_form = fem.form(a)
        linear_form = fem.form(L)
        return bilinear_form,linear_form
    
    def create_systems(bilinear_form,linear_form):
        A = fem.petsc.assemble_matrix(bilinear_form, bcs=bc)
        A.assemble()
        b = fem.petsc.create_vector(linear_form)
        return A,b
    def get_solver(A):
        solver = PETSc.KSP().create(msh.comm)
        solver.setOperators(A)
        # solver.setType(PETSc.KSP.Type.PREONLY)  
        # solver.getPC().setType(PETSc.PC.Type.LU)
        solver.setType(PETSc.KSP.Type.BICG)
        solver.getPC().setType(PETSc.PC.Type.GAMG)
        return solver
    def transient_solver(b,bilinear_form,linear_form,bcs,solver,T_old,dt,tf,Qs):

        sol = []

        t = 0
        T_old.x.array[:] = Ti
        Tfem = fem.Function(V)
        Tfem.x.array[:] = Ti
        # Crear archivo XDMF y guardar condiciones iniciales
        xdmf = io.XDMFFile(msh.comm, f"{dir}/fenicsx/results/T.xdmf", "w")
        xdmf.write_mesh(msh)
        xdmf.write_function(T_old, t)

        num_steps = int(tf/dt) # numero de pasos de tiempo

        #create a txt file to store log
        for i in range(num_steps):
            # Avanzar en el tiempo
            # log = open(f"{dir}/fenicsx/log.txt", "a")
            # log.write(f"t = {t:.2f} / {tf:.2f} - Tmax = {Tfem.x.array.max()}\n")
            # log.close()
            sol.append((t,Tfem.copy()))
            t += dt

            # Ensamblar vector lineal
            Qs.interpolate(Expression(Qs_func(t), V.element.interpolation_points())) # Evaluar fuente de calor
            with b.localForm() as loc_b:
                loc_b.set(0)
            fem.petsc.assemble_vector(b, linear_form)

            # Aplicar condiciones de frontera
            fem.petsc.apply_lifting(b, [bilinear_form], [bcs])
            b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
            fem.petsc.set_bc(b, bcs)

            # Resolver sistema lineal
            solver.solve(b, Tfem.vector)
            # print(i)
            Tfem.x.scatter_forward()

            # Actualizar solucion anterior
            T_old.x.array[:] = Tfem.x.array

            # Guardar solucion en archivo XDMF
            if (i+1)*dt % 5 == 0:
                xdmf.write_function(Tfem, t)
                print(f"t = {t:.2f} / {tf:.2f}")
                print(f'Tmin = {Tfem.x.array.min()}')
                print(f'Tmax = {Tfem.x.array.max()}')
        return sol
        log.close()
    
        if postprocess==True:
            postprocess_funcs.write_max_temperature(Tfem)
            postprocess_funcs.write_max_temperature_position(Tfem,coords)
        

    bilinear_form,linear_form = get_forms()
    A,b = create_systems(bilinear_form,linear_form)
    solver = get_solver(A)
    sol=transient_solver(b,bilinear_form,linear_form,bc,solver,T_old,dt,tf,Qs)


    return sol

def export_field_mesh(field,msh,name,dir):
    msh = msh[0]
    xdmf = io.XDMFFile(msh.comm, f"{dir}/fenicsx/results/fields/{name}.xdmf", "w")
    xdmf.write_mesh(msh)
    xdmf.write_function(field, 0)
